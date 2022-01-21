import pkgutil
import pytest
from urllib import response
from django.test import TestCase, client
from django.utils.http import urlencode
from django.urls import reverse
from django.utils import timezone
# for all te tests in apis and databases
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from drones import views
from drones.urls import app_name
# for DroneCategory test
from drones.models import DroneCategory

# for Pilot test
from drones.models import Pilot
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

# for drone test
from drones.models import Drone
# Create your tests here.

# url constantes
droneCategoryList_url = reverse(f'{app_name}:{views.DroneCategoryList.name}')
pilotList_url = reverse(f'{app_name}:{views.PilotList.name}')
droneList_url = reverse(f'{app_name}:{views.DroneList.name}')


class DroneCategoryTests(APITestCase):
	def post_drone_category(self, name):
		"""un metodo para postear una categoria de drone"""
		url = droneCategoryList_url
		data = {'name': name}
		client = APIClient()
		response = client.post(url, data, format='json')
		return response

	def test_post_and_get_drone_category(self):
		"""test para crear una nueva categoria de drone y poder recuperarla"""
		new_drone_category_name = 'test-category'
		response = self.post_drone_category(new_drone_category_name)
		print("\nPK {0}\n".format(DroneCategory.objects.get().pk))
		assert response.status_code == status.HTTP_201_CREATED
		assert DroneCategory.objects.count() == 1
		assert DroneCategory.objects.get().name == new_drone_category_name

	def test_post_existing_drone_category_name(self):
		"""nos aseguramos que no podemos crear otra categoria de drone continue
		   nombre existente"""
		url = droneCategoryList_url
		new_drone_category_name = 'test-category-duplicated'
		data = {'name':new_drone_category_name}
		response1 = self.client.post(url, data, format='json')
		assert response1.status_code == status.HTTP_201_CREATED
		response2 = self.client.post(url, data, format='json')
		print(response2)
		assert response2.status_code == status.HTTP_400_BAD_REQUEST

	def test_filter_drone_category_by_name(self):
		"""
		Ensure we can filter a drone category by name
		"""
		drone_name_1 = 'Hexacopter'
		drone_name_2 = 'Octocopter'
		self.post_drone_category(drone_name_1)
		self.post_drone_category(drone_name_2)
		filter_by_name = {'name':drone_name_1} #nombre a filtrar
		# componiendo url con el nombre a filtrar
		url =droneCategoryList_url+'?'+urlencode(filter_by_name)# construye una urlencoded por medio de un diccionario
		print(url)
		response = self.client.get(url, format='json')
		print(response)
		assert response.status_code == status.HTTP_200_OK
		# make user we received just one element in the response
		assert response.data['count'] == 1
		assert response.data['results'][0]['name'] == drone_name_1
	
	def test_update_drone_category(self):
		"""
		Ensure we can update a single field for a drone category
		"""
		drone_category_name = 'drone-category-1'
		response = self.post_drone_category(drone_category_name)
		print(response.data)
		# miremos que se creo el drone
		assert response.status_code == status.HTTP_201_CREATED		
		updated_url = droneCategoryList_url+str(response.data['pk']) # llamando /drone/drone-categories/pk
		print('UPDATED URL: ', updated_url)
		updated_name = 'Updated-name'
		data = {'name':updated_name}
		client = APIClient()
		path_response = client.patch(updated_url, data, format='json')
		assert path_response.status_code == status.HTTP_200_OK
		assert path_response.data['name'] == updated_name

	def test_get_drone_category(self):
		"""
		Ensure we can get a single drone category by id
		"""
		drone_category_name = 'drone-to-retrieve'
		response = self.post_drone_category(drone_category_name)
		url = reverse(f'{app_name}:{views.DroneCategoryList.name}')+str(response.data['pk'])
		print('\n',url,'\n')
		client = APIClient()
		response = client.get(url, format='json')
		assert response.status_code == status.HTTP_200_OK

		
class PilotTests(APITestCase):
	def post_pilot(self, name, gender, races_count):
		url = pilotList_url
		data = { 'name':name, 'gender':gender, 'races_count':races_count}
		response = self.client.post(url, data, format='json')
		return response
	
	def create_user_and_set_token_credentials(self):
		user = User.objects.create_user('user03','user03@example.com','user03password')
		token = Token.objects.create(user=user)
		self.client.credentials(HTTP_AUTHORIZATION='Token {0}'.format(token.key))
		#print('\n TOKEN',token.key,'\n')

	def test_try_to_post_pilot_without_token(self):
		"""
		Ensure we cannot create a pilot without a token
		"""
		pilot_name = 'Esteban'
		pilot_gender = 'M'
		pilot_races = 5
		response = self.post_pilot(pilot_name,pilot_gender, pilot_races)
		assert response.status_code == status.HTTP_401_UNAUTHORIZED
		assert Pilot.objects.count() == 0

	def test_post_and_get_pilot(self):
		"""Ensure we can create a Pilot and retrieve it,
		   Ensure we cannot retrieve the persisted pilot without autentication"""
		self.create_user_and_set_token_credentials()
		pilot_name = 'Esteban'
		pilot_gender = 'M'
		pilot_races = 5
		response = self.post_pilot(pilot_name,pilot_gender,pilot_races)
		print('\n PK {0}'.format(Pilot.objects.get().pk))
		assert response.status_code == status.HTTP_201_CREATED
		assert Pilot.objects.count() == 1

		# checking pilot in DB is the pilot we create
		saved_pilot = Pilot.objects.get()
		assert saved_pilot.name == pilot_name
		assert saved_pilot.gender == pilot_gender
		assert saved_pilot.races_count == pilot_races

		# checking authorized get response to the pilot
		url = pilotList_url+str(saved_pilot.pk)
		print(url)
		authorized_resp = self.client.get(url, format='json')
		assert authorized_resp.status_code == status.HTTP_200_OK
		assert authorized_resp.data['name'] == saved_pilot.name
		print('\n',self.client._credentials,'\n')
		# clean up credentials
		self.client.credentials()
		print('\n',self.client._credentials,'\n')
		unauthorized_resp = self.client.get(url, format='json')
		assert unauthorized_resp.status_code == status.HTTP_401_UNAUTHORIZED

	def test_update_pilot_with_autentication(self):
		# creating the pilot
		self.create_user_and_set_token_credentials()
		pilot_name = 'Esteban'
		pilot_gender = 'M'
		pilot_races = 5
		response = self.post_pilot(pilot_name,pilot_gender,pilot_races)
		# pilot created
		assert response.status_code == status.HTTP_201_CREATED
		pk = Pilot.objects.get().pk
		url_pilot = pilotList_url+str(pk)
		#update pilot with authentication
		data={'name':'Esteban-upd','gender': 'M','races_count':6}
		authorized_update = self.client.patch(url_pilot,data,format='json')
		assert authorized_update.status_code == status.HTTP_200_OK
		assert authorized_update.data['name']=='Esteban-upd'
		assert authorized_update.data['races_count'] == 6
		assert Pilot.objects.count() == 1
		# clean up credentials
		self.client.credentials()
		# updated pilot without credentials
		data_2={'name':'Esteban-No-Upd','gender': 'M','races_count':7}
		no_auth_update = self.client.patch(url_pilot,data_2,format='json')
		assert no_auth_update.status_code == status.HTTP_401_UNAUTHORIZED
		assert Pilot.objects.count() == 1
		assert Pilot.objects.get().name == data['name']
		assert Pilot.objects.get().races_count == data['races_count']
	
	def test_filter_pilot_with_autentication(self):
		self.create_user_and_set_token_credentials()
		pilot_name_1 = 'Esteban'
		pilot_gender_1 = 'M'
		pilot_races_1 = 5
		response1 = self.post_pilot(pilot_name_1,pilot_gender_1,pilot_races_1)
		pilot_name_2 = 'Paula'
		pilot_gender_2 = 'F'
		pilot_races_2 = 5
		response2 = self.post_pilot(pilot_name_2,pilot_gender_2,pilot_races_2)
		# check there are two pilotes created
		assert Pilot.objects.count() == 2

		# filter by name
		filter_by_name = {'name':pilot_name_1}
		url_name = pilotList_url+'?'+urlencode(filter_by_name) # construye una urlencoded por medio de un diccionario
		resp_filter1 = self.client.get(url_name, format='json')
		assert resp_filter1.status_code == status.HTTP_200_OK
		assert resp_filter1.data['count'] == 1
		assert resp_filter1.data['results'][0]['name'] == pilot_name_1
		
		# filter_by_gender
		filter_by_gender ={'gender':pilot_gender_2}
		url_gender = pilotList_url+'?'+urlencode(filter_by_gender)
		resp_filter2= self.client.get(url_gender, format='json')
		assert resp_filter2.status_code == status.HTTP_200_OK
		assert resp_filter2.data['count'] == 1
		assert resp_filter2.data['results'][0]['gender'] == pilot_gender_2

		# filter_by_races_count
		filter_by_races = {'races_count':5}
		url_races = pilotList_url+'?'+urlencode(filter_by_races)
		resp_filter3 = self.client.get(url_races, format='json')
		assert resp_filter3.status_code == status.HTTP_200_OK
		assert resp_filter3.data['count'] == 2

		#cleaning autentication
		self.client.credentials()
		resp_filter1 = self.client.get(url_name, format='json')
		assert resp_filter1.status_code == status.HTTP_401_UNAUTHORIZED

	def test_delete_pilot_with_authentication(self):
		self.create_user_and_set_token_credentials()
		pilot_name = 'Esteban'
		pilot_gender = 'M'
		pilot_races = 5
		response = self.post_pilot(pilot_name,pilot_gender,pilot_races)
		assert Pilot.objects.count() == 1
		# clean up authentication
		self.client.credentials()
		pk = Pilot.objects.get().pk
		url_pilot = pilotList_url+str(pk)
		# delete pilot without authentication
		response2 =  self.client.delete(url_pilot,format='json')
		assert response2.status_code == status.HTTP_401_UNAUTHORIZED
		# create credentials
		token = Token.objects.get()
		self.client.credentials(HTTP_AUTHORIZATION='Token {0}'.format(token.key))
		# delete object with token credential
		response3 = self.client.delete(url_pilot,format='json')
		assert response3.status_code == status.HTTP_204_NO_CONTENT
		assert Pilot.objects.count() == 0

	def test_search_pilot_by_name(self):
		self.create_user_and_set_token_credentials()
		pilot_name_1 = 'Esteban'
		pilot_gender_1 = 'M'
		pilot_races_1 = 5
		response1 = self.post_pilot(pilot_name_1,pilot_gender_1,pilot_races_1)
		pilot_name_2 = 'Paula'
		pilot_gender_2 = 'F'
		pilot_races_2 = 5
		response3 = self.post_pilot(pilot_name_2,pilot_gender_2,pilot_races_2)
		pilot_name_3 = 'Branca'
		pilot_gender_3 = 'F'
		pilot_races_3 = 5
		response3 = self.post_pilot(pilot_name_3,pilot_gender_3,pilot_races_3)
		assert Pilot.objects.count() == 3
		# url search by name
		search_name = {'search':pilot_name_3}
		url_search = pilotList_url + '?' + urlencode(search_name)

	def test_nopossible_post_duplicated_pilot_name(self):
		self.create_user_and_set_token_credentials()
		pilot_name = 'Esteban'
		pilot_gender = 'M'
		pilot_races = 5
		response = self.post_pilot(pilot_name,pilot_gender,pilot_races)
		assert response.status_code == status.HTTP_201_CREATED
		assert response.data['name'] == pilot_name
		# re posting the pilot
		response2 = self.post_pilot(pilot_name, pilot_gender, pilot_races)
		assert response2.status_code == status.HTTP_400_BAD_REQUEST
		assert Pilot.objects.count() == 1

class DroneTests(APITestCase):
	def post_drone_category(self, name):
		"""un metodo para postear una categoria de drone"""
		url = droneCategoryList_url
		data = {'name': name}
		client = APIClient()
		response = client.post(url, data, format='json')
		return response

	# autenticarse
	def user1_login(self):
		user = User.objects.create_user('user01','user01@example.com','user01password')
		self.client.login(username='user01',password='user01password')

	def user2_login(self):
		user = User.objects.create_user('user02','user02@example.com','user02password')
		self.client.login(username='user02',password='user02password')

	def post_drone(self, name, drone_category,manufacturing_date, has_it_competed):
		data = {'name':name,'drone_category':drone_category, 
			'manufacturing_date':manufacturing_date,
			'has_it_competed':has_it_competed}
		# creating a drone
		response = self.client.post(droneList_url, data, format='json' )
		return response

	def test_post_drone_with_authentication(self):
		"""
		Ensure we can only post a drone with authentication
		"""
		drone_category = 'Drone-cat-1'
		# crear una categoria de drone
		self.post_drone_category(drone_category)

		#Autenticarse with user 1
		self.user1_login()

		# postear drone
		name = 'Falcon Collar'
		manufacturing_date = timezone.now()
		has_it_competed = True
		response = self.post_drone(name,drone_category,manufacturing_date,has_it_competed)
		assert response.status_code == status.HTTP_201_CREATED
		assert response.data['name'] == name
		assert response.data['owner'] == 'user01'
		assert Drone.objects.count() == 1
		# logout
		self.client.logout()
		name2 = 'Falcon 2'
		# checking unauthorized post
		response2 = self.post_drone(name2,drone_category,manufacturing_date,has_it_competed)
		assert response2.status_code == status.HTTP_401_UNAUTHORIZED
		assert Drone.objects.count() == 1
		
	def test_post_and_get_drone(self):
		"""
		Ensure we can only post a drone with authentication
		"""
		drone_category = 'Drone-cat-1'
		# crear una categoria de drone
		self.post_drone_category(drone_category)

		#Autenticarse with user 1
		self.user1_login()

		# postear drone
		name = 'Falcon Collar'
		manufacturing_date = timezone.now()
		has_it_competed = True
		response = self.post_drone(name,drone_category,manufacturing_date,has_it_competed)
		assert response.status_code == status.HTTP_201_CREATED

		# get the drone created
		pk = Drone.objects.get().pk
		url_drone = droneList_url + str(pk)
		response2 = self.client.get(url_drone,format='json')
		assert response2.status_code == status.HTTP_200_OK
		assert response2.data['name'] == name

	def test_post_existing_drone_name(self):
		"""
		Ensure we cannot create two drones with the same name
		"""
		drone_category = 'Drone-cat-1'
		# crear una categoria de drone
		self.post_drone_category(drone_category)

		#Autenticarse with user 1
		self.user1_login()

		# postear drone
		name = 'Falcon Collar'
		manufacturing_date = timezone.now()
		has_it_competed = True
		response = self.post_drone(name,drone_category,manufacturing_date,has_it_competed)
		assert response.status_code == status.HTTP_201_CREATED

		# postear 2do con el mismo nombre NO es posible
		response2 = self.post_drone(name,drone_category,manufacturing_date,False)
		assert response2.status_code == status.HTTP_400_BAD_REQUEST

	def test_drone_SAFE_METHODS_with_no_authentication(self):
		"""
		Ensure we can use safe methods like GET, OPTIONS, HEAD with no authentication
		"""
		drone_category = 'Drone-cat-1'
		# crear una categoria de drone
		self.post_drone_category(drone_category)

		#Autenticarse with user 1
		self.user1_login()

		# postear drone
		name_drone_1 = 'Falcon Collar'
		manufacturing_date = timezone.now()
		has_it_competed = True
		response = self.post_drone(name_drone_1,drone_category,manufacturing_date,has_it_competed)
		assert response.status_code == status.HTTP_201_CREATED
		assert response.data['name'] == name_drone_1
		pk_1 = Drone.objects.get().pk

		# postear segundo drone
		name_drone_2 = 'Falcon Collar 2'
		response2 = self.post_drone(name_drone_2,drone_category,manufacturing_date,False)
		assert response2.status_code == status.HTTP_201_CREATED
		assert response2.data['name'] == name_drone_2
		# chequear que hay 2 drones en la DB
		assert Drone.objects.count() == 2

		# chequear methodos sin autenticacion
		self.client.logout()
		# check GET method with drone list
		no_auth_response1 = self.client.get(droneList_url, format='json')
		assert no_auth_response1.status_code == status.HTTP_200_OK
		assert no_auth_response1.data['count'] == 2
		url_drone_1 = droneList_url + str(pk_1)
		# check metodo GEt with Drone detail
		no_auth_response2 = self.client.get(url_drone_1, format='json')
		assert no_auth_response2.status_code == status.HTTP_200_OK
		assert no_auth_response2.data['name'] == name_drone_1

		# check Metodo OPTIONS
		no_auth_response3 = self.client.options(droneList_url, format='json')
		assert no_auth_response3.status_code == status.HTTP_200_OK
		no_auth_response4 = self.client.options(url_drone_1, format='json')
		assert no_auth_response4.status_code == status.HTTP_200_OK

	def test_delete_drone_only_owner(self):
		"""
		Ensure only owner can DELETE a drone of  his property
		"""
		drone_category = 'Drone-cat-1'
		# crear una categoria de drone
		self.post_drone_category(drone_category)

		#Autenticarse with user 1
		self.user1_login()

		# postear drone
		name_drone_1 = 'Falcon Collar'
		manufacturing_date = timezone.now()
		has_it_competed = True
		response = self.post_drone(name_drone_1,drone_category,manufacturing_date,has_it_competed)
		assert Drone.objects.count() == 1 # first drone created
		pk_drone_1 = Drone.objects.get().pk
		url_drone_user1 = droneList_url + str(pk_drone_1)
		# logout and login with user 2
		self.client.logout()
		self.user2_login()

		# trying to DELETE another user's drone
		response2 = self.client.delete(url_drone_user1, format='json')
		assert response2.status_code == status.HTTP_403_FORBIDDEN
		assert Drone.objects.count() == 1 # the drone still exist
		assert Drone.objects.get().name == name_drone_1

		# Login with user 1 and DELETE the drone
		self.client.logout()
		self.client.login(username='user01', password='user01password')
		response3 = self.client.delete(url_drone_user1, format='json')
		assert response3.status_code == status.HTTP_204_NO_CONTENT
		assert Drone.objects.count() == 0

	def test_patch_drone_only_owner(self):
		"""
		Ensure only owner can PATCH a drone of  his property
		"""
		drone_category = 'Drone-cat-1'
		# crear una categoria de drone
		self.post_drone_category(drone_category)

		#Autenticarse with user 1
		self.user1_login()

		# postear drone
		name_drone_1 = 'Falcon Collar'
		manufacturing_date = timezone.now()
		has_it_competed = True
		response = self.post_drone(name_drone_1,drone_category,manufacturing_date,has_it_competed)
		assert Drone.objects.count() == 1 # first drone created
		# get drone url
		pk_drone_1 = Drone.objects.get().pk
		url_drone_user1 = droneList_url + str(pk_drone_1)

		# PATCH drone from same owner
		response2 = self.client.patch(url_drone_user1, {'has_it_competed':False}, format='json')
		assert response2.status_code == status.HTTP_200_OK
		
		assert Drone.objects.get(pk=pk_drone_1).has_it_competed == False
		# logout and login with user 2
		self.client.logout()
		self.user2_login()

		# trying to PATCH another user's drone
		response3 = self.client.patch(url_drone_user1, {'name':'Falcon-updated'}, 'json')
		assert response3.status_code == status.HTTP_403_FORBIDDEN
		assert Drone.objects.get().name == name_drone_1
		
