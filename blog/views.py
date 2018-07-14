# coding=utf8
from django.contrib import auth
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.template import loader
from django.http import HttpResponse, Http404
from django.template import Template, Context
from django.shortcuts import render
from blog.models import BlogPost
from blog.models import ContentItems
from django import forms
from blog.models import Users
import datetime

SEX_CHOICES = ((True, 'male'), (False, 'female'))

class UserForm(forms.Form):
	username = forms.CharField(label='Name', max_length=50)
	password = forms.CharField(label='Password', max_length=50, widget=forms.PasswordInput)
	confirmpassword = forms.CharField(label='Confirm Password', max_length=50, widget=forms.PasswordInput)
	email = forms.EmailField(label='email')

class LoginUserForm(forms.Form):
	username = forms.CharField(label='Name', max_length=50)
	password = forms.CharField(label='Password', max_length=50, widget=forms.PasswordInput)

@csrf_exempt
def register(request):
	if request.method == 'POST':
		uf = UserForm(request.POST)
		if uf.is_valid():
			username = uf.cleaned_data['username']
			password = uf.cleaned_data['password']
			email = uf.cleaned_data['email']

			if username != None and password != None and email != None:
				User.objects.create_user(username=username, password=password, email=email)
				User.save()
				
				userlogin = auth.authenticate(username=account,password=password)
				auth.login(request,userlogin)
				return HttpResponseRedirect(ROOT_URL)
			else:
				return HttpResponse('regist failed!')
	else:
		uf = UserForm()
	return render(request, 'register.html',{'userform':uf})

@csrf_exempt
def login(request):
    if request.method == 'POST':
        uf = LoginUserForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']

            user = User.objects.filter(username__exact=username,password__exact=password)

            if user:
                return render(request, 'mypage.html',{'userform':uf})
            else:
                return HttpResponse('用户名或密码错误,请重新登录')
    else:
        uf = LoginUserForm()
    return render(request, 'login.html', {'userform':uf})

@csrf_exempt
def index(request):
	cis = ContentItems.objects.all()
	return render(request, 'index.html', {'posts':cis})
	
def hours_ahead(request, offset):
	try:
		offset = int(offset)
	except ValueError:
		raise(Http404())
	dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
	html = "In %s hour(s), it will be %s" % (offset, dt)
	return HttpResponse(html)

