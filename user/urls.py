# from django.urls import path
# from .views import RegisterView, LogoutView, ChangePasswordView
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# urlpatterns = [
#     path('login/', TokenObtainPairView.as_view(), name='login'),
#     path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#     path('register/', RegisterView.as_view(), name="sign_up"),
#     path('logout/', LogoutView.as_view(), name="logout"),
#     path('change-password/', ChangePasswordView.as_view(), name='change-password'),

# ]


# users/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, ChangePasswordView, UserManageViewSet, LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = DefaultRouter()
router.register(r'users', UserManageViewSet, basename='users')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
