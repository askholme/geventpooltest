from django.test.utils import override_settings
from django.test import LiveServerTestCase
import hashlib
from .models import Item
from .tasks import download_images

class CeleryTestCase(LiveServerTestCase):
	cleans_up_after_itself = True
	def setUp(self):
		sp = Item.objects.create(name="Image Test",image_url=self.get_url(),image=None)
		sp.save()
	
	@override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
                          CELERY_ALWAYS_EAGER=True,
                          BROKER_BACKEND='memory')
	def testImagedownload(self):
		download_images()
		obj = Item.objects.get(name="Image Test")
		obj.image.open(mode='rb')
		md5 = hashlib.md5()
		for chunk in obj.image.chunks():
			md5.update(chunk)
		md5sum = md5.hexdigest()
		self.assertEqual(md5sum,'492ecffd8a4579f582a5bb2e3b567e27')
	
	def tearDown(self):
		#delete objects one by one to include the file
		for obj in Item.objects.all():
			obj.delete()
		
	def get_url(self):
		return "%s/static/download_image_test/img.png" % self.live_server_url