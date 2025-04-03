from . import views
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import TweetViewSet
from rest_framework.authtoken.views import obtain_auth_token
router=DefaultRouter()
router.register(r'tweets', TweetViewSet)

urlpatterns = [
    path('', views.tweet_list, name='tweet_list'),
    path('create/', views.tweet_create, name='tweet_create'),
    path('<int:tweet_id>/edit/', views.tweet_edit, name='tweet_edit'),
    path('<int:tweet_id>/delete/', views.tweet_delete, name='tweet_delete'),
    path('register/', views.register, name='register'),
    path('api/',include(router.urls)),
    path('api/token/',obtain_auth_token, name='api_token_auth'),
]