from ..models import Notification
from rest_framework import serializers
from profiles.models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            'title',
            'logo',
        )
        extra_kwargs = {
            "title": {"read_only": True},
            "logo": {"read_only": True},
        }

    def validate(self, attrs):
        user = self.context.get("user")
        if not Notification.objects.filter(user=user, is_read=False).exists():
            raise serializers.ValidationError({"error": "Oxunmamis mesajlar yoxdur"})
        return super().validate(attrs)


class ProfileDashboardSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Profile
        fields = (
            "background_image",
            "profile_photo",
            "fullname",
        )


class ProfileViewCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "profile_viewed_count",
        )
