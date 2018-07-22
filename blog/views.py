# coding=utf8
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.template import loader
from django.http import HttpResponse, Http404
from django.shortcuts import render
from blog.models import ContentItems, CaiZan
from django import forms
import datetime
import json

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
			error = ''
			username = uf.cleaned_data['username']
			password = uf.cleaned_data['password']
			password2 = uf.cleaned_data['confirmpassword']
			email = uf.cleaned_data['email']
			user_model = list(User.objects.all().values_list('username'))
			for i in user_model:
				if username in i:
					error += '用户名已存在!    '
			if password != password2:
				error += '两次密码输入不一致！请重新输入!'
			if error != '':
				return render(request, "register.html", {'userform':uf, 'error':error})

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
@login_required
def own_zone(request):
	username = request.user.username
	userid = request.user.id
	posts = ContentItems.objects.filter(uid=userid)
	return render(request, 'ownzone.html', {'username':username, 'posts':posts})

@login_required
@csrf_exempt
def ajax_submit(request):
	ret = {'status':True, 'error':None, 'data':None}
	if request.method=="POST":
		content = request.POST.get("content")
		# isanonymous = request.POST.get("IsAnonymous")
		if content == '':
			ret['status'] = False
			ret['error'] = '空文本不能提交...'
			return HttpResponse(json.dumps(ret))
		contentitem = ContentItems.objects.create(uid=request.user, postposition='', content=content, isshowname=True)
		contentitem.save()
		return HttpResponse(json.dumps(ret))
	ret['status'] = False
	ret['error'] = '发布失败'
	return HttpResponse(json.dumps(ret))
	
@csrf_exempt
def ajax_checkusername(request):
	pass

@login_required
@csrf_exempt
def ajax_cai(request):
	ret = {'status':True, 'error':None, 'data':None}
	cid = request.POST.get("cid")
	if request.method=="POST":
		try:
			cid=int(cid)
		except (TypeError,e):
			ret['status']=False
			ret['error']=e
			return HttpResponse(json.dumps(ret))
		c = ContentItems.objects.get(cid=cid)
		cz = CaiZan.objects.filter(uid=request.user, cid=cid)
		if cz:
			CaiZan.objects.filter(uid=request.user, cid=cid).delete()
			cai = c.cai
			c.cai = cai-1
			c.save()
		else:
			newcai = CaiZan.objects.create(uid=request.user, cid=c)
			newcai.save()
			cai = c.cai
			c.cai = cai+1
			c.save()
		ret['data']=c.cai
		return HttpResponse(json.dumps(ret))
	ret['error']='Unknown error.'
	return HttpResponse(json.dumps(ret))
