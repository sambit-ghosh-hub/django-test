from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, SubscriptionSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from .tasks import message_on_sub

def members_index(request):
 template=loader.get_template('memberspage.html')
 return HttpResponse(template.render())

@api_view(['POST'])
def login(request):
 user=get_object_or_404(User,username=request.data['username'])
 if not user.check_password(request.data['password']):
  return Response({"detail":"Not found."},status=status.HTTP_404_NOT_FOUND)
 token, created = Token.objects.get_or_create(user=user)
 serializer=UserSerializer(instance=user)
 return Response({'token':token.key,'user':serializer.data},status=status.HTTP_200_OK)

@api_view(['POST'])
def signup(request):
 serializer=UserSerializer(data=request.data)
 if serializer.is_valid():
  serializer.save()
  user=User.objects.get(username=request.data['username'])
  user.set_password(request.data['password'])
  user.save()
  token = Token.objects.create(user=user)
  return Response({'token':token.key,'user':serializer.data},status=status.HTTP_201_CREATED)
 return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
 return Response({"message":'success',"user":request.user.email},status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_subscription(request):
 data = {
  "start" : request.data['start'],
  "end" : request.data['end'],
  "owner" : request.user.id,
 }
 serializer=SubscriptionSerializer(data = data)
 if serializer.is_valid():
  serializer.save()
  message_on_sub.delay(request.user.email)
  return Response({"message":"Started sending messages"},status=status.HTTP_200_OK)
 return Response({"message":"Bad Request","error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)