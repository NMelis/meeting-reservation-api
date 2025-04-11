from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from server.apps.user.views import RegisterView

urlpatterns = [
    path('auth/', include([
        path('register/', RegisterView.as_view(), name='register'),
        path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ])),
]
