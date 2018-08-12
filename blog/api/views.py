from blog.models import (
	ContentItems, Comment, CaiZan
	)
from blog.api.serializers import (
	ContentItemsSerializer, CommentSerializer, CaiZanSerializer
	)
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


@api_view(['POST'])
def content_post(request, format=None):
	if request.method() == 'POST':
		serializer = ContentItemsSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.Http_201_CREATED)
		return Response(serializer.errors, status=status.Http_400_BAD_REQUEST)


class ContentItemDetailAPI(APIView):
	def get_object(self, pk):
		try:
			return ContentItems.objects.get(pk=pk)
		except DoseNotExist:
			return Http404()

	def delete(self, request, pk, format=None):
		content_item = self.get_object(pk)
		content_item.delete()
		return Response(status.Http_204_NO_CONTENT)


class CommentDetailAPI(APIView):
	def get_object(self, pk):
		try:
			return Comment.objects.get(pk=pk)
		except Snippet.DoseNotExist:
			raise Http404()

	def get(self, request, pk, format=None):
		comment = self.get_object(pk)
		serializer = CommentSerializer(comment)
		return Response(serializer.data)

	def put(self, request, pk, format=None):
		comment = self.get_object(pk)
		serializer = SnippetSerializer(comment, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.Http_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		comment = self.get_object(pk)
		comment.delete()
		return Response(status=status.Http_204_NO_CONTENT)



@api_view(['POST'])
def caizan_post(request, format=None):
	if request.method() == 'POST':
		caizan = CaiZanSerializer(request.data)
		if caizan.is_valid():
			caizan.save()
			return Response(caizan.data, status=status.Http_201_CREATED)
		return Response(caizan.errors, status=status.Http_400_BAD_REQUEST)


class CaiZanAPI(APIView):
	def get_object(self, pk):
		try:
			return CaiZan.objects.get(pk=pk)
		except DoseNotExist:
			raise Http404()

	def get(self, request, pk, format=None):
		caizan = self.get_object(pk)
		serializer = CaiZanSerializer(caizan, context={'request':request})
		return Response(serializer.data)

	# def delete(self, request, pk, format=None):
	# 	caizan = self.get_object(pk)
	# 	caizan.delete()
	# 	return Response(status=status.Http_204_NO_CONTENT)