from django.urls import path
from django.contrib.auth import views as auth_views
from .views import RegisterView, ProfileUpdateView, UserDashboardView, UserSettingsView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('dashboard/', UserDashboardView.as_view(), name='dashboard'),
    path('settings/', UserSettingsView.as_view(), name='settings'),
    
    # Password Reset
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
    
    # Change Password
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html', success_url='/accounts/profile/'), name='password_change'),
]
