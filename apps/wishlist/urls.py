from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^login$', views.login),
	url(r'^logout$', views.logout),
	url(r'^register$', views.register),
	url(r'^dashboard$', views.dashboard),
	url(r'^wish_items/(?P<item_id>\d+)$', views.aboutitem),
	url(r'^wish_items/create$', views.itemform),
	url(r'^additem$', views.additem),
	url(r'^(?P<item_id>\d+)/delete$', views.delete),
	url(r'^(?P<item_id>\d+)/addwish$', views.addwish),
	url(r'^(?P<item_id>\d+)/removewish$', views.removewish),
	#(?P<user_id>\d+)
  ]