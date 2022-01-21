from django.db import models
from django.utils import timezone
# Create your models here.

class Toy(models.Model):
	name = models.CharField(max_length=200, blank=False, default='')
	description = models.TextField(blank=True, default='')
	toy_category = models.CharField(max_length=200,blank=False, default='')
	created = models.DateTimeField(auto_now_add=True)
	release_date = models.DateTimeField(default=timezone.now())
	updated = models.DateTimeField(auto_now=True)
	was_included_in_home = models.BooleanField(default=False)

	class Meta:
		ordering = ('name',)