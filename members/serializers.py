from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Subscription

class UserSerializer(serializers.ModelSerializer):
 class Meta(object):
  model=User
  fields = ['id','username','email','password']

class SubscriptionSerializer(serializers.ModelSerializer):
 class Meta(object):
  model=Subscription
  fields = ['id','start','end','owner']