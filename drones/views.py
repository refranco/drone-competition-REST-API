from datetime import datetime
from django.shortcuts import render
from rest_framework import  generics, status
from rest_framework.response import Response  # para crear la respuesta tipo JSON en la api-root
from rest_framework.reverse import reverse
# importing all the models
from drones.models import DroneCategory, Drone, Pilot, Competition
# importing all the serializers 
from drones.serializers import DroneCategorySerializer, DroneSerializer, \
	PilotSerializer, PilotCompetitionSerializer, UserTokenSerializer

# adding filtering, searching and ordering capabilities
from django_filters import AllValuesFilter, DateTimeFilter, NumberFilter
import django_filters

# setting permission and authentication
from rest_framework import permissions
from drones import custompermission
from rest_framework.permissions import IsAuthenticated


# for token autentication
from rest_framework.authentication import TokenAuthentication
from drones import customautentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken  # para alterar el login y obtener el token

# setting throttling policies
from rest_framework.throttling import ScopedRateThrottle, UserRateThrottle
from datetime import datetime

# para trabajar con sesiones
from django.contrib.sessions.models import Session
# Create your views here.

# class CustomAuthentication(authentication.BaseAuthentication):
# 	def authenticate(self, request):
# 		if request.user.is_authenticated:
# 			token,_= Token.objects.get_or_create(user=request.user)


class DroneCategoryList(generics.ListCreateAPIView):
	queryset = DroneCategory.objects.all()
	serializer_class = DroneCategorySerializer
	name = 'dronecategory-list'
	filterset_fields = ( # para filtros, mirar setting / DEFAULT_FILTER_BACKENDS
		'name',
	)
	search_fields = (
		'^name', # el gorro ^ es para indicar una coincidencia starts-with
	)
	ordering_fields = (
		'name',
	)

	
class DroneCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = DroneCategory.objects.all()
	serializer_class = DroneCategorySerializer
	name = 'dronecategory-detail'

class DroneList(generics.ListCreateAPIView):
	queryset = Drone.objects.all()
	serializer_class = DroneSerializer
	name = 'drone-list'
	filterset_fields = ( # para filtros, mirar setting / DEFAULT_FILTER_BACKENDS
		'name',
		'drone_category',
		'manufacturing_date',
		'has_it_competed',
	)
	search_fields = ( # para filtros, mirar setting / DEFAULT_FILTER_BACKENDS
		'^name',
	)
	ordering_fields = ( # para filtros, mirar setting / DEFAULT_FILTER_BACKENDS
		'name',
		'manufacturing_date',
		'created_at',
	)
	permission_classes = (
		permissions.IsAuthenticatedOrReadOnly,
		custompermission.IsCurrentUserOwnerOrReadOnly,
	)
	# configurando politica de throttling
	throttle_scope = 'drones' # mirar en settings este scope
	throttle_classes = (ScopedRateThrottle,)

	def perform_create(self, serializer): # sobreescribiendo el metodo perform_create para añadir al campo owner el usuario que hace el POST request
	    serializer.save(owner=self.request.user)

class DroneDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Drone.objects.all()
	serializer_class = DroneSerializer
	name = 'drone-detail'
	# permitiondo cualquier usuario solo lectura, modificacion solo para dueños, mirar custompermission.py
	permission_classes = ( 
		permissions.IsAuthenticatedOrReadOnly,
		custompermission.IsCurrentUserOwnerOrReadOnly,
	)
	# configurando politica de throttling
	throttle_scope = 'drones' # mirar en settings este scope
	throttle_classes = (ScopedRateThrottle,)

class PilotList(generics.ListCreateAPIView):
	queryset = Pilot.objects.all()
	serializer_class = PilotSerializer
	name = 'pilot-list'
	filterset_fields = ( # para filtros, mirar setting / DEFAULT_FILTER_BACKENDS
		'name',
		'gender',
		'races_count',
	)
	search_fields = ( # para filtros, mirar setting / DEFAULT_FILTER_BACKENDS
		'^name',
	)
	ordering_fields = (# para filtros, mirar setting / DEFAULT_FILTER_BACKENDS
		'name',
		'races_count'
	)
	permission_classes = ( # para trabajar con permisos y autenticación con token. mirar setting / rest_framework.authtoken
		IsAuthenticated,
	)
	authentication_classes = ( # para trabajar con permisos y autenticación con token. mirar setting / rest_framework.authtoken
		TokenAuthentication,
	)
	# configurando politica de throttling
	throttle_scope = 'pilots' # mirar en settings este scope
	throttle_classes = (ScopedRateThrottle,)
	
	# def get(self, request, format=None):
	# 	content = {
	# 	'user': str(request.user),  # `django.contrib.auth.User` instance.
	# 	'auth': str(request.auth),  # None
	# 	}
	# 	headers = {'WWW-Authenticate':Token.objects.get(user=request.user).key}
	# 	return Response(content, headers=headers)

class PilotDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Pilot.objects.all()
	serializer_class = PilotSerializer
	name = 'pilot-detail'
	authentication_classes = ( # para trabajar con permisos y autenticación con token. mirar setting / rest_framework.authtoken
		TokenAuthentication,
	)
	permission_classes = ( # para trabajar con permisos y autenticación con token. mirar setting / rest_framework.authtoken
		IsAuthenticated,
	)
	# configurando politica de throttling
	throttle_scope = 'pilots' # mirar en settings este scope
	throttle_classes = (ScopedRateThrottle,)

class CompetitionFilter(django_filters.FilterSet): #**** Linea cambia con respecto al libro (django_filters.FilterSet)
	from_achievement_date = DateTimeFilter(
		field_name='distance_achievement_date', lookup_expr='gte')
	to_achievement_date = DateTimeFilter(
		field_name='distance_achievement_date', lookup_expr='lte')
	min_distance_in_feet = NumberFilter(
		field_name='distance_in_feet', lookup_expr='gte')
	max_distance_in_feet = NumberFilter(
		field_name='distance_in_feet', lookup_expr='lte')
	drone_name = AllValuesFilter(
		field_name='drone__name')
	pilot_name = AllValuesFilter(
		field_name='pilot__name')
	
	class Meta:
		model = Competition
		fields = (
			'distance_in_feet',
			'from_achievement_date',
			'to_achievement_date',
			'min_distance_in_feet',
			'max_distance_in_feet',
			# drone__name will be accessed as drone_name
			'drone_name',
			# pilot__name will be accessed as pilot_name
			'pilot_name',
		)

class CompetitionList(generics.ListCreateAPIView):
	queryset = Competition.objects.all()
	serializer_class = PilotCompetitionSerializer
	name = 'competition-list'
	filter_class = CompetitionFilter  # mirar anterior FilterSet creado: CompetitionFilter
	ordering_fields = (
		'distance_in_feet',
		'distance_achievement_date',
	)

class CompetitionDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Competition.objects.all()
	serializer_class = PilotCompetitionSerializer
	name = 'competition-detail'


class ApiRoot(generics.GenericAPIView):
	name = 'api-root'
	
	def get(self, request, *args, **kwargs):
		return Response({
			'drone-categories': reverse(DroneCategoryList.name, request=request),
			'drones': reverse(DroneList.name, request=request),
			'pilots': reverse(PilotList.name, request=request),
			'competitions': reverse(CompetitionList.name, request=request)
		})

class Login(ObtainAuthToken):

	def post(self, request, *args, **kwargs):
		# en el request.data vienen el username y password porque esta clase hereda de ObtainAuthToken
		login_serializer = self.serializer_class(data=request.data, context={'request':request})
		if login_serializer.is_valid():
			print(login_serializer.validated_data)
			user = login_serializer.validated_data['user']
			token,created = Token.objects.get_or_create(user = user)
			print(token.key)
			if created:
				return Response({'user':UserTokenSerializer(user).data,
					'token':token.key,
					'mensaje':f'Hola {user}, has iniciado sesion'},
					status=status.HTTP_201_CREATED)
			else:
				# ---- para borrar todas las sesiones en un nuevo login ------------
				# all_session = Session.objects.filter(expire_date_gte=datetime.now())
				# if all_session.exists():
				# 	for session in all_session:
				# 		session_data = session.get_decoded()
				# 		if int(session['auth_user_id']) == user.id:
				# 			session.delete()
				token.delete()
				token = Token.objects.create(user = user)

				return Response({'user':UserTokenSerializer(user).data,
					'token':token.key,
					'mensaje':f'Hola {user}, has iniciado sesion'},
					status=status.HTTP_201_CREATED)
		else:
			return Response({'mensaje':'el usuario es invalido'}, status=status.HTTP_400_BAD_REQUEST)
		