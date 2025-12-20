from django.urls import path

from .views import ProfilDetailView, ProfilUpdateView

urlpatterns = [
    path("me/", ProfilDetailView.as_view(), name="me"),
    path("me/edytuj/", ProfilUpdateView.as_view(), name="edit"),
    path("<str:username>/", ProfilDetailView.as_view(), name="detail"),
]
