from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from accounts.models import User

from .forms import ProfilWykonawcyForm
from .models import ProfilWykonawcy


@method_decorator(login_required, name="dispatch")
class ProfilDetailView(View):
    template_name = "profiles/detail.html"

    def get(self, request, username=None):
        user = get_object_or_404(User, username=username) if username else request.user
        profile = getattr(user, "worker_profile", None)
        return render(request, self.template_name, {"profile_user": user, "profile": profile})


@method_decorator(login_required, name="dispatch")
class ProfilUpdateView(View):
    template_name = "profiles/edit.html"

    def get(self, request):
        profile, _ = ProfilWykonawcy.objects.get_or_create(
            user=request.user, defaults={"stawka_h": 0, "kategorie": []}
        )
        initial = {"kategorie": ", ".join(profile.kategorie)}
        form = ProfilWykonawcyForm(instance=profile, initial=initial)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        profile, _ = ProfilWykonawcy.objects.get_or_create(
            user=request.user, defaults={"stawka_h": 0, "kategorie": []}
        )
        form = ProfilWykonawcyForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil zapisany.")
            return redirect("profiles:detail", username=request.user.username)
        return render(request, self.template_name, {"form": form})
