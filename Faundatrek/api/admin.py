from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Story, StoryLike, StoryComment, Pitch, Donation, DonationContribution, Message


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'is_active', 'created_at']
    list_filter = ['role', 'is_active', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    fieldsets = UserAdmin.fieldsets + (
        ('FaundaTrek Profile', {'fields': ('role', 'bio', 'location', 'profile_pic')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('FaundaTrek Profile', {'fields': ('role', 'bio', 'location')}),
    )


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'content_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'user__username']
    ordering = ['-created_at']
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content Preview'


@admin.register(StoryLike)
class StoryLikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'story', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['story__content', 'user__username']


@admin.register(StoryComment)
class StoryCommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'story', 'user', 'content_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'user__username', 'story__content']
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content Preview'


@admin.register(Pitch)
class PitchAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'funding_goal', 'current_funding', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description', 'user__username']
    ordering = ['-created_at']


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'donation_type', 'target_goal', 'current_amount', 'deadline', 'is_active']
    list_filter = ['donation_type', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'user__username']
    ordering = ['-created_at']


@admin.register(DonationContribution)
class DonationContributionAdmin(admin.ModelAdmin):
    list_display = ['id', 'donation', 'contributor', 'amount', 'created_at']
    list_filter = ['created_at']
    search_fields = ['donation__title', 'contributor__username']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'receiver', 'content_preview', 'timestamp', 'read_status']
    list_filter = ['read_status', 'timestamp']
    search_fields = ['content', 'sender__username', 'receiver__username']
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content Preview'
