from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import APIException


class AccountAlreadyExists(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = f'An account with that email already exists. Contact {settings.HELP_DESK_EMAIL} for assistance.'
    default_code = 'conflict'
