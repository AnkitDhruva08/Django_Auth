

from django.urls import path



from .views import register_user, login_user, logout_user, verify_authentication

# URLs configuration
urlpatterns = [
    path('api/register/', register_user, name='register_user'),
    path('api/login/', login_user, name='login_user'),
    path('api/logout/', logout_user, name='logout_user'),
    path('api/verify/', verify_authentication, name='verify_authentication'),
]