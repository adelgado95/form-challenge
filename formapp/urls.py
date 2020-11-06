from django.conf.urls import include, url
from django.urls import path,re_path
from . import views	

urlpatterns = [
	path('', views.IndexView.as_view(), name='index'),
    path('person/add/', views.add_person, name='person-add'),
]