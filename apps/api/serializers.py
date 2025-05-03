from rest_framework import serializers
from apps.users.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the User model.
    """
    
    class Meta:
        model = User
        fields = ['url', 'email', 'first_name', 'last_name', 'is_staff']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        """
        Create and return a new user.
        """
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
    
    def update(self, instance, validated_data):
        """
        Update and return an existing user.
        """
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user 