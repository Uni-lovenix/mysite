from django.template import loader
from django.http import HttpResponse, Http404
from django.template import Template, Context
from django.shortcuts import render
from blog.models import BlogPost
import datetime

def archive(request):
	posts = BlogPost.objects.all()
	t = loader.get_template("archive.html")
	c = {'posts':posts}
	return HttpResponse(t.render(c))
	

def hello(request):
	html = 'Current time is: %s' % datetime.datetime.now()
	return HttpResponse(html)

def current_time(request):
	now = datetime.datetime.now()
	return render(request, 'app/current_time.html', {'current_date': now})
	
def hours_ahead(request, offset):
	try:
		offset = int(offset)
	except ValueError:
		raise(Http404())
	dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
	html = "In %s hour(s), it will be %s" % (offset, dt)
	return HttpResponse(html)

def Order_notice(request):
	t = loader.get_template("t1.html")
	c = {"person_name": "Mike", 
		"company": "Huawei",
		"ship_date": datetime.date(2016,7,7), 
		"order_warranty": False}
	return HttpResponse(t.render(c))


def mypage_template(request):
	now = datetime.datetime.now()
	return render(request, 'mypage.html', {'title': 'FIRST', 'current_section': now})

def future_time(request, offset):
	try:
		offset = int(offset)
	except ValueError:
		raise(Http404())
	dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
	return render(request, "app/future.html", {'hour_offset':offset, 'next_time':dt})
