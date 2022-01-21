from django.conf.urls import url
from django.urls import  path
from toys import views

app_name='toys'
urlpatterns = [
	path('', views.toy_list, name='list'),
	path('<int:pk>/', views.toy_detail, name='detail'),
	#url(r'^toys/(?P<pk>[0-9]+)$', views.toy_detail),
]