from django.urls import path

from .views import thread

urlpatterns = [
    path("<int:job_pk>/", thread, name="thread"),
]
