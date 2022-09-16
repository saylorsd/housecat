from django.core.exceptions import BadRequest
from django.db import IntegrityError
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response

from accounts.exceptions import AccountAlreadyExists
from accounts.models import UserProfile, User
from accounts.serializers import UserProfileBriefSerializer, UserProfileRequestSerializer, UserProfileSerializer

REQUIRED_FIELDS = (
    'email',
    'category',
    'affiliation',
    'intended_use',
    'expected_account_tenure',
    'conflicts',
    'agreed_to_terms',
)


def validate_new_profile_request(request: Request):
    missing_fields = []
    for field in REQUIRED_FIELDS:
        if field not in request.data:
            missing_fields.append(field)
    if missing_fields:
        raise BadRequest(f'Missing the following fields {missing_fields}')


@api_view(['POST'])
def request_new_profile(request: Request):
    """ Handle submission of account request form data """
    validate_new_profile_request(request)  # will raise a BadRequest error for invalid requests

    profile_params = {k: v for k, v in request.data.items() if k != 'email'}
    user_email = request.data.get('email')

    try:
        user = User.objects.create_user(user_email, email=user_email)
        new_profile = UserProfile.objects.create(user=user, **profile_params)
        return Response(
            UserProfileSerializer(new_profile).data,
            status=status.HTTP_201_CREATED
        )

    except IntegrityError:
        raise AccountAlreadyExists()


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def approve_profile(request: Request):
    user_email = request.data.get('user')
    try:
        new_user = UserProfile.objects.get(user__username=user_email)
        new_user.approved = True
        new_user.save()
        new_user.user.is_active = True
        new_user.user.save()
        return Response(UserProfileSerializer(new_user).data)
    except UserProfile.DoesNotExist:
        raise BadRequest(f'Request for {user_email} was not found.')


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def revoke_profile(request: Request):
    user_email = request.data.get('user')
    try:
        profile = UserProfile.objects.get(user__username=user_email)
        profile.approved = False
        profile.save()
        profile.user.is_active = False
        profile.user.save()
        return Response(UserProfileSerializer(profile).data)
    except UserProfile.DoesNotExist:
        raise BadRequest(f'Account for {user_email} was not found.')


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    lookup_field = 'user__username'

    def get_serializer_class(self, ):
        if self.request.method == 'POST':
            return UserProfileRequestSerializer

        return UserProfileSerializer
