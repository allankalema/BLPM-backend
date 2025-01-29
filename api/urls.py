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
    
    path('users', users.protected_view, name='protected_view'),

    # User CRUD URLs
    path('users/create/', users.create_user, name='create_user'),  # Fixed this line
    path('users/<str:username>', users.get_user, name='get_user'),
    path('users/update/<str:username>/', users.update_user, name='update_user'),

    path('update_password/', users.update_password, name='update_password'),
    path('logout/', users.user_logout, name='user_logout'),
]
