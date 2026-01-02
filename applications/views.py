from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from jobs.models import Zlecenie

from .forms import ZgloszenieForm
from .models import Zgloszenie


@method_decorator(login_required, name="dispatch")
class ZgloszenieCreateView(View):
    template_name = "applications/form.html"

    def get(self, request, job_pk):
        zlecenie = get_object_or_404(Zlecenie, pk=job_pk)
        if not zlecenie.has_capacity or zlecenie.status != Zlecenie.STATUS_PUBLISHED:
            messages.error(request, "Zlecenie nie przyjmuje nowych zgloszen.")
            return redirect(zlecenie.get_absolute_url())
        return render(request, self.template_name, {"form": ZgloszenieForm(), "zlecenie": zlecenie})

    def post(self, request, job_pk):
        zlecenie = get_object_or_404(Zlecenie, pk=job_pk)
        form = ZgloszenieForm(request.POST)
        if form.is_valid():
            if zlecenie.owner == request.user:
                messages.error(request, "Nie możesz zgłaszać się do własnego zlecenia.")
                return redirect(zlecenie.get_absolute_url())
            if not zlecenie.has_capacity or zlecenie.status != Zlecenie.STATUS_PUBLISHED:
                messages.error(request, "Zlecenie nie przyjmuje nowych zgloszen.")
                return redirect(zlecenie.get_absolute_url())
            zg = form.save(commit=False)
            zg.zlecenie = zlecenie
            zg.wykonawca = request.user
            zg.save()
            messages.success(request, "Zgloszenie wyslane.")
            return redirect(zlecenie.get_absolute_url())
        return render(request, self.template_name, {"form": form, "zlecenie": zlecenie})


@login_required
def zgloszenie_accept(request, pk):
    zg = get_object_or_404(Zgloszenie, pk=pk, zlecenie__owner=request.user)
    try:
        zg.accept(request.user)
        messages.success(request, "Zaakceptowales zgloszenie.")
    except (ValidationError) as exc:
        messages.error(request, "; ".join(exc.messages))
    except Exception as exc:
        messages.error(request, str(exc))
    return redirect(zg.zlecenie.get_absolute_url())


@login_required
def zgloszenie_decline(request, pk):
    zg = get_object_or_404(Zgloszenie, pk=pk, zlecenie__owner=request.user)
    try:
        zg.reject(request.user)
        messages.info(request, "Zgloszenie odrzucone.")
    except ValidationError as exc:
        messages.error(request, "; ".join(exc.messages))
    except Exception as exc:
        messages.error(request, str(exc))
    return redirect(zg.zlecenie.get_absolute_url())


@login_required
def zgloszenie_complete(request, pk):
    zg = get_object_or_404(Zgloszenie, pk=pk, zlecenie__owner=request.user)
    try:
        zg.complete(request.user)
        messages.success(request, "Zlecenie oznaczone jako zakonczone.")
    except ValidationError as exc:
        messages.error(request, "; ".join(exc.messages))
    except Exception as exc:
        messages.error(request, str(exc))
    return redirect(zg.zlecenie.get_absolute_url())
