from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User


class ContentItems(models.Model):
	cid = models.AutoField(primary_key=True)
	uid = models.ForeignKey(User, on_delete=False, related_name='auth_user_contentItems')
	posttime = models.DateTimeField(auto_now_add=True)
	postposition = models.CharField(max_length=90, default='')
	content = models.TextField()
	picture = models.ImageField(upload_to='Content_img', default=None)
	cai = models.IntegerField(default=0)
	isshowname = models.BooleanField(default=True)

class ContentItemsAdmin(admin.ModelAdmin):
	list_display = ('uid', 'content', 'isshowname', 'posttime')

admin.site.register(ContentItems, ContentItemsAdmin)