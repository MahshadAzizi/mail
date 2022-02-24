from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LogInView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('home/', home, name='home'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('activate/<uidb64>/<token>/', ActivateAccountForgotPassword.as_view(), name='activate_password'),
    path('forgot_password/', ForgotPassword.as_view(), name='forgot_password'),


]