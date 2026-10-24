# Preferowane wybory

Skrót dla człowieka: co wybierać w tym repozytorium i projektach, które się na nim wzorują.
Pełne uzasadnienia są w [`docs/zasady-ai.md`](zasady-ai.md) — tutaj tylko decyzje.

## Nienegocjowalne

- **Test przed kodem.** Zawsze, poza zmianami bez wykonywalnego zachowania.
- **Twierdzenie wymaga testu.** Sąd („to czytelniejsze”) oznaczaj jako sąd, nie jako dowód.
- **Jedna zmiana, jeden cel.** Bez refaktorów przy okazji.

## Architektura

- **Funkcjonalny rdzeń, cienka skorupa I/O.** Logika nie wie, że istnieje sieć, zegar czy plik.
- **Zależności w jedną stronę.** Adaptery i UI znają rdzeń; rdzeń nie zna ich nigdy.
- **Granica walidacji raz.** Dane z zewnątrz zamieniane na wąski typ na wejściu, dalej bez sprawdzeń.
- **Moduły według domeny, nie według typu.** `zamowienia/`, nie `services/` + `models/` + `controllers/`.
- **Warianty jako zamknięte typy z wyczerpującym dopasowaniem.** Zapomniany przypadek = błąd kompilacji.
- **Błędy jako wartości w rdzeniu.** Wyjątki tylko na granicy, gdzie stają się odpowiedzią lub logiem.
- **Stan jawny, przekazywany argumentem.** Żadnych globali, singletonów ani mutowalnych modułów.
- **Czas, losowość, identyfikatory i sieć wstrzykiwane.** Rdzeń nie czyta ich sam.
- **Konfiguracja wczytywana raz, na starcie.** Przekazywana dalej jako jawny obiekt.
- **Kompozycja zamiast dziedziczenia.** Hierarchia klas tylko tam, gdzie narzuca ją framework.
- **Maksymalnie trzy warstwy.** Każda kolejna to koszt kontekstu i miejsce na pomyłkę.
- **Bez kontenerów DI, dekoratorów zmieniających zachowanie i metaprogramowania.** Jawne wywołania.

## Kod

- **Plik do około 300 linii, funkcja do około 30.** Limit pliku egzekwuje `scripts/check.py`.
- **Jedna nazwa na koncept w całym repo.** Bez synonimów; bez `data`, `manager`, `utils`, `helper`.
- **Bez flag w parametrach.** Wariant to osobna funkcja albo nazwany obiekt opcji.
- **Wczesne wyjścia, maksymalnie dwa poziomy zagnieżdżenia.**
- **Dane zamiast logiki.** Macierz przypadków jako tabela lub mapowanie, nie łańcuch `if`/`else`.
- **Niemutowalne struktury.** Funkcja zwraca nową wartość, nie zmienia wejścia.
- **Deterministyczna kolejność** w kolekcjach i w wyjściu, żeby diff był czytelny.
- **Wąskie API modułu.** Kilka funkcji publicznych, reszta prywatna.
- **Komentarz mówi o pułapce, nie o kodzie.** Nagłówek modułu: po co, co dostaje, co gwarantuje.

## Testy

- **Jeden test, jedna reguła.** Nazwa testu to zdanie o gwarantowanym zachowaniu.
- **Rdzeń testowany bez mocków.** Mock tylko na granicy, którą sami wyznaczyliśmy.
- **Test deterministyczny.** Bez prawdziwego zegara, sieci i losowości; inaczej wstrzyknięte.
- **Property i snapshot** tam, gdzie przypadków jest zbyt wiele na wyliczanie ręczne.
- **Przed zmianą starego kodu** powstaje test charakteryzujący obecne zachowanie.

## Zależności i narzędzia

- **Biblioteka standardowa przed pakietem.** Nowa zależność wymaga uzasadnienia.
- **Wersje przypięte, lock w repozytorium.**
- **Narzędzia w Pythonie przez `uv`**, testy w `pytest`.
- **Jedna komenda sprawdzająca** — `uv run python scripts/check.py`.
- **Formatowanie i lint w konfiguracji narzędzi**, nie w dokumentacji jako prośba.

## Czego nie robić

- **Nie buduj abstrakcji „na przyszłość”.** Wprowadzaj ją, gdy pojawi się drugi przypadek.
- **Nie dodawaj warstwy, żeby „oddzielić odpowiedzialności”.** Najpierw sprawdź, czy problem istnieje.
- **Nie wyciągaj wspólnego kodu, dopóki nie ma dwóch realnych użyć.**
- **Nie zmieniaj nazw i struktury w commicie naprawiającym błąd.**
- **Nie zostawiaj `TODO`.** Albo zrobione, albo zgłoszone jako niezrobione.
