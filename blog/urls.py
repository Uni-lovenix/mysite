from django.conf.urls import url
from blog.views import archive, hello, hours_ahead, Order_notice, current_time, mypage_template, future_time

urlpatterns = [
	# url(r'^', archive),
	url(r'^archive$', archive),
	url(r'^hello$', hello),
	url(r'^time/plus/(\d{1,2})/$', hours_ahead),
	url(r'^order_notice$', Order_notice),
	url(r'^current_time$', current_time),
	url(r'^mypage$', mypage_template),
	url(r'^future_time/(\d{1,2})/$', future_time)
	]