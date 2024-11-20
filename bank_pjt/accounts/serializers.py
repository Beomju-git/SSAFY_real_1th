from rest_framework import serializers
from .models import User
from articles.models import Comment, Article

class UserSerializer(serializers.ModelSerializer):
    class UserArticleSerialzier(serializers.ModelSerializer):
        class Meta:
            model = Article
            fields = ('id','title',)
    # 작성한 글 목록
    article_set = UserArticleSerialzier(read_only= True, many=True)
    # 좋아요 싫어요 누른 글 목록 
    likes_articles = UserArticleSerialzier(read_only= True, many=True)
    dislikes_articles = UserArticleSerialzier(read_only= True, many=True)

    class CommentArticleSerialzier(serializers.ModelSerializer):
        class Meta:
            model = Comment
            fields = ('id',)
    # 작성한 댓글 목록
    comment_set = CommentArticleSerialzier(read_only= True, many=True)
    # 좋아요 싫어요 누른 댓글 목록 
    likes_comments = CommentArticleSerialzier(read_only= True, many=True)
    dislikes_comments = CommentArticleSerialzier(read_only= True, many=True)    

    class Meta:
        model = User
        fields=(
            'username', 'first_name', 'last_name',
            'email','phone_number','address','birth_date','major_bank',
            'article_set',
            'likes_articles','dislikes_articles','likes_comments','dislikes_comments',
            'comment_set',
                )
        # fields='__all__'

class UserChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model =User
        fields=('email','phone_number','address','birth_date','major_bank',)
        read_only_fields = ('username', 'first_name', 'last_name','article_set','likes_articles','dislikes_articles','likes_comments','dislikes_comments',)