from rest_framework import serializers
from .models import User
from articles.models import Comment, Article
from products.models import TermDeposit, TermDepositOptions

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
    
    class ZZimProdcutSerialzier(serializers.ModelSerializer):
        class ZZimProductOptionSerializer(serializers.ModelSerializer):
            class Meta:
                model = TermDepositOptions
                fields = '__all__'
        termdepositoptions_set = ZZimProductOptionSerializer(read_only= True, many=True)
                
        class Meta:
            model = TermDeposit
            fields = ('fin_prdt_cd', 'kor_co_nm', 'fin_prdt_nm','termdepositoptions_set',)
            
            
    zzim_product = ZZimProdcutSerialzier(read_only= True, many=True)

    class Meta:
        model = User
        fields=(
            'username', 'first_name', 'last_name',
            'email','phone_number','address','birth_date','major_bank',
            'article_set',
            'likes_articles','dislikes_articles','likes_comments','dislikes_comments',
            'comment_set', 'zzim_product',
                )
        # fields='__all__'

class UserChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model =User
        fields=('email','phone_number','address','birth_date','major_bank',)
        read_only_fields = ('username', 'first_name', 'last_name','article_set','likes_articles','dislikes_articles','likes_comments','dislikes_comments',)