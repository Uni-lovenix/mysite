from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from blog.api import views

urlpatterns = [
	url(r'^caizan/$', views.caizan_post),
	url(r'^caizan/(?P<pk>[0-9]+)/$', views.CaiZanAPI.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)