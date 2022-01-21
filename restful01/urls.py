"""restful01 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('toys/', include('toys.urls')),
    path('model/', include('toysModel.urls')),
    path('drone/', include('drones.urls', namespace='v1')),
    path('api-auth/', include('rest_framework.urls',namespace='rest_framework_v1')),
    path('api-generate-token/', views.obtain_auth_token)  # para desplegar las vistas de login y logout en la esquina superior derecha del ApiRoot
    #path('drone/v2/', include('drones.v2.urls', namespace='v2')), 
    # path('v2/api-auth/', include('rest_framework.urls',namespace='rest_framework_v2')), # para desplegar las vistas de login y logout en la esquina superior derecha del ApiRoot
]
