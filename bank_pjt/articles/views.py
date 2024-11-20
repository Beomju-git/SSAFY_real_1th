from django.shortcuts import render
from .models import Article, Comment
from .serializers import ArticleListSerializer, ArticleCreateSerializer
from .serializers import CommentCreateSerializer ,CommentListSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import status

# 회원가입을 위해
from rest_framework.decorators import authentication_classes
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
# Create your views here.

#  전체 게시물 조회 및 게시물 생성
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication, BasicAuthentication])
def articles(request):
    if request.method =='GET':
        # get_list_obect 써야되나
        # articles= get_list_or_404(Article)
        articles = Article.objects.all()
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)
    elif request.method=='POST':
        serializer=ArticleCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# 단일 게시물 조회, 수정, 삭제
# 단딜 게시물 조회 시 댓글 목록, 좋아요 수 도 함께 JSon으로 보내줌
@api_view(['GET','PUT','DELETE'])
@authentication_classes([TokenAuthentication, BasicAuthentication])
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method =='GET':
        serializer = ArticleCreateSerializer(article)
        return Response(serializer.data)
    elif request.method =='PUT':
        serializer = ArticleCreateSerializer(article, data=request.  data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            return Response(serializer.data)
    elif request.method =='DELETE':
        article.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
    
# 전체 댓글 조회(게시글과 상관없이 모든 댓글) + 댓글 생성
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication, BasicAuthentication])
def comments(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    if request.method =='GET':
        # get_list_obect 써야되나
        # articles= get_list_or_404(Article)
        comments = Comment.objects.all()
        serializer = CommentListSerializer(comments, many=True)
        return Response(serializer.data)
    elif request.method=='POST':
        serializer=CommentCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, article=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

# 단일 댓글 조회, 수정, 삭제제
@api_view(['GET','PUT','DELETE'])
@authentication_classes([TokenAuthentication, BasicAuthentication])
def comment_detail(request,article_pk,comments_pk):
    comment = get_object_or_404(Comment, pk=comments_pk)
    article = get_object_or_404(Article, pk = article_pk)
    if request.method =='GET':
        serializer = CommentCreateSerializer(comment)
        return Response(serializer.data)
    elif request.method =='PUT':
        serializer = CommentCreateSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    elif request.method =='DELETE':
        comment.delete()
        return Response(status=status.HTTP_202_ACCEPTED)

# 게시물 좋아요 누르기
@api_view(['POST'])
@authentication_classes([TokenAuthentication, BasicAuthentication])    
def article_like(request,article_pk):
    article = get_object_or_404(Article, pk= article_pk)
    if request.user in article.liked_users.all():
        article.liked_users.remove(request.user)
        return Response({'message': '게시글 좋아요 취소'}, status=status.HTTP_200_OK)
    else:
        article.liked_users.add(request.user)
        return Response({'message': '게시글 좋아요 추가'}, status=status.HTTP_201_CREATED)

# 게시물 싫어요 누르기
@api_view(['POST'])
@authentication_classes([TokenAuthentication, BasicAuthentication])    
def article_dislike(request,article_pk):
    article = get_object_or_404(Article, pk= article_pk)
    if request.user in article.disliked_users.all():
        article.disliked_users.remove(request.user)
        return Response({'message': '게시글 싫어요 취소'}, status=status.HTTP_200_OK)
    else:
        article.disliked_users.add(request.user)
        return Response({'message': '게시글 싫어요 추가'}, status=status.HTTP_201_CREATED)    
    

# 댓글 좋아요 누르기
@api_view(['POST'])
@authentication_classes([TokenAuthentication, BasicAuthentication])    
def comment_like(request,article_pk,comments_pk):
    comment = get_object_or_404(Comment, pk= comments_pk)
    if request.user in comment.liked_users.all():
        comment.liked_users.remove(request.user)
        return Response({'message': '댓글 좋아요 취소'}, status=status.HTTP_200_OK)
    else:
        comment.liked_users.add(request.user)
        return Response({'message': '댓글 좋아요 추가'}, status=status.HTTP_201_CREATED)

# 댓글 싫어요 누르기
@api_view(['POST'])
@authentication_classes([TokenAuthentication, BasicAuthentication])    
def comment_dislike(request,article_pk,comments_pk):
    comment = get_object_or_404(Comment, pk= comments_pk)
    if request.user in comment.disliked_users.all():
        comment.disliked_users.remove(request.user)
        return Response({'message': '댓글 싫어요 취소'}, status=status.HTTP_200_OK)
    else:
        comment.disliked_users.add(request.user)
        return Response({'message': '댓글 싫어요 추가'}, status=status.HTTP_201_CREATED)    
    