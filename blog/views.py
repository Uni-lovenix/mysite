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
from blog.models import ContentItems, CaiZan, Comment
from django import forms
from django.core import serializers
from django.db.models import Q
import datetime
import json
import re

SEX_CHOICES = ((True, 'male'), (False, 'female'))

class UserForm(forms.Form):
	username = forms.CharField(label='Name', max_length=50, error_messages={"required":"username不能为空",})
	password = forms.CharField(label='Password', max_length=50, widget=forms.PasswordInput)
	confirmpassword = forms.CharField(label='Confirm Password', max_length=50, widget=forms.PasswordInput)
	email = forms.EmailField(label='email', error_messages={"required":"email不能为空",})

class LoginUserForm(forms.Form):
	username = forms.CharField(label='Name', max_length=50)
	password = forms.CharField(label='Password', max_length=50, widget=forms.PasswordInput)

def check_illegal_char(s):
	illegal_char = r'[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）]+'
	if re.match(illegal_char, s)==None:
		return True
	return False

def check_cid(cid):
	try:
		cid = int(cid)
	except:
		return -1
	return cid

@csrf_exempt
def register(request):
	if request.method == 'POST':
		uf = UserForm(request.POST)
		if uf.is_valid():
			error = ''
			username = uf.cleaned_data['username']
			if check_illegal_char(username)==False:
				return render(request, 'register.html', {'userform':uf, 'error': '用户名含有非法字符!'})

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
	# cis = ContentItems.objects.all().order_by('-posttime')
	# return render(request, 'index.html', {'posts':cis})
	return render(request, 'index.html')

@csrf_exempt
def ajax_getcontents(request):
	if request.method=="POST":
		current=request.POST.get('current')
		current=check_cid(current)
		num=7
		if current==-1 or num==-1:
			ret['status']=False
			ret['error']='request data error.'
			return Http404()
		posts=ContentItems.objects.all().order_by('-posttime')[current:current+num]
		return render(request, 'includes/content.html', {'posts':posts})

@csrf_exempt
@login_required
def own_zone(request):
	username = request.user.username
	userid = request.user.id
	posts = ContentItems.objects.filter(uid=userid).order_by('-posttime')
	return render(request, 'ownzone.html', {'username':username, 'posts':posts})

@login_required
@csrf_exempt
def ajax_submit(request):
	ret = {'status':True, 'error':None, 'data':None}
	if request.method=="POST":
		content = request.POST.get("content")
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
	if request.method=="POST":
		cid = request.POST.get("cid")
		cid = check_cid(cid)
		if cid==-1:
			ret['status']=False
			ret['error']='失败!'
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

@login_required(login_url='/login/')
@csrf_exempt
def ajax_remove_content(request):
	ret = {'status':True, 'error':None, 'data':None}
	if request.method=="POST":
		cid = request.POST.get('cid')
		cid = check_cid(cid)
		if cid!=-1:
			ContentItems.objects.get(cid=cid).delete()
			return HttpResponse(json.dumps(ret))
	ret['status']=False
	ret['error']='Unknown error.'
	return HttpResponse(json.dumps(ret))

@login_required(login_url='/login/')
@csrf_exempt
def ajax_submit_comment(request):
	ret = {'status':True, 'error':None, 'data':None}
	if request.method=="POST":
		cmt = request.POST.get("comment")
		if cmt!="" and cmt!=None:
			cid = request.POST.get("cid")
			cid = check_cid(cid)
			if cid!=-1:
				content = ContentItems.objects.get(cid=cid)
				if content:
					newcomment = Comment.objects.create(uid=request.user, cid=content, cuid=content.uid, comment=cmt)
					newcomment.save()
					nc = { "username":request.user.username,
						"comment":cmt,
						# "commenttime":str(newcomment.commenttime)
						"commenttime":newcomment.commenttime.ctime()
						}
					# nc = serializers.serialize("json", [newcomment])
					ret['data']=nc
					return HttpResponse(json.dumps(ret))
		ret['status']=False
		ret['error']='提交评论失败!'
	return HttpResponse(json.dumps(ret))


@csrf_exempt
def ajax_comment(request):
	try:
		if request.method=="POST":
			cid = request.POST.get("cid")
			cid = check_cid(cid)
			if cid!=-1:
				comments = Comment.objects.filter(cid=cid).order_by('-commenttime')
				# comments = serializers.serialize("json",Comment.objects.filter(cid=cid).order_by('-commenttime'))
				return render(request, 'includes/comment.html', {'comments':comments})
	except:
		return "<div>无评论!</div>"


@csrf_exempt
def search(request):
    if request.method == 'POST':
        keyword = request.POST.get('k')
        contents = ContentItems.objects.filter(Q(content__icontains=keyword))
        print(comments)
        return render(request, 'includes/content.html', {'comments': content})