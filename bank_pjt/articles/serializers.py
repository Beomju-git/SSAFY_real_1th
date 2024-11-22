from rest_framework import serializers
from .models import Article, Comment
from accounts.models import User


# 게시글 전체 목록 조회 
class ArticleListSerializer(serializers.ModelSerializer):
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model =User
            fields =('id', 'username',)
    author = UserSerializer()
    class Meta:
        model = Article
        #  게시물 조회 시 게시물 모든 정보 던지기
        fields = '__all__'

#게시글 생성, 수정, 조회
# 생성 시 게시글  좋아요, 싫어요 수정 x 읽기만 가능
class ArticleCreateSerializer(serializers.ModelSerializer):
    # 단일 게시글 조회 시, 게시물에 달린 댓글 조회
    class ArticleCommentSerializer(serializers.ModelSerializer):
        class UserSerializer(serializers.ModelSerializer):
            class Meta:
                model=User
                fields =('username', 'id',)
        user = UserSerializer()
        class Meta:
            model = Comment
            fields = '__all__'
    comment_set = ArticleCommentSerializer(read_only= True, many=True)
    class UserInfoSerialzier(serializers.ModelSerializer):
        class Meta:
            model = User
            fields =('username', 'id',)
    author =    UserInfoSerialzier()
    
    # 단일 게시글 조회 시 좋아요, 싫어요 개수 출력
    liked_count = serializers.IntegerField(source='liked_users.count', read_only=True)
    disliked_count = serializers.IntegerField(source='disliked_users.count', read_only=True)
    class Meta:
        model = Article
        # 필드 순서 조정하기
        fields = ['id', 'title', 'description', 'created_at', 'image', 'author', 'liked_users', 'liked_count','disliked_users', 'disliked_count','comment_set']
        read_only_fields=('author','liked_users','disliked_users',)



# 댓글 전체 조회
class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields= '__all__'



# 댓글 생성, 수정, 조회
class CommentCreateSerializer(serializers.ModelSerializer):
    # 단일 게시글 조회 시 좋아요, 싫어요 개수 출력
    # liked_count = serializers.IntegerField(source='liked_users.count', read_only=True)
    # disliked_count = serializers.IntegerField(source='disliked_users.count', read_only=True)    

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields=('user','article','liked_users','disliked_users',)