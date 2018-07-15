from django.conf.urls import url
from blog.views import login, register, index, logout_view

app_name='blog'

urlpatterns = [
    url(r'^login/$', login, name='login'),
    url(r'^regist/$', register, name='register'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^$', index),
	]