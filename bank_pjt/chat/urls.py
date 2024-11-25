# finance/urls.py

from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('recommend/', views.chat_recommend, name='chat_recommend'),
    path('standardize/', views.run_standardization_view, name='chat_standardize'),
]
