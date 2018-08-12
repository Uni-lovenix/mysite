from django.contrib.auth.models import User
from blog.models import (
	ContentItems, CaiZan, Comment
	)
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username', 'email')

class ContentItemsSerializer(serializers.ModelSerializer):
	uid = serializers.PrimaryKeyRelatedField(read_only=True)
	class Meta:
		model = ContentItems
		fields = ('cid', 'uid', 'posttime', 'content', 'cai')


class CaiZanSerializer(serializers.ModelSerializer):
	uid = serializers.PrimaryKeyRelatedField(read_only=True)
	cid = serializers.PrimaryKeyRelatedField(read_only=True)
	class Meta:
		model = CaiZan
		fields = ('uid', 'cid')


class CommentSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Comment
		fields = ('uid', 'cid', 'cuid', 'comment', 'commenttime', 'isshowname')
