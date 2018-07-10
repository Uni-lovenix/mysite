from __future__ import unicode_literals
from django.contrib import admin
from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=60)
    sex = models.BooleanField(default=False)
    phonenumber = models.CharField(max_length=11)
    email = models.EmailField()
    password = models.CharField(max_length=64)
    createtime = models.DateTimeField(auto_now_add=True)

class UserAdmin(admin.ModelAdmin):
    list_display = ('username','password','email', 'sex', 'phonenumber', 'createtime')

admin.site.register(User,UserAdmin)