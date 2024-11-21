from django.shortcuts import render
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer, UserChangeSerializer
from rest_framework.decorators import api_view
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import status
# Create your views here.
from rest_framework.decorators import authentication_classes
from rest_framework.authentication import TokenAuthentication, BasicAuthentication


@api_view(["GET", "PUT"])
@authentication_classes([TokenAuthentication, BasicAuthentication])
def profile(request,user_id):
    user = User.objects.get(pk=user_id)
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    elif request.method =='PUT':
        serializer = UserChangeSerializer(user,data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            return Response(serializer.data)

@api_view(["GET", "PUT"])
@authentication_classes([TokenAuthentication, BasicAuthentication])
def signout(request):
    request.user.delete()
    return Response({'message': '회원탈퇴'})

