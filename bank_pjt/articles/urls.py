from django.urls import path
from . import views
app_name ='articles'

urlpatterns = [
    # 게시물 생성 및 전체 게시물 조회
    path('', views.articles, name='articles'),
    # 단일 게시물 조회(댓글 목록, 좋아요 수, 싫어요 수), 삭제 및 수정
    path('<int:article_pk>/', views.article_detail, name='article_detail'),
    # 게시물과 상관없는 댓글 전체 조회(필요할까?) + 단일 게시물에 해당하는 생성
    path('<int:article_pk>/comments/', views.comments, name='comments'),
    # article에 작성된 단일 댓글 수정 삭제
    path('<int:article_pk>/comments/<int:comments_pk>/', views.comment_detail, name='comment_detail'),
    #artilce 좋아요
    path('<int:article_pk>/like/', views.article_like, name='article_like'),
    #artilce 싫어요
    path('<int:article_pk>/dislike/', views.article_dislike, name='article_dislike'),
    #댓글 좋아요
    path('<int:article_pk>/comments/<int:comments_pk>/like/', views.comment_like, name='comment_like'),
    #댓글 싫어요
    path('<int:article_pk>/comments/<int:comments_pk>/dislike/', views.comment_dislike, name='comment_dislike'),

]
