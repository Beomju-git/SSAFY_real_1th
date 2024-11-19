from django.db import models
from django.conf import settings
# Create your models here.

class Article(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    liked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes_articles')
    disliked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='dislikes_articles')
    title = models.CharField(max_length=100)
    description= models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    image= models.ImageField(null=True)
    

class Comment(models.Model):
    article =models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    liked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes_comments')
    disliked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='dislikes_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
