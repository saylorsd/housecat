from django.conf import settings
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import BadRequest
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response

from accounts.models import UserProfile, User
from accounts.serializers import UserProfileRequestSerializer, UserProfileSerializer
from accounts.tokens import account_activation_token

REQUIRED_FIELDS = (
    'email',
    'category',
    'affiliation',
    'intended_use',
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
    user_fields = ['email', 'first_name', 'last_name', 'password']
    profile_params = {k: v for k, v in request.data.items() if k not in user_fields}
    user_email = request.data.get('email')
    password = request.data.get('password')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')

    user = User.objects.create_user(
        user_email,
        email=user_email,
        first_name=first_name,
        last_name=last_name,
        password=password
    )
    new_profile = UserProfile.objects.create(user=user, **profile_params)
    message = render_to_string('accounts/emails/request_alert.html', {
        'user': user,
    })
    try:
        send_mail(
            "New HouseCat account request",
            message,
            settings.DEFAULT_FROM_EMAIL,
            settings.ALERT_EMAILS
        )
    except Exception as e:
        print(e)
    return Response(
        UserProfileSerializer(new_profile).data,
        status=status.HTTP_201_CREATED
    )


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def approve_profile(request: Request):
    """ The view admins request to approve an account """
    user_email = request.data.get('user')
    try:
        # Update the user
        new_user = UserProfile.objects.get(user__username=user_email)
        # send email
        current_site = get_current_site(request)
        mail_subject = 'Your HouseCat account has been approved!'
        message = render_to_string('accounts/emails/account_activation.html', {
            'user': new_user.user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(new_user.user.pk)),
            'token': account_activation_token.make_token(new_user.user),
        })
        send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])

        new_user.approved = True
        new_user.save()
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


def activate(request, uidb64, token):
    """  The view the user requests when activating their approved profile. """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    print(user, token)
    print(account_activation_token.check_token(user, token))

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect(settings.LOGIN_REDIRECT_URL)
    return ''


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def check_login(request: Request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return Response({'details': 'not logged in'}, status=status.HTTP_403_FORBIDDEN)
    if profile.approved:
        return Response(UserProfileSerializer(profile).data)
    else:
        return Response({'details': 'not approved'}, status=status.HTTP_403_FORBIDDEN)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'user__username'

    def get_serializer_class(self, ):
        if self.request.method == 'POST':
            return UserProfileRequestSerializer

        return UserProfileSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = UserProfile.objects.all()
        approved: bool = self.request.query_params.get('approved') == 'true'
        if approved is not None:
            queryset = queryset.filter(approved=approved)
        return queryset
