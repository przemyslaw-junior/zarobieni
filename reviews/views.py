from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from applications.models import Zgloszenie
from jobs.models import Zlecenie

from .forms import OpiniaForm
from .models import Opinia


@login_required
def create_review(request, job_pk):
    zlecenie = get_object_or_404(Zlecenie, pk=job_pk, owner=request.user)
    accepted = zlecenie.accepted_application
    if not accepted or zlecenie.status != Zlecenie.STATUS_COMPLETED:
        messages.error(request, "Opinia możliwa po zakończeniu zlecenia.")
        return redirect(zlecenie.get_absolute_url())
    reviewee = accepted.wykonawca
    if request.method == "POST":
        form = OpiniaForm(request.POST)
        if form.is_valid():
            opinia, created = Opinia.objects.get_or_create(
                zlecenie=zlecenie, reviewer=request.user, reviewee=reviewee, defaults=form.cleaned_data
            )
            if not created:
                messages.info(request, "Opinia została już wystawiona.")
            else:
                messages.success(request, "Opinia dodana.")
            return redirect(zlecenie.get_absolute_url())
    else:
        form = OpiniaForm()
    return render(request, "reviews/form.html", {"form": form, "zlecenie": zlecenie, "reviewee": reviewee})
