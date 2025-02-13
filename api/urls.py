from django.urls import path
import users.views as users
import property.views as properties
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Authentication
    path('login', users.user_login, name='user_login'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User CRUD URLs
    path('register', users.register, name='create_user'),  # Fixed this line
    path('check-username/<str:username>', users.checkUserName),
    path('check-email/<str:email>', users.checkEmail),
    path('users/update', users.update_user, name='update_user'),

    path('update_password', users.update_password, name='update_password'),
    path('logout', users.user_logout, name='user_logout'),

    path('properties', properties.index, name='properties'),
    path('create-property', properties.create_property, name='create_property'),
    path('update-property', properties.update_property, name='update_property'),
    path('delete-property', properties.delete_property, name='delete_property'),

]
