from django.urls import path

from .views import (
    ZlecenieCreateView,
    ZlecenieDetailView,
    ZlecenieListView,
    ZlecenieUpdateView,
    zlecenie_cancel,
)

urlpatterns = [
    path("", ZlecenieListView.as_view(), name="list"),
    path("nowe/", ZlecenieCreateView.as_view(), name="create"),
    path("<int:pk>/", ZlecenieDetailView.as_view(), name="detail"),
    path("<int:pk>/edycja/", ZlecenieUpdateView.as_view(), name="edit"),
    path("<int:pk>/anuluj/", zlecenie_cancel, name="cancel"),
]
