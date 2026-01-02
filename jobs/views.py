from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from applications.models import Zgloszenie
from profiles.models import ProfilWykonawcy

from .forms import ZlecenieFilterForm, ZlecenieForm
from .models import Zlecenie


class ZlecenieListView(View):
    template_name = "jobs/list.html"

    def get(self, request):
        mode = request.GET.get("mode", "worker")
        if mode not in ("worker", "client"):
            mode = "worker"

        qs = (
            Zlecenie.objects.select_related("owner", "accepted_application", "accepted_application__wykonawca")
            .prefetch_related("zgloszenia")
            .filter(status=Zlecenie.STATUS_PUBLISHED)
        )
        helper_profiles = ProfilWykonawcy.objects.select_related("user")
        sidebar_profile = getattr(request.user, "worker_profile", None) if request.user.is_authenticated else None
        my_applications = []
        my_posted_jobs = []
        accepted_history = []
        if request.user.is_authenticated:
            accepted_history = (
                Zgloszenie.objects.select_related("zlecenie", "zlecenie__owner")
                .filter(wykonawca=request.user, status__in=[Zgloszenie.Status.ACCEPTED, Zgloszenie.Status.COMPLETED])
                .order_by("-decided_at", "-created_at")
            )
        if mode == "client":
            qs = helper_profiles
        form = ZlecenieFilterForm(request.GET or None)
        if form.is_valid():
            data = form.cleaned_data
            if mode == "client":
                if data.get("miasto"):
                    raw = data["miasto"]
                    parts = [p.strip() for p in raw.replace("/", ",").split(",") if p.strip()]
                    if len(parts) >= 2:
                        miasto_val, dzielnica_val = parts[0], parts[1]
                        qs = qs.filter(user__city__icontains=miasto_val, user__district__icontains=dzielnica_val)
                    else:
                        qs = qs.filter(Q(user__city__icontains=raw) | Q(user__district__icontains=raw))
                if data.get("dzielnica"):
                    qs = qs.filter(user__district__icontains=data["dzielnica"])
                if data.get("ok_dla_niepelnoletnich"):
                    qs = qs.filter(ok_dla_niepelnoletnich=True)
                if data.get("tylko_weekend"):
                    qs = qs.filter(dostepnosc="weekend")
            else:
                if data.get("miasto"):
                    raw = data["miasto"]
                    parts = [p.strip() for p in raw.replace("/", ",").split(",") if p.strip()]
                    if len(parts) >= 2:
                        miasto_val, dzielnica_val = parts[0], parts[1]
                        qs = qs.filter(miasto__icontains=miasto_val, dzielnica__icontains=dzielnica_val)
                    else:
                        qs = qs.filter(Q(miasto__icontains=raw) | Q(dzielnica__icontains=raw))
                if data.get("dzielnica"):
                    qs = qs.filter(dzielnica__icontains=data["dzielnica"])
                if data.get("ok_dla_niepelnoletnich"):
                    qs = qs.filter(ok_dla_niepelnoletnich=True)
                if data.get("max_czas"):
                    qs = qs.filter(czas_trwania_h__lte=2)
                if data.get("max_stawka"):
                    qs = qs.filter(stawka_h__lte=40)
                if data.get("tylko_dzis"):
                    qs = qs.filter(data_start=date.today())
                if data.get("tylko_weekend"):
                    qs = qs.filter(data_start__week_day__in=[1, 7])

        if request.user.is_authenticated:
            if mode == "worker":
                job_ids = list(qs.values_list("id", flat=True))
                if job_ids:
                    my_applications = list(
                        Zgloszenie.objects.filter(zlecenie_id__in=job_ids, wykonawca=request.user)
                    )
            my_posted_jobs = list(
                Zlecenie.objects.select_related("accepted_application", "accepted_application__wykonawca")
                .filter(owner=request.user)
                .order_by("-created_at")[:6]
            )
        return render(
            request,
            self.template_name,
            {
                "zlecenia": qs,
                "form": form,
                "mode": mode,
                "sidebar_profile": sidebar_profile,
                "accepted_history": accepted_history,
                "my_applications": my_applications,
                "my_posted_jobs": my_posted_jobs,
            },
        )


class ZlecenieDetailView(View):
    template_name = "jobs/detail.html"

    def get(self, request, pk):
        zlecenie = get_object_or_404(Zlecenie, pk=pk)
        my_application = None
        if request.user.is_authenticated:
            my_application = zlecenie.zgloszenia.filter(wykonawca=request.user).first()
        return render(request, self.template_name, {"zlecenie": zlecenie, "my_application": my_application})


@method_decorator(login_required, name="dispatch")
class ZlecenieCreateView(View):
    template_name = "jobs/form.html"

    def get(self, request):
        return render(request, self.template_name, {"form": ZlecenieForm()})

    def post(self, request):
        form = ZlecenieForm(request.POST)
        if form.is_valid():
            zlecenie = form.save(commit=False)
            zlecenie.owner = request.user
            zlecenie.save()
            messages.success(request, "Zlecenie dodane.")
            return redirect(zlecenie.get_absolute_url())
        return render(request, self.template_name, {"form": form})


@method_decorator(login_required, name="dispatch")
class ZlecenieUpdateView(View):
    template_name = "jobs/form.html"

    def get(self, request, pk):
        zlecenie = get_object_or_404(Zlecenie, pk=pk, owner=request.user)
        return render(request, self.template_name, {"form": ZlecenieForm(instance=zlecenie), "edit": True})

    def post(self, request, pk):
        zlecenie = get_object_or_404(Zlecenie, pk=pk, owner=request.user)
        form = ZlecenieForm(request.POST, instance=zlecenie)
        if form.is_valid():
            form.save()
            messages.success(request, "Zlecenie zapisane.")
            return redirect(zlecenie.get_absolute_url())
        return render(request, self.template_name, {"form": form, "edit": True})


@login_required
def zlecenie_cancel(request, pk):
    zlecenie = get_object_or_404(Zlecenie, pk=pk, owner=request.user)
    zlecenie.cancel()
    messages.info(request, "Zlecenie anulowane.")
    return redirect("jobs:list")
