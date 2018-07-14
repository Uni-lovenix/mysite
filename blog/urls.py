from django.conf.urls import url
from blog.views import login, register, index

urlpatterns = [
    url(r'^login/$', login),
    url(r'^regist/$', register),
    url(r'^$', index),
	]