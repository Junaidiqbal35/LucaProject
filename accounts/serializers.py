from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Permission
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'groups', 'permissions']

    def get_groups(self, user):
        return [group.name for group in user.groups.all()]

    def get_permissions(self, user):
        permissions = Permission.objects.filter(group__user=user).distinct()
        return [perm.codename for perm in permissions]


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(error_messages={'required': 'Username is required'})
    password = serializers.CharField(error_messages={'required': 'Password is required'})

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username:
            raise serializers.ValidationError({"username": "Username is required."})
        if not password:
            raise serializers.ValidationError({"password": "Password is required."})

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError({"non_field_errors": "Invalid username or password."})

        if not user.is_active:
            raise serializers.ValidationError({"non_field_errors": "User account is disabled."})

        return user
