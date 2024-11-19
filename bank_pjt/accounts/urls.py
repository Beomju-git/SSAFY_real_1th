from django.urls import path
from . import views
app_name ='accounts'

urlpatterns = [
    path('<int:user_id>/detail/', views.profile, name='profile'),
    path('', views.signout, name='signout'),
]
