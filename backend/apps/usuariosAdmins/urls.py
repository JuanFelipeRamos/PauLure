from django.urls import path
from .views import GetCurrentUserAdmin

urlpatterns = [
    path('me/', GetCurrentUserAdmin.as_view(), name='current-admin'),
]
