from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("konto/", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("profil/", include(("profiles.urls", "profiles"), namespace="profiles")),
    path("zlecenia/", include(("jobs.urls", "jobs"), namespace="jobs")),
    path("zgloszenia/", include(("applications.urls", "applications"), namespace="applications")),
    path("wiadomosci/", include(("messaging.urls", "messaging"), namespace="messaging")),
    path("opinie/", include(("reviews.urls", "reviews"), namespace="reviews")),
]
