from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CustomTokenObtainPairView, register, profile_detail

app_name = 'accounts'

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', register, name='register'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profiles/me/', profile_detail, name='profile_detail'),
]