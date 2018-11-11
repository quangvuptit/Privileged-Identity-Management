from django.conf.urls import url 
from . import views 

app_name = "ssh" 
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^(?P<id>[0-9]+)/$', views.detail, name='detail'),
	url(r'^(?P<id>[0-9]+)/connect$', views.connect, name='connectSSH'),
	url(r'^manage/', views.manage, name='manage'),
	url(r'^monitor/(?P<id>[0-9]+)$', views.monitor, name='monitor'),
	url(r'^ajax/get_User/$', views.get_User, name='get_User'),\
	url(r'^ajax/delete_User/$', views.delete_User, name='delete_User'),
	url(r'^ajax/add_User/$', views.add_User, name='add_User'),
    # ex: /polls/5/results/
]