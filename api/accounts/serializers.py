from rest_framework import serializers

from accounts.models import UserProfile, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'date_joined',
        )


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = (
            'id',
            'user',
            'category',
            'affiliation',
            'intended_use',
            'conflicts',
            'expiration_date',
            'agreed_to_terms',
            'approved',
        )


class UserProfileBriefSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = (
            'id',
            'user',
            'category',
            'approved',
        )


class UserProfileRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'category',
            'affiliation',
            'intended_use',
            'conflicts',
            'agreed_to_terms',
        )

