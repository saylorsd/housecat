from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITransactionTestCase

from accounts.models import UserProfile, User


class UserProfileTests(APITransactionTestCase):
    request_url = reverse('request_new_profile')
    request_data = {
        "email": "test@wprdc.edu",
        "category": "ADMIN",
        "affiliation": "WPRDC",
        "intended_use": "Testing stuff.",
        "expected_account_tenure": "24",
        "conflicts": "Investments in the testing industry.",
        "agreed_to_terms": True
    }
    request_dup_data = {
        "email": "test@wprdc.edu",
        "category": "BAD",
        "affiliation": "WPRDC",
        "intended_use": "Testing stuff.",
        "expected_account_tenure": "24",
        "conflicts": "Investments in the testing industry.",
        "agreed_to_terms": True
    }

    regular_user = None
    staff_user = None

    approve_url = reverse('approve_profile')
    revoke_url = reverse('revoke_profile')

    def setUp(self) -> None:
        self.regular_user = User.objects.create_user(username='regular', password='tH3@ssW0rd!')
        self.staff_user = User.objects.create_user(username='staff', password='tH3@ssW0rd!')
        self.staff_user.is_staff = True
        self.staff_user.save()

    def test_request_new_profile(self):
        """
        Ensure we can create a new UserProfile.
        """
        response = self.client.post(self.request_url, self.request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserProfile.objects.count(), 1)
        self.assertEqual(UserProfile.objects.get().user.email, 'test@wprdc.edu')

    def test_duplicate_request_new_profile(self):
        """
        Ensure duplicate new account requests are properly handled
        """
        self.client.post(self.request_url, self.request_data, format='json')
        duplicate_response = self.client.post(self.request_url, self.request_dup_data, format='json')
        self.assertEqual(duplicate_response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(UserProfile.objects.count(), 1)
        self.assertEqual(UserProfile.objects.get().user.email, 'test@wprdc.edu')
        # test that the record wasn't overwritten anyway
        self.assertEqual(UserProfile.objects.get().category, 'ADMIN')

    def test_approve_profile(self):
        """
        Ensures staff, and only staff, can approve accounts
        """
        response = self.client.post(self.request_url, self.request_data, format='json')

        # first without permissions
        self.client.post(self.approve_url, {'user': "test@wprdc.edu"}, format='json')
        self.assertEqual(UserProfile.objects.get().approved, False)

        # regular users also don't have permission
        self.client.login(
            username='regular',
            password='tH3@ssW0rd!'
        )
        self.client.post(self.approve_url, {'user': "test@wprdc.edu"}, format='json')
        self.assertEqual(UserProfile.objects.get().approved, False)

        # only users with is_staff = True can approve
        self.client.login(
            username='staff',
            password='tH3@ssW0rd!'
        )
        self.client.post(self.approve_url, {'user': "test@wprdc.edu"}, format='json')
        self.assertEqual(UserProfile.objects.get().approved, True)

    def test_revoke_profile(self):
        """
        Ensures staff, and only staff, can revoke accounts
        """
        # create and approve a request first
        self.client.post(self.request_url, self.request_data, format='json')

        self.client.login(
            username='staff',
            password='tH3@ssW0rd!'
        )
        self.client.post(self.approve_url, {'user': "test@wprdc.edu"}, format='json')

        # first try to revoke without permissions
        self.client.logout()
        self.client.post(self.revoke_url, {'user': "test@wprdc.edu"}, format='json')
        self.assertEqual(UserProfile.objects.get().approved, True)

        # regular users also don't have permission
        self.client.login(
            username='regular',
            password='tH3@ssW0rd!'
        )
        self.client.post(self.revoke_url, {'user': "test@wprdc.edu"}, format='json')
        self.assertEqual(UserProfile.objects.get().approved, True)

        # only users with is_staff = True can revoke
        self.client.login(
            username='staff',
            password='tH3@ssW0rd!'
        )
        self.client.post(self.revoke_url, {'user': "test@wprdc.edu"}, format='json')
        self.assertEqual(UserProfile.objects.get().approved, False)
