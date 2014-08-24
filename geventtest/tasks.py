from __future__ import absolute_import
from .models import Item
from gevent.pool import Pool
from gevent.queue import Queue,Empty as QueueEmpty
from datetime import datetime
from django.core.files.base import File
from django.db.models import Q
import requests, io,gevent,time
POOL_SIZE = 10
queue = Queue()

#support function to find image extension
class RequestFailed(Exception):
	pass
	
#throw exception if http status is not OK
def do_request(url):
	try:
		response = requests.get(url)
		if response.status_code != 200:
			raise Exception("HTTP status is %s" % response.status_code)
	except Exception as e:
		raise RequestFailed("Unable to download for %s - reason: %s" % (url,e))
	return response
#store fill in memory and put a django wrapper around it
def handle_file_response(response):
	file = io.BytesIO()
	for chunk in response.iter_content():
		file.write(chunk)
	return File(file)

# crawler function to run inside greenlet
def download_crawler():
	# eternal loop until break function is reached
	while 1:
		try:
			# get data from queue - will go to except if queue is empty
			queue_obj = queue.get(block=False)
			[sp_id,image_url] = queue_obj
			response = do_request(image_url)
			file = handle_file_response(response)
			Item.objects.get(pk=sp_id).image.save("%s_%s" % (sp_id,datetime.now().strftime("%Y%m%d%H%M%S")),file)
		except QueueEmpty:
			# stop if queue is empty
			break
		except RequestFailed:
			pass
		finally:
			#running below line fixes 
			#from django import db; db.close_old_connections()
			pass

#celery task call to download images on store products
def download_images():
	images_to_download = Item.objects.filter(Q(image__isnull=True) | Q(image=''),image_url__isnull=False).values_list('pk','image_url')
	for obj in images_to_download:
		queue.put(obj)
	# create greenlet pool and spawn workers
	pool = Pool(size=POOL_SIZE)
	pool.spawn(download_crawler)
	# eventlet uses free(), gevent uses free_count()
	while not pool.free_count() == POOL_SIZE:
		gevent.sleep(0.1)
		#eventlet.sleep
		for x in xrange(0, min(queue.qsize(), pool.free_count())):
			pool.spawn(download_crawler)
	# Wait for everything to complete - eventlet uses waitall
	pool.join()
	pool.kill()
	time.sleep(2)