from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'api'

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('auth/login/', views.UserLoginView.as_view(), name='user-login'),
    
    # Profile endpoints
    path('profile/<uuid:id>/', views.ProfileDetailView.as_view(), name='profile-detail'),
    
    # Story endpoints
    path('stories/', views.StoryListView.as_view(), name='story-list'),
    path('stories/<uuid:id>/', views.StoryDetailView.as_view(), name='story-detail'),
    path('stories/<uuid:id>/like/', views.StoryLikeView.as_view(), name='story-like'),
    path('stories/<uuid:id>/comment/', views.StoryCommentView.as_view(), name='story-comment'),
    
    # Pitch endpoints
    path('pitches/', views.PitchListView.as_view(), name='pitch-list'),
    path('pitches/<uuid:id>/', views.PitchDetailView.as_view(), name='pitch-detail'),
    
    # Donation endpoints
    path('donations/', views.DonationListView.as_view(), name='donation-list'),
    path('donations/<uuid:id>/', views.DonationDetailView.as_view(), name='donation-detail'),
    path('donations/<uuid:id>/contribute/', views.DonationContributeView.as_view(), name='donation-contribute'),
    
    # Message endpoints
    path('messages/', views.MessageListView.as_view(), name='message-list'),
    path('messages/<uuid:user_id>/', views.UserMessagesView.as_view(), name='user-messages'),
    path('messages/<uuid:id>/read/', views.MessageMarkReadView.as_view(), name='message-mark-read'),
]
