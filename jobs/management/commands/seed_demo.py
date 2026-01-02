from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand

from accounts.models import User
from applications.models import Zgloszenie
from jobs.models import Zlecenie
from profiles.models import ProfilWykonawcy


class Command(BaseCommand):
    help = "Tworzy przykladowe dane demo (loginy: zleceniodawca, klient2, klient3, wykonawca, luna, pomocnik; haslo: demo1234)"

    def handle(self, *args, **options):
        def ensure_password(user):
            user.set_password("demo1234")
            user.is_active = True
            user.save()

        client, _ = User.objects.get_or_create(
            username="zleceniodawca",
            defaults={
                "email": "klient@example.com",
                "city": "Warszawa",
                "district": "Mokotow",
                "birth_date": date(1990, 1, 1),
            },
        )
        ensure_password(client)

        client2, _ = User.objects.get_or_create(
            username="klient2",
            defaults={
                "email": "klient2@example.com",
                "city": "Warszawa",
                "district": "Ursynow",
                "birth_date": date(1988, 9, 9),
            },
        )
        ensure_password(client2)

        client3, _ = User.objects.get_or_create(
            username="klient3",
            defaults={
                "email": "klient3@example.com",
                "city": "Warszawa",
                "district": "Praga",
                "birth_date": date(1992, 6, 18),
            },
        )
        ensure_password(client3)

        worker, _ = User.objects.get_or_create(
            username="wykonawca",
            defaults={
                "email": "wykonawca@example.com",
                "city": "Warszawa",
                "district": "Ochota",
                "birth_date": date(2000, 5, 5),
            },
        )
        ensure_password(worker)

        worker2, _ = User.objects.get_or_create(
            username="luna",
            defaults={
                "email": "luna@example.com",
                "city": "Warszawa",
                "district": "Wola",
                "birth_date": date(2004, 7, 12),
            },
        )
        ensure_password(worker2)

        worker3, _ = User.objects.get_or_create(
            username="pomocnik",
            defaults={
                "email": "pomocnik@example.com",
                "city": "Warszawa",
                "district": "Zoliborz",
                "birth_date": date(1998, 3, 30),
            },
        )
        ensure_password(worker3)

        ProfilWykonawcy.objects.get_or_create(
            user=worker,
            defaults={
                "stawka_h": 35,
                "dostepnosc": "flex",
                "kategorie": ["sprzatanie", "zakupy"],
                "bio": "Pomoge z drobnymi sprawami w okolicy.",
                "ok_dla_niepelnoletnich": True,
                "rating_avg": 4.8,
                "rating_count": 19,
            },
        )

        ProfilWykonawcy.objects.get_or_create(
            user=worker2,
            defaults={
                "stawka_h": 30,
                "dostepnosc": "weekend",
                "kategorie": ["wyprowadzanie psa", "koszenie trawy"],
                "bio": "Licealistka, szukam drobnych zlecen po szkole i w weekendy.",
                "ok_dla_niepelnoletnich": True,
                "rating_avg": 4.6,
                "rating_count": 12,
            },
        )

        ProfilWykonawcy.objects.get_or_create(
            user=worker3,
            defaults={
                "stawka_h": 28,
                "dostepnosc": "weekdays",
                "kategorie": ["montaz", "malowanie"],
                "bio": "Zlota raczka, popoludniami i wieczorami.",
                "ok_dla_niepelnoletnich": False,
                "rating_avg": 4.7,
                "rating_count": 8,
            },
        )

        jobs_data = [
            {
                "owner": client,
                "tytul": "Koszenie trawnika przed domem",
                "opis": "Dzis 16-18, sprzatniecie skoszonej trawy po wszystkim.",
                "kategoria": "Koszenie trawy",
                "miasto": "Warszawa",
                "dzielnica": "Wawer",
                "data_start": date.today(),
                "czas_trwania_h": 2,
                "stawka_h": 80,
                "ok_dla_niepelnoletnich": True,
            },
            {
                "owner": client,
                "tytul": "Codzienny spacer z psem (Luna)",
                "opis": "Pon-pt 18:00-18:45, platnosc tygodniowo, pies sredniej wielkosci.",
                "kategoria": "Wyprowadzanie psa",
                "miasto": "Warszawa",
                "dzielnica": "Mokotow",
                "data_start": date.today() + timedelta(days=1),
                "czas_trwania_h": 1,
                "stawka_h": 30,
                "ok_dla_niepelnoletnich": True,
            },
            {
                "owner": client,
                "tytul": "Zrobienie zakupow dla starszej pani",
                "opis": "Lista zakupow gotowa, zwrot za zakupy osobno. Prosze o pomoc jutro rano.",
                "kategoria": "Zakupy",
                "miasto": "Warszawa",
                "dzielnica": "Praga-Poludnie",
                "data_start": date.today() + timedelta(days=1),
                "czas_trwania_h": 2,
                "stawka_h": 40,
                "ok_dla_niepelnoletnich": True,
            },
            {
                "owner": client2,
                "tytul": "Montaz karnisza",
                "opis": "2 karnisze w salonie, potrzebna wiertarka i poziomica.",
                "kategoria": "Montaz",
                "miasto": "Warszawa",
                "dzielnica": "Ursynow",
                "data_start": date.today() + timedelta(days=1),
                "czas_trwania_h": 1,
                "stawka_h": 50,
                "ok_dla_niepelnoletnich": False,
            },
            {
                "owner": client2,
                "tytul": "Szybka pomoc przy przeprowadzce",
                "opis": "Wyniesienie kartonów do samochodu, 4 piętro bez windy.",
                "kategoria": "Przeprowadzka",
                "miasto": "Warszawa",
                "dzielnica": "Wola",
                "data_start": date.today() + timedelta(days=2),
                "czas_trwania_h": 2,
                "stawka_h": 70,
                "ok_dla_niepelnoletnich": False,
            },
            {
                "owner": client3,
                "tytul": "Malowanie małego pokoju",
                "opis": "Pokój 10m2, ściany i sufit, farba na miejscu.",
                "kategoria": "Malowanie",
                "miasto": "Warszawa",
                "dzielnica": "Praga",
                "data_start": date.today() + timedelta(days=3),
                "czas_trwania_h": 2,
                "stawka_h": 120,
                "ok_dla_niepelnoletnich": False,
            },
            {
                "owner": client3,
                "tytul": "Pomoc w lekcjach matematyki",
                "opis": "Przygotowanie do sprawdzianu, 2 godziny.",
                "kategoria": "Korepetycje",
                "miasto": "Warszawa",
                "dzielnica": "Ochota",
                "data_start": date.today() + timedelta(days=1),
                "czas_trwania_h": 2,
                "stawka_h": 60,
                "ok_dla_niepelnoletnich": True,
            },
        ]

        jobs = []
        for jd in jobs_data:
            defaults = jd.copy()
            owner = defaults.pop("owner")
            job, _ = Zlecenie.objects.get_or_create(owner=owner, tytul=defaults["tytul"], defaults=defaults)
            jobs.append(job)

        if len(jobs) >= 3:
            Zgloszenie.objects.get_or_create(
                zlecenie=jobs[1],
                wykonawca=worker2,
                defaults={"wiadomosc": "Chetnie codziennie, mam czas po 17:30.", "proponowana_stawka": 30},
            )

            accepted_app, _ = Zgloszenie.objects.get_or_create(
                zlecenie=jobs[0],
                wykonawca=worker,
                defaults={"wiadomosc": "Moge dzis o 16:00. Mam wlasna kosiarke.", "proponowana_stawka": 80},
            )
            if accepted_app.status == Zgloszenie.Status.PENDING and jobs[0].has_capacity:
                try:
                    accepted_app.accept(accepted_app.wykonawca)
                except (ValidationError, ValueError):
                    pass

            completed_app, _ = Zgloszenie.objects.get_or_create(
                zlecenie=jobs[2],
                wykonawca=worker3,
                defaults={"wiadomosc": "Zrobie zakupy jutro rano.", "proponowana_stawka": 42},
            )
            if completed_app.status == Zgloszenie.Status.PENDING and jobs[2].has_capacity:
                try:
                    completed_app.accept(completed_app.wykonawca)
                    completed_app.complete(completed_app.zlecenie.owner)
                except (ValidationError, ValueError):
                    pass

        self.stdout.write(
            self.style.SUCCESS(
                "Dane demo utworzone. Loginy: zleceniodawca / klient2 / klient3 / wykonawca / luna / pomocnik (haslo: demo1234)"
            )
        )
