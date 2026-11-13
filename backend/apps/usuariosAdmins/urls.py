from django.urls import path
from .views import GetCurrentUserAdmin, GetUsersAdmins

urlpatterns = [
    path('me/', GetCurrentUserAdmin.as_view(), name='current-admin'),
    path('users/', GetUsersAdmins.as_view(), name='admin-all'),
]
