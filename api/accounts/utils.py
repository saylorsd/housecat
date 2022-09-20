import typing

from django.core.mail import send_mail

if typing.TYPE_CHECKING:
    from accounts.models import UserProfile


def finalize_account(account: UserProfile):
    # create password for account
    pass
