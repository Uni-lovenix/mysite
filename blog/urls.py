from django.conf.urls import url
import blog.views as views

app_name='blog'

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^regist/$', views.register, name='register'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^ownzone/$', views.own_zone, name='ownzone'),
    url(r'^submit_text/$', views.ajax_submit, name='submit_text'),
    url(r'^$', views.index, name='index'),
	]