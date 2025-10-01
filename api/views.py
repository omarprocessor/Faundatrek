from rest_framework import status, generics, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Story, StoryLike, StoryComment, Pitch, Donation, DonationContribution, Message
from .serializers import (
    UserSerializer, UserRegistrationSerializer, UserLoginSerializer,
    StorySerializer, StoryCreateSerializer, StoryCommentSerializer,
    PitchSerializer, PitchCreateSerializer,
    DonationSerializer, DonationCreateSerializer, DonationContributeSerializer,
    MessageSerializer, MessageCreateSerializer
)


# Authentication Views
class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Profile Views
class ProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'
    
    def get_object(self):
        obj = get_object_or_404(User, id=self.kwargs['id'])
        return obj


# Story Views
class StoryListView(generics.ListCreateAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['content', 'user__username']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return StoryCreateSerializer
        return StorySerializer
    
    def perform_create(self, serializer):
        # For now, create with a default user (first user in system)
        default_user = User.objects.first()
        if default_user:
            serializer.save(user=default_user)
        else:
            # Create a default user if none exists
            default_user = User.objects.create_user(
                username='default_user',
                email='default@example.com',
                password='defaultpass123',
                role='entrepreneur'
            )
            serializer.save(user=default_user)


class StoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return StoryCreateSerializer
        return StorySerializer


class StoryLikeView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, id):
        story = get_object_or_404(Story, id=id)
        
        # For now, use a default user for likes
        default_user = User.objects.first()
        if not default_user:
            default_user = User.objects.create_user(
                username='default_user',
                email='default@example.com',
                password='defaultpass123',
                role='entrepreneur'
            )
        
        like, created = StoryLike.objects.get_or_create(story=story, user=default_user)
        
        if not created:
            like.delete()
            return Response({'message': 'Like removed'}, status=status.HTTP_200_OK)
        
        return Response({'message': 'Story liked'}, status=status.HTTP_201_CREATED)


class StoryCommentView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, id):
        story = get_object_or_404(Story, id=id)
        serializer = StoryCommentSerializer(data=request.data)
        
        if serializer.is_valid():
            # For now, use a default user for comments
            default_user = User.objects.first()
            if not default_user:
                default_user = User.objects.create_user(
                    username='default_user',
                    email='default@example.com',
                    password='defaultpass123',
                    role='entrepreneur'
                )
            
            serializer.save(story=story, user=default_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Pitch Views
class PitchListView(generics.ListCreateAPIView):
    queryset = Pitch.objects.filter(is_active=True)
    serializer_class = PitchSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'user__username']
    ordering_fields = ['created_at', 'funding_goal', 'current_funding']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PitchCreateSerializer
        return PitchSerializer
    
    def perform_create(self, serializer):
        # For now, create with a default user
        default_user = User.objects.first()
        if default_user:
            serializer.save(user=default_user)
        else:
            # Create a default user if none exists
            default_user = User.objects.create_user(
                username='default_user',
                email='default@example.com',
                password='defaultpass123',
                role='entrepreneur'
            )
            serializer.save(user=default_user)


class PitchDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pitch.objects.all()
    serializer_class = PitchSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PitchCreateSerializer
        return PitchSerializer


# Donation Views
class DonationListView(generics.ListCreateAPIView):
    queryset = Donation.objects.filter(is_active=True)
    serializer_class = DonationSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'user__username']
    ordering_fields = ['created_at', 'target_goal', 'deadline']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DonationCreateSerializer
        return DonationSerializer
    
    def perform_create(self, serializer):
        # For now, create with a default user
        default_user = User.objects.first()
        if default_user:
            serializer.save(user=default_user)
        else:
            # Create a default user if none exists
            default_user = User.objects.create_user(
                username='default_user',
                email='default@example.com',
                password='defaultpass123',
                role='entrepreneur'
            )
            serializer.save(user=default_user)


class DonationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return DonationCreateSerializer
        return DonationSerializer


class DonationContributeView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, id):
        donation = get_object_or_404(Donation, id=id)
        
        if donation.is_expired:
            return Response({'error': 'Donation deadline has passed'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = DonationContributeSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            message = serializer.validated_data.get('message', '')
            
            # For now, use a default user for contributions
            default_user = User.objects.first()
            if not default_user:
                default_user = User.objects.create_user(
                    username='default_user',
                    email='default@example.com',
                    password='defaultpass123',
                    role='entrepreneur'
                )
            
            # Create contribution
            DonationContribution.objects.create(
                donation=donation,
                contributor=default_user,
                amount=amount,
                message=message
            )
            
            # Update donation current amount
            donation.current_amount += amount
            donation.save()
            
            return Response({'message': 'Contribution successful'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Message Views
class MessageListView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        # For now, return all messages
        return Message.objects.all().order_by('-timestamp')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MessageCreateSerializer
        return MessageSerializer
    
    def perform_create(self, serializer):
        # For now, use a default user as sender
        default_user = User.objects.first()
        if default_user:
            serializer.save(sender=default_user)
        else:
            # Create a default user if none exists
            default_user = User.objects.create_user(
                username='default_user',
                email='default@example.com',
                password='defaultpass123',
                role='entrepreneur'
            )
            serializer.save(sender=default_user)


class UserMessagesView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        # For now, return all messages
        return Message.objects.all().order_by('timestamp')


class MessageMarkReadView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, id):
        message = get_object_or_404(Message, id=id)
        message.read_status = True
        message.save()
        return Response({'message': 'Message marked as read'}, status=status.HTTP_200_OK)
