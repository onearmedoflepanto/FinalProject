from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.shortcuts import get_object_or_404, get_list_or_404
from .serializers import CommentSerializer
from .models import Comment
from stocks.models import StockDetail

# Create your views here.

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_comments(request, name):
    stock = get_object_or_404(StockDetail, name=name)

    if request.method == 'GET':
        comments = Comment.objects.filter(stock=stock)
        serializer = CommentSerializer(comments, many=True, context={'request' : request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data, context={'request' : request})
        if serializer.is_valid():
            serializer.save(user=request.user, stock=stock)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)