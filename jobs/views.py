from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from .forms import ZlecenieFilterForm, ZlecenieForm
from .models import Zlecenie


class ZlecenieListView(View):
    template_name = "jobs/list.html"

    def get(self, request):
        mode = request.GET.get("mode", "worker")
        if mode not in ("worker", "client"):
            mode = "worker"

        qs = Zlecenie.objects.select_related("owner").filter(status=Zlecenie.STATUS_PUBLISHED)
        client_jobs = None
        if mode == "client" and request.user.is_authenticated and request.user.is_client:
            client_jobs = Zlecenie.objects.filter(owner=request.user).order_by("-created_at")
            qs = client_jobs
        form = ZlecenieFilterForm(request.GET or None)
        if form.is_valid():
            data = form.cleaned_data
            if data.get("miasto"):
                raw = data["miasto"]
                # pozwól na format "Warszawa / Mokotów" lub "Warszawa, Mokotów"
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
        return render(
            request,
            self.template_name,
            {
                "zlecenia": qs,
                "form": form,
                "mode": mode,
                "client_jobs": client_jobs,
            },
        )


class ZlecenieDetailView(View):
    template_name = "jobs/detail.html"

    def get(self, request, pk):
        zlecenie = get_object_or_404(Zlecenie, pk=pk)
        return render(request, self.template_name, {"zlecenie": zlecenie})


@method_decorator(login_required, name="dispatch")
class ZlecenieCreateView(View):
    template_name = "jobs/form.html"

    def get(self, request):
        return render(request, self.template_name, {"form": ZlecenieForm()})

    def post(self, request):
        form = ZlecenieForm(request.POST)
        if form.is_valid():
            if not request.user.is_client:
                messages.error(request, "Tylko zleceniodawcy mogą dodawać zlecenia.")
                return redirect("jobs:list")
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
