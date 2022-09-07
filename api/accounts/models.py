from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _

from housecat.abstract_models import Described
from housing_data.models import ProjectIndex


class User(AbstractUser):
    pass


class UserProfile(models.Model):
    ADMIN = 'ADMIN'
    NONPROFIT = 'nonprofit'
    GOVERNMENT = 'government'
    PHILANTHROPY = 'philanthropy'
    MEDIA = 'media'
    STUDENT = 'student'
    RESEARCHER = 'researcher'
    MISSION_ALIGNED_DEVELOPER = 'mission_aligned_dev'
    FINANCIAL_INST = 'financial_inst'

    USER_CATEGORY_CHOICES = (
        (ADMIN, _('--ADMINISTRATOR--')),
        (NONPROFIT, _('Housing and community development-focused nonprofit organizations ')),
        (GOVERNMENT, _('Local, state, and federal government agencies and authorities')),
        (PHILANTHROPY, _('Philanthropic organizations/Charitable foundations ')),
        (MEDIA, _('Media organizations')),
        (STUDENT, _('Students')),
        (RESEARCHER, _('Researchers')),
        (MISSION_ALIGNED_DEVELOPER, _('Mission-aligned developers')),
        (FINANCIAL_INST, _('Financial Institutions')),
    )
    # User attributes
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # user category
    category = models.CharField(max_length=64, choices=USER_CATEGORY_CHOICES)
    # group / organization name
    affiliation = models.CharField(max_length=128, null=True, blank=True)
    # what are your intended uses/target audiences for the data?
    intended_use = models.TextField(null=True, blank=True)
    # how long do you anticipate needing/wanting access?
    expected_account_tenure = models.IntegerField(help_text='in weeks', default=4)
    # do you have any potential COIs which would preclude access to the data?
    conflicts = models.TextField(null=True, blank=True)

    # Account Tracking
    # when the account will stop working and need to be reset by maintainers
    expiration_date = models.DateField(help_text='', null=True, blank=True)
    # have users agree to terms when they first log in
    agreed_to_terms = models.BooleanField(null=True, blank=True)

    def is_stale(self):
        return (datetime.now() - self.user.last_login) > timedelta(days=settings.TIME_TO_STALE)

    def is_expired(self):
        if self.category == self.ADMIN:
            return False
        if self.expiration_date is not None:
            return datetime.now() < self.expiration_date
        return True

    def __str__(self):
        return self.user.username


class Watchlist(Described):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = ArrayField(base_field=models.CharField(max_length=200))

    @property
    def user_name(self):
        return self.user.username

    @property
    def project_indices(self):
        return ProjectIndex.objects.filter(property_id__in=self.items)
