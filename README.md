# Projekt zaliczeniowy - Aplikacje internetowe
# zarobieni.pl

# zarobieni.pl (MVP)

Django (Python 3) marketplace lokalnych drobnych zleceń zgodny z SRS. Frontend: Django Templates + Bootstrap 5. Auth: Django auth z rozszerzonym modelem użytkownika (role).

## Wymagane komponenty
- Python 3.10+
- (Opcjonalnie) virtualenv
- Pakiety Pythona: Django
- Baza: SQLite (domyślnie)

## Instalacja (SQLite)
1. `cd zarobieni`
2. (Opcjonalnie) virtualenv:
   - `python -m venv .venv`
   - Windows: `.venv\\Scripts\\activate`
   - Linux/macOS: `source .venv/bin/activate`
3. Zainstaluj zależności: `pip install -r requirements.txt`
4. Migracje: `python manage.py migrate`
5. (Opcjonalnie) konto admin: `python manage.py createsuperuser`
6. Dane demo: `python manage.py seed_demo`  
   (loginy: `zleceniodawca`, `klient2`, `wykonawca`, `luna`; hasło `demo1234`)
7. Uruchom: `python manage.py runserver`
8. Przeglądarka: `http://127.0.0.1:8000/`

## Struktura aplikacji
- `accounts` – rozszerzony model użytkownika (role: zleceniodawca/wykonawca), rejestracja/logowanie.
- `profiles` – profil wykonawcy (stawka, dostępność, kategorie, bio, flaga „OK dla niepełnoletnich”, rating).
- `jobs` – zlecenia, statusy, filtrowanie, publikacja/edycja/anulowanie.
- `applications` – zgłoszenia wykonawców, akceptacja/odrzucenie, unikatowość per zlecenie.
- `messaging` – czat 1:1 po akceptacji zgłoszenia.
- `reviews` – opinie po zakończonym zleceniu.
- `templates/`, `static/` – UI oparte na makiecie (Bootstrap 5).

## Kluczowe adresy
- `/` – strona główna.
- `/konto/rejestracja/`, `/konto/logowanie/`, `/konto/wyloguj/`.
- `/zlecenia/` – lista z filtrami (miasto/dzielnica, dziś, weekend, do 2h, do 40 zł/h, OK dla niepełnoletnich).
- `/zlecenia/nowe/` – dodawanie (tylko zleceniodawca).
- `/zlecenia/<id>/` – szczegóły, zgłoszenia, akceptacja, czat, opinie.
- `/zgloszenia/<id>/akceptuj|odrzuc/` – decyzja zleceniodawcy.
- `/wiadomosci/<job_id>/` – czat po akceptacji.
- `/opinie/<job_id>/nowa/` – opinia po statusie „zakończone”.
- `/profil/me/edytuj/` – edycja profilu wykonawcy; `/profil/<username>/` – podgląd.
- `/admin/` – panel administracyjny.

## Walidacje biznesowe (wybrane)
- Użytkownik min. 16 lat.
- Stawka zlecenia ≤ 40 PLN/h (MVP).
- Czas trwania ≤ 2h (MVP).
- Zgłoszenie składa tylko wykonawca; akceptuje/odrzuca tylko właściciel zlecenia.
- Czat dostępny po akceptacji zgłoszenia.
- Opinia możliwa po statusie „zakończone” i przypisanym wykonawcy.

## Ręczne testy end-to-end
- Rejestracja zleceniodawcy, dodanie zlecenia.
- Rejestracja wykonawcy, uzupełnienie profilu, zgłoszenie do zlecenia.
- Akceptacja zgłoszenia, dostęp do czatu.
- Ustawienie zlecenia na „zakończone” (np. w admin) i dodanie opinii.
- Filtry na liście zleceń (miasto/dzielnica, dziś, weekend, do 2h, do 40 zł/h, OK dla niepełnoletnich).

## Uwagi
- Domyślny backend e-mail: konsola (logi w terminalu).
- Ustaw własny `DJANGO_SECRET_KEY` i `DEBUG=0` w produkcji (np. przez zmienne środowiskowe/.env).