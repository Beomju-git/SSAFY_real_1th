from django.urls import path, include
from . import views

app_name='exchange'
urlpatterns = [
    path('', views.exchanges, name = 'exchanges'),
    path('update/', views.update, name='update')
]