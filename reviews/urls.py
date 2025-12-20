from django.urls import path

from .views import create_review

urlpatterns = [
    path("<int:job_pk>/nowa/", create_review, name="create"),
]
