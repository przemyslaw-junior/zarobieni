from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
        return render(request, self.template_name, {"form": ZgloszenieForm(), "zlecenie": zlecenie})

    def post(self, request, job_pk):
        zlecenie = get_object_or_404(Zlecenie, pk=job_pk)
        form = ZgloszenieForm(request.POST)
        if form.is_valid():
            if not request.user.is_worker:
                messages.error(request, "Tylko wykonawca może złożyć zgłoszenie.")
                return redirect(zlecenie.get_absolute_url())
            zg = form.save(commit=False)
            zg.zlecenie = zlecenie
            zg.wykonawca = request.user
            zg.save()
            messages.success(request, "Zgłoszenie wysłane.")
            return redirect(zlecenie.get_absolute_url())
        return render(request, self.template_name, {"form": form, "zlecenie": zlecenie})


@login_required
def zgloszenie_accept(request, pk):
    zg = get_object_or_404(Zgloszenie, pk=pk, zlecenie__owner=request.user)
    zg.accept()
    messages.success(request, "Wykonawca wybrany.")
    return redirect(zg.zlecenie.get_absolute_url())


@login_required
def zgloszenie_decline(request, pk):
    zg = get_object_or_404(Zgloszenie, pk=pk, zlecenie__owner=request.user)
    zg.decline()
    messages.info(request, "Zgłoszenie odrzucone.")
    return redirect(zg.zlecenie.get_absolute_url())
