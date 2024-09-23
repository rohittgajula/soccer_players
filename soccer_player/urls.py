
from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.views import PublicView, ProtectedView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include('players.urls')),
    path("users/", include('users.urls')),

    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/protected/', ProtectedView.as_view(), name='protected_view'),
    path('api/public/', PublicView.as_view(), name='public_view'),
]
