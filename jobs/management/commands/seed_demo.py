from datetime import date, timedelta

from django.core.management.base import BaseCommand

from accounts.models import User
from applications.models import Zgloszenie
from jobs.models import Zlecenie
from profiles.models import ProfilWykonawcy


class Command(BaseCommand):
    help = "Tworzy przykladowe dane demo (loginy: zleceniodawca, klient2, wykonawca, luna; haslo: demo1234)"

    def handle(self, *args, **options):
        def ensure_password(user):
            user.set_password("demo1234")
            user.is_active = True
            user.save()

        client, _ = User.objects.get_or_create(
            username="zleceniodawca",
            defaults={
                "email": "klient@example.com",
                "role": User.ROLE_CLIENT,
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
                "role": User.ROLE_CLIENT,
                "city": "Warszawa",
                "district": "Ursynow",
                "birth_date": date(1988, 9, 9),
            },
        )
        ensure_password(client2)

        worker, _ = User.objects.get_or_create(
            username="wykonawca",
            defaults={
                "email": "wykonawca@example.com",
                "role": User.ROLE_WORKER,
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
                "role": User.ROLE_WORKER,
                "city": "Warszawa",
                "district": "Wola",
                "birth_date": date(2004, 7, 12),
            },
        )
        ensure_password(worker2)

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

        jobs_data = [
            {
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
        ]

        created_jobs = []
        for jd in jobs_data:
            job, _ = Zlecenie.objects.get_or_create(
                owner=client,
                tytul=jd["tytul"],
                defaults=jd,
            )
            created_jobs.append(job)

        extra_jobs = [
            {
                "tytul": "Malowanie malego pokoju",
                "opis": "Pokoj 10m2, sciany i sufit, farba i narzedzia na miejscu.",
                "kategoria": "Malowanie",
                "miasto": "Warszawa",
                "dzielnica": "Ursynow",
                "data_start": date.today() + timedelta(days=2),
                "czas_trwania_h": 2,
                "stawka_h": 80,
                "ok_dla_niepelnoletnich": False,
                "status": Zlecenie.STATUS_PUBLISHED,
            },
            {
                "tytul": "Montaz karnisza",
                "opis": "2 karnisze w salonie, potrzebna wiertarka i poziomica.",
                "kategoria": "Montaz",
                "miasto": "Warszawa",
                "dzielnica": "Ursynow",
                "data_start": date.today() + timedelta(days=1),
                "czas_trwania_h": 1,
                "stawka_h": 50,
                "ok_dla_niepelnoletnich": False,
                "status": Zlecenie.STATUS_PUBLISHED,
            },
        ]

        for jd in extra_jobs:
            Zlecenie.objects.get_or_create(owner=client2, tytul=jd["tytul"], defaults=jd)

        if created_jobs:
            Zgloszenie.objects.get_or_create(
                zlecenie=created_jobs[0],
                wykonawca=worker,
                defaults={"wiadomosc": "Moge dzis o 16:00. Mam wlasna kosiarke.", "proponowana_stawka": 80},
            )
            Zgloszenie.objects.get_or_create(
                zlecenie=created_jobs[1],
                wykonawca=worker2,
                defaults={"wiadomosc": "Chetnie codziennie, mam czas po 17:30.", "proponowana_stawka": 30},
            )
            Zgloszenie.objects.get_or_create(
                zlecenie=created_jobs[2],
                wykonawca=worker,
                defaults={"wiadomosc": "Moge jutro rano, prosze o liste.", "proponowana_stawka": 40},
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Dane demo utworzone. Loginy: zleceniodawca / klient2 / wykonawca / luna (haslo: demo1234)"
            )
        )
