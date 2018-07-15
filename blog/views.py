# coding=utf8
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.template import loader
from django.http import HttpResponse, Http404
from django.shortcuts import render
from blog.models import ContentItems
from django import forms
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
				try:
					user = User.objects.create_user(username=username, password=password, email=email)
					user.save()
					
					userlogin = auth.authenticate(username=username,password=password)
					auth.login(request,userlogin)
					return HttpResponseRedirect(settings.ROOT_URL)
				except:
					return render(request, 'register.html', {'userform':uf, 'error': 'regist failed!'})
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

            user = auth.authenticate(username=username,password=password)
            if user is not None:
            	auth.login(request, user)
            	return HttpResponseRedirect(settings.ROOT_URL)
            return render(request, 'login.html', {'userform':uf, 'error':'用户名或密码错误,请重新登录'})
    else:
        uf = LoginUserForm()
    return render(request, 'login.html', {'userform':uf})

@csrf_exempt
def logout_view(request):
    auth.logout(request)
    return index(request)

@csrf_exempt
def index(request):
	cis = ContentItems.objects.all()
	return render(request, 'index.html', {'posts':cis})

@csrf_exempt
def own_zoom(request):
	pass
	
def hours_ahead(request, offset):
	try:
		offset = int(offset)
	except ValueError:
		raise(Http404())
	dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
	html = "In %s hour(s), it will be %s" % (offset, dt)
	return HttpResponse(html)

