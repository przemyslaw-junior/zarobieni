from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from jobs.models import Zlecenie

from .forms import WiadomoscForm
from .models import Wiadomosc


@login_required
def thread(request, job_pk):
    zlecenie = get_object_or_404(Zlecenie, pk=job_pk)
    accepted = zlecenie.accepted_application
    if not accepted:
        messages.error(request, "Czat dostępny po wyborze wykonawcy.")
        return redirect(zlecenie.get_absolute_url())
    worker = accepted.wykonawca
    if request.user not in [zlecenie.owner, worker]:
        messages.error(request, "Brak dostępu do tej konwersacji.")
        return redirect("jobs:list")

    if request.method == "POST":
        form = WiadomoscForm(request.POST)
        if form.is_valid():
            wiadomosc = form.save(commit=False)
            wiadomosc.zlecenie = zlecenie
            wiadomosc.nadawca = request.user
            wiadomosc.odbiorca = worker if request.user == zlecenie.owner else zlecenie.owner
            wiadomosc.save()
            messages.success(request, "Wiadomość wysłana.")
            return redirect("messaging:thread", job_pk=job_pk)
    else:
        form = WiadomoscForm()
    wiadomosci = Wiadomosc.objects.filter(zlecenie=zlecenie)
    return render(
        request,
        "messaging/thread.html",
        {"zlecenie": zlecenie, "wiadomosci": wiadomosci, "form": form, "worker": worker},
    )
