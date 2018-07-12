from django.db import models
from django.contrib import admin

class Users(models.Model):
	userid = models.AutoField(primary_key=True)
	username = models.CharField(max_length=60)
	sex = models.BooleanField(default=False)
	phonenumber = models.CharField(max_length=11)
	email = models.EmailField()
	password = models.CharField(max_length=64)
	createtime = models.DateTimeField(auto_now_add=True)


class BlogPost(models.Model):
	title = models.CharField(max_length=150)
	body = models.TextField()
	timestamp = models.DateTimeField()

class BlogPostAdmin(admin.ModelAdmin):
	list_display = ('title', 'timestamp')


admin.site.register(BlogPost, BlogPostAdmin)