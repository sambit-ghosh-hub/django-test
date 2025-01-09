from rest_framework import serializers

from .models import BookModel


class BookSerializer(serializers.HyperlinkedModelSerializer):
 class Meta:
  model = BookModel
  fields = ('title','description')
