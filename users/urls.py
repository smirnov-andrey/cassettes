# Импортируем из приложения django.contrib.auth нужный view-класс
from django.contrib.auth.views import LogoutView, LoginView, PasswordResetView, PasswordChangeView, \
    PasswordChangeDoneView
from django.urls import path
from . import views
from .views import Profile, ProfileUpdate, GoogleSignInView

app_name = 'users'

urlpatterns = [
    path('accounts/google/login/', GoogleSignInView.as_view(), name='google_account_sigin'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path(
        'logout/',
        LogoutView.as_view(template_name='users/logged_out.html'),
        name='logout'
    ),
    path(
        'login/',
        LoginView.as_view(template_name='users/login.html'),
        name='login'
    ),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_change/', PasswordChangeView.as_view(template_name='users/edit-password.html'),
         name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(template_name='users/edit-password-done.html'),
         name='password_change_done'),
    path('profile/', Profile.as_view(), name='profile'),
    path('profile-update/', ProfileUpdate.as_view(), name='profile-update'),
]

