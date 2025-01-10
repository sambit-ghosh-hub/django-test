from celery import shared_task
from django.contrib.auth.models import User
from .models import Subscription
from time import sleep
from datetime import date

@shared_task
def message_on_sub(email):
 user=User.objects.get(email=email)
 sleep(2)
 print("Messaging user at: ", user.email,"You are Subscribed now")

@shared_task
def notify_subcription_end():
 today = date.today()
 subs_over = Subscription.objects.get(ends=today)
 for sub_over in subs_over:
  sleep(2)
  print("Messaging user at: ", sub_over.owner.email,"Your subscription ends today")