from django.db import models

# Create your models here.
class Item(models.Model):
	"""(Item description)"""
	name = models.CharField(blank=True, max_length=100)
	image_url = models.URLField(blank=True)
	image = models.FileField(upload_to="testpath/")
	class Admin:
		list_display = ('',)
		search_fields = ('',)

	def __unicode__(self):
		return u"Item"
