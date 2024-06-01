from rest_framework import serializers
from .models import CustomUser, FriendRequest

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ('password', 'last_login', 'groups' ,'user_permissions')

# users/serializers.py


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'status']
        read_only_fields = ['from_user', 'status']

    def validate_to_user(self, value):
        request = self.context.get('request')

        if FriendRequest.objects.filter(from_user=request.user, to_user=value).exists():
            raise serializers.ValidationError("Friend request already sent")

        if value==request.user:
            raise serializers.ValidationError("You can not send Friend request to yourself")

        return value