from django.contrib.auth.tokens import PasswordResetTokenGenerator

from accounts.models import User


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user: User, timestamp):
        return f'{user.pk}{timestamp}{user.username}'


account_activation_token = AccountActivationTokenGenerator()
