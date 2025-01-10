from django.db import models
from django.contrib.auth.models import User

class Subscription(models.Model):
 start = models.DateField()
 end = models.DateField()
 owner = models.ForeignKey(User, on_delete=models.CASCADE)
