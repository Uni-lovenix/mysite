from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
import django.utils.timezone as timezone


class ContentItems(models.Model):
    cid = models.AutoField(primary_key=True)
    uid = models.ForeignKey(User,
                            on_delete=models.CASCADE,
                            related_name='auth_user_contentItems')
    posttime = models.DateTimeField(default=timezone.now)
    postposition = models.CharField(max_length=90, default='')
    content = models.TextField()
    picture = models.ImageField(upload_to='Content_img', default=None)
    cai = models.IntegerField(default=0)
    isshowname = models.BooleanField(default=True)


class CaiZan(models.Model):
    uid = models.ForeignKey(User,
                            on_delete=models.CASCADE,
                            related_name='auth_user_caizan')
    cid = models.ForeignKey(ContentItems,
                            on_delete=models.CASCADE,
                            related_name='contentitems_caizan')


class Comment(models.Model):
    uid = models.ForeignKey(User,
                            on_delete=models.CASCADE,
                            related_name='auth_user_comment')
    cid = models.ForeignKey(ContentItems,
                            on_delete=models.CASCADE,
                            related_name='contentitems_comment')
    cuid = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='auth_user_comment_cuid')
    comment = models.TextField()
    commenttime = models.DateTimeField(default=timezone.now)
    isshowname = models.BooleanField(default=True)


class ContentItemsAdmin(admin.ModelAdmin):
    list_display = ('uid', 'content', 'isshowname', 'posttime', 'cai')


class CaiZanAdmin(admin.ModelAdmin):
    list_display = ('uid', 'cid')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('uid', 'cid', 'cuid', 'comment', 'commenttime',
                    'isshowname')


admin.site.register(ContentItems, ContentItemsAdmin)
admin.site.register(CaiZan, CaiZanAdmin)
admin.site.register(Comment, CommentAdmin)