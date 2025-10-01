from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Story, StoryLike, StoryComment, Pitch, Donation, DonationContribution, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'bio', 'location', 'profile_pic', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'first_name', 'last_name', 'role', 'bio', 'location']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include username and password')
        
        return attrs


class StoryCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = StoryComment
        fields = ['id', 'user', 'content', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class StoryLikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = StoryLike
        fields = ['id', 'user', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class StorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    comments = StoryCommentSerializer(many=True, read_only=True)
    likes = StoryLikeSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    is_liked_by_user = serializers.SerializerMethodField()
    
    class Meta:
        model = Story
        fields = ['id', 'user', 'content', 'image', 'video', 'created_at', 'updated_at', 
                 'comments', 'likes', 'likes_count', 'comments_count', 'is_liked_by_user']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def get_is_liked_by_user(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False


class StoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ['content', 'image', 'video']


class PitchSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    funding_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Pitch
        fields = ['id', 'user', 'title', 'description', 'pitch_file', 'funding_goal', 
                 'current_funding', 'funding_percentage', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'current_funding', 'created_at', 'updated_at']
    
    def get_funding_percentage(self, obj):
        if obj.funding_goal > 0:
            return round((obj.current_funding / obj.funding_goal) * 100, 2)
        return 0


class PitchCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pitch
        fields = ['title', 'description', 'pitch_file', 'funding_goal']


class DonationContributionSerializer(serializers.ModelSerializer):
    contributor = UserSerializer(read_only=True)
    
    class Meta:
        model = DonationContribution
        fields = ['id', 'contributor', 'amount', 'message', 'created_at']
        read_only_fields = ['id', 'contributor', 'created_at']


class DonationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    contributions = DonationContributionSerializer(many=True, read_only=True)
    funding_percentage = serializers.SerializerMethodField()
    is_expired = serializers.ReadOnlyField()
    
    class Meta:
        model = Donation
        fields = ['id', 'user', 'title', 'description', 'donation_type', 'target_goal', 
                 'current_amount', 'funding_percentage', 'deadline', 'is_active', 'is_expired',
                 'created_at', 'updated_at', 'contributions']
        read_only_fields = ['id', 'user', 'current_amount', 'created_at', 'updated_at']
    
    def get_funding_percentage(self, obj):
        if obj.target_goal > 0:
            return round((obj.current_amount / obj.target_goal) * 100, 2)
        return 0


class DonationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ['title', 'description', 'donation_type', 'target_goal', 'deadline']


class DonationContributeSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=15, decimal_places=2, min_value=0.01)
    message = serializers.CharField(required=False, allow_blank=True)


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp', 'read_status']
        read_only_fields = ['id', 'sender', 'timestamp']


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['receiver', 'content']
