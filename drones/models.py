from django.db import models
from django.db.models.enums import Choices
from django.utils import timezone

# mi propias librerias para generar el token
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import  User

# Create your models here.

class DroneCategory(models.Model):
	name = models.CharField(max_length=250,null=False, verbose_name='Categoria Drone', unique=True)

	class Meta:
		ordering = ('name',)

	def __str__(self):
		return self.name

class Drone(models.Model):
	name = models.CharField(max_length=100, null=False, unique=True)
	drone_category = models.ForeignKey(DroneCategory, related_name='drones', on_delete= models.CASCADE)
	manufacturing_date = models.DateTimeField(null=True, blank=True)
	has_it_competed  = models.BooleanField(verbose_name='Has it completed a competition')
	created_at = models.DateTimeField(auto_now_add=True)
	owner  = models.ForeignKey('auth.User',related_name='drones',on_delete=models.CASCADE)
	

	class Meta:
		ordering = ('name',)
	
	def __str__(self):
	    return self.name

class Pilot(models.Model):
	GENDER_CHOICES = [('M','MALE'), ('F','FEMALE')]
	name = models.CharField(max_length=100, blank=False, default='', unique=True)
	gender = models.CharField(max_length=2, choices=GENDER_CHOICES, default='')
	races_count = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('name',)
	
	def __str__(self):
	    return self.name

class Competition(models.Model):
	pilot = models.ForeignKey(Pilot, on_delete=models.CASCADE, related_name='competitions')
	drone = models.ForeignKey(Drone, on_delete=models.CASCADE)
	distance_in_feet = models.FloatField(default=0.0)
	distance_achievement_date = models.DateTimeField()
	
	class Meta:
		# Order by distance in descending order
		ordering = ('-distance_in_feet',)
		
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
# 	if created:
# 		Token.objects.create(user=instance)
# 	for user in User.objects.all():
# 		Token.objects.get_or_create(user=user)