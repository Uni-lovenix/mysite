# coding=utf8
from django.template import loader
from django.http import HttpResponse, Http404
from django.template import Template, Context
from django.shortcuts import render
from blog.models import BlogPost
from django import forms
from blog.models import Users
import datetime

SEX_CHOICES = ((True, 'male'), (False, 'female'))

class UserForm(forms.Form):
	username = forms.CharField(label='Name', max_length=50)
	password = forms.CharField(label='Password', max_length=50, widget=forms.PasswordInput)
	email = forms.EmailField(label='email')
	phonenumber = forms.CharField(label='phonenumber', max_length=11)
	sex = forms.ChoiceField(widget=forms.RadioSelect,choices=SEX_CHOICES,label="sex")

class LoginUserForm(forms.Form):
	username = forms.CharField(label='Name', max_length=50)
	password = forms.CharField(label='Password', max_length=50, widget=forms.PasswordInput)


def register(request):
	if request.method == 'POST':
		uf = UserForm(request.POST)
		if uf.is_valid():
			username = uf.cleaned_data['username']
			password = uf.cleaned_data['password']
			email = uf.cleaned_data['email']
			phonenumber = uf.cleaned_data['phonenumber']
			sex = uf.cleaned_data['sex']

			Users.objects.create(username=username, password=password, email=email, \
				phonenumber=phonenumber, sex=sex)
			# Users.save()

			return HttpResponse('regist success!')
	else:
		uf = UserForm()
	return render(request, 'register.html',{'userform':uf})

def login(request):
    if request.method == 'POST':
        userform = LoginUserForm(request.POST)
        if userform.is_valid():
            username = userform.cleaned_data['username']
            password = userform.cleaned_data['password']

            user = User.objects.filter(username__exact=username,password__exact=password)

            if user:
                return render_to_response('index.html',{'userform':userform})
            else:
                return HttpResponse('用户名或密码错误,请重新登录')
    else:
        userform = UserForm()
    return render('login.html',{'userform':userform})

def archive(request):
	posts = BlogPost.objects.all()
	t = loader.get_template("archive.html")
	c = {'posts':posts}
	return HttpResponse(t.render(c))

def hello(request):
	html = 'Hello, welcome!'
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
