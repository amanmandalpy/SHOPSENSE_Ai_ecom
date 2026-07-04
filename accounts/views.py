from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import UserRegistrationForm, UserProfileUpdateForm
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        # Save user and log them in
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Account created successfully! Please verify your email.")
        return redirect(self.success_url)

class UserDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'

class UserSettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/settings.html'

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileUpdateForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user
        
    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully.")
        return super().form_valid(form)
