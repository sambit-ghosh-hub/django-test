from django.urls import path
from . import views

urlpatterns = [
 path('members/',views.members_index, name='members'),
 path('api/login/', views.login),
 path('api/signup/', views.signup),
 path('api/test_token/', views.test_token),
]