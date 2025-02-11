from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
import users.views as users

urlpatterns = [
    # For Authentication
    path('login', users.user_login, name='user_login'),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth-user', users.get_auth_user, name='get_auth_user'),
    path('test', users.test, name='test'),
    
    # User CRUD URLs
    path('register', users.create_user, name='create_user'),  # Fixed this line
    path('check-username/<str:username>', users.checkUserName),
    # path('users/<str:username>', users.get_user, name='get_user'),
    path('users/update', users.update_user, name='update_user'),

    path('update_password', users.update_password, name='update_password'),
    path('logout', users.user_logout, name='user_logout'),
]
