from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View

from .forms import LoginForm, UserRegistrationForm


class RegisterView(View):
    template_name = "accounts/register.html"

    def get(self, request):
        return render(request, self.template_name, {"form": UserRegistrationForm()})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Konto utworzone.")
            return redirect("jobs:list")
        return render(request, self.template_name, {"form": form})


class LoginPageView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True


class LogoutPageView(View):
    """Logout on POST (preferred) and allow GET fallback for convenience."""

    def post(self, request):
        logout(request)
        return redirect("home")

    def get(self, request):
        logout(request)
        return redirect("home")
