from django.conf.urls import url
import blog.views as views

app_name='blog'

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^regist/$', views.register, name='register'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^ownzone/$', views.own_zone, name='ownzone'),
    url(r'^submit_text/$', views.ajax_submit, name='submit_text'),
    url(r'^ajax_cai/$', views.ajax_cai, name='ajax_cai'),
    url(r'^ajax_remove_content/$', views.ajax_remove_content, name='ajax_remove_content'),
    url(r'^ajax_submit_comment/$', views.ajax_submit_comment, name='ajax_submit_comment'),
    url(r'^ajax_comment/$', views.ajax_comment, name='ajax_comment'),
    url(r'^ajax_getcontents/$', views.ajax_getcontents, name='ajax_getcontents'),
    url(r'^$', views.index, name='index'),
	]