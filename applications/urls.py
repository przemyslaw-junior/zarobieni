from django.urls import path

from .views import ZgloszenieCreateView, zgloszenie_accept, zgloszenie_decline

urlpatterns = [
    path("<int:job_pk>/nowe/", ZgloszenieCreateView.as_view(), name="create"),
    path("<int:pk>/akceptuj/", zgloszenie_accept, name="accept"),
    path("<int:pk>/odrzuc/", zgloszenie_decline, name="decline"),
]
