from django.urls import path

from .views import LoginPageView, LogoutPageView, RegisterView

urlpatterns = [
    path("rejestracja/", RegisterView.as_view(), name="register"),
    path("logowanie/", LoginPageView.as_view(), name="login"),
    path("wyloguj/", LogoutPageView.as_view(), name="logout"),
]
