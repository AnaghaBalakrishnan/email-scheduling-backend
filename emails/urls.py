# emails/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScheduledEmailViewSet

router = DefaultRouter()
router.register(r'schedule', ScheduledEmailViewSet, basename='schedule-email')

urlpatterns = [
    path('', include(router.urls)),
]   