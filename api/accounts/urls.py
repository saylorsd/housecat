from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'profile', views.UserProfileViewSet, basename='userprofile')

urlpatterns = router.urls + [
    path('request/', views.request_new_profile, name='request_new_profile'),
    path('approve/', views.approve_profile, name='approve_profile'),
    path('revoke/', views.revoke_profile, name='revoke_profile'),
    path('user/', views.check_login, name='check_login'),
    path(r'activate/<uidb64>/<token>/', views.activate, name='activate'),

    path('', include('django.contrib.auth.urls')),
]
