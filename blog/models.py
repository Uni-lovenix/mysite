from django.db import models
from django.contrib import admin

class Users(models.Model):
	userid = models.AutoField(primary_key=True)
	username = models.CharField(max_length=60)
	heading = models.ImageField(upload_to='img', default='img/4.jpg')
	sex = models.BooleanField(default=False)
	phonenumber = models.CharField(max_length=11)
	email = models.EmailField()
	password = models.CharField(max_length=64)
	createtime = models.DateTimeField(auto_now_add=True)
	isactivity = models.BooleanField(default=False)

class ContentItems(models.Model):
	cid = models.AutoField(primary_key=True)
	userid = models.ForeignKey(Users, on_delete=False, related_name='users_contentItems')
	posttime = models.DateTimeField(auto_now_add=True)
	postposition = models.CharField(max_length=90)
	content = models.TextField()
	picture = models.ImageField(upload_to='Content_img', default=None)
	cai = models.IntegerField(default=0)
	isshowname = models.BooleanField(default=True)

class ContentItemsAdmin(admin.ModelAdmin):
	list_display = ('userid', 'content', 'isshowname', 'posttime')

admin.site.register(ContentItems, ContentItemsAdmin)