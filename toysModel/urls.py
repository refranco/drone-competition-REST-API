from django.conf.urls import url
from django.urls import path
from toysModel import views

app_name = 'toysModel'
urlpatterns = [
	path('toys2/', views.toyM_list, name='list2'),
	path('toys2/<int:pk>/', views.toyM_detail, name='detail2'),
]