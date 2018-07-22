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
	# zan = models.IntegerField(default=0)
	cai = models.IntegerField(default=0)
	isshowname = models.BooleanField(default=True)

class CaiZan(models.Model):
	uid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auth_user_caizan')
	cid = models.ForeignKey(ContentItems, on_delete=models.CASCADE, related_name='contentitems_caizan')

class ContentItemsAdmin(admin.ModelAdmin):
	list_display = ('uid', 'content', 'isshowname', 'posttime','cai')

class CaiZanAdmin(admin.ModelAdmin):
	list_display = ('uid', 'cid')

admin.site.register(ContentItems, ContentItemsAdmin)
admin.site.register(CaiZan, )