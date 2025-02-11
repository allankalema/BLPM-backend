from django.urls import path
import users.views as users

urlpatterns = [
    # Authentication
    path('login', users.user_login, name='user_login'),

    # User Registration (Two-step)
    path('register', users.register, name='register'),
    path('create_location', users.create_location, name='complete_profile'),

    # Other User Operations
    path('check-username/<str:username>', users.checkUserName),
    path('users/update', users.update_user, name='update_user'),
    path('location/update/', users.update_location, name='update_location'),
    path('update_password', users.update_password, name='update_password'),
    path('logout', users.user_logout, name='user_logout'),
]
