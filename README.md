# ai_stuff

**Reguły, dzięki którym agent AI psuje mniej kodu — zapisane tak, żeby dało się je wyegzekwować, a nie tylko deklarować.**

![Licencja: MIT](https://img.shields.io/badge/licencja-MIT-blue)
![Dokumentacja: polski](https://img.shields.io/badge/dokumentacja-polski-red)
![Sprawdzenie: jedna komenda](https://img.shields.io/badge/sprawdzenie-jedna%20komenda-success)

Baza wiedzy o pisaniu i utrzymywaniu kodu z agentami AI. To nie aplikacja i nie framework:
zestaw zasad, dokumentów i skryptów, które kopiujesz do własnego projektu.

## Po co to istnieje

Model nie psuje kodu dlatego, że jest zły. Psuje go, bo działa pod presją kontekstu: gubi wątek,
dopowiada nieistniejące API, pomija wariant, naprawia jedną z dwóch kopii tej samej reguły, robi
„lokalną” zmianę w pięciu plikach. Każda reguła w tym repozytorium adresuje jeden z tych trybów
awarii. Reguła, która nie adresuje żadnego, nie ma tu czego szukać.

Założenie wyjściowe: **reguła, która żyje wyłącznie w prozie, jest prawdopodobieństwem, nie
gwarancją.** Dlatego każda reguła ma tu drogę w dół drabiny egzekwowania — od prozy, przez
checklistę i jedną komendę, do hooka, CI i uprawnień.

Zasady są niezależne od języka. Typy, kontrakty i obsługa błędów tłumaczą się na idiomy języka,
w którym powstaje projekt. Preferencja narzędziowa autora (Python, `uv`, `pytest` dla skryptów
pomocniczych) jest opisana osobno i nie jest zasadą architektury.

## Zacznij w minutę

```sh
git clone https://github.com/JonasWit/ai_stuff.git
cd ai_stuff
uv run python scripts/check.py
```

Ostatnia komenda sprawdza spójność repozytorium: wymagane pliki, martwe linki, zakazane
znaczniki, budżety rozmiaru plików i testy projektu.

## Wybierz swoją ścieżkę

| Chcę… | Zacznij od |
| --- | --- |
| poznać reguły i ich uzasadnienia | [`docs/zasady-ai.md`](docs/zasady-ai.md) |
| wdrożyć je w swoim projekcie | [`AGENTS.md`](AGENTS.md), potem [`docs/jak-pisac-agents-md.md`](docs/jak-pisac-agents-md.md) |
| zobaczyć, jak wygląda dobry kod | [`examples/kotlin/`](examples/kotlin/README.md) |
| sprawdzić, czy model naprawdę ich przestrzega | [`docs/testy-instrukcji.md`](docs/testy-instrukcji.md) |
| zobaczyć, co jest wymuszane maszynowo | [`scripts/check.py`](scripts/check.py) |

## Co jest w środku

```
docs/            wiedza: zasady, dystrybucja do AGENTS.md, decyzje, sondy
examples/kotlin/ złoty przykład czystego rdzenia (TimerEngine)
scripts/         jedna komenda sprawdzająca + testy w pytest
.githooks/       hook commit-msg wymagający dowodu w commicie
.github/         szablon pull requesta z definicją „gotowe”
```

## Preferowane wybory

### Nienegocjowalne

- **Test przed kodem.** Zawsze, poza zmianami bez wykonywalnego zachowania.
- **Twierdzenie wymaga testu.** Sąd („to czytelniejsze”) oznaczaj jako sąd, nie jako dowód.
- **Jedna zmiana, jeden cel.** Bez refaktorów przy okazji.

### Architektura

- **Funkcjonalny rdzeń, cienka skorupa I/O.** Logika nie wie, że istnieje sieć, zegar czy plik.
- **Zależności w jedną stronę.** Adaptery i UI znają rdzeń; rdzeń nie zna ich nigdy.
- **Granica walidacji raz.** Dane z zewnątrz zamieniane na wąski typ na wejściu, dalej bez sprawdzeń.
- **Moduły według domeny, nie według typu.** `zamowienia/`, nie `services/` + `models/` + `controllers/`.
- **Warianty jako zamknięte typy z wyczerpującym dopasowaniem.** Zapomniany przypadek = błąd kompilacji; w językach bez sum typów — `enum` plus test wyczerpujący warianty.
- **Błędy jako wartości w rdzeniu.** `Result`/`Either`, a gdy język nie ma typowanego wyniku — jawny typ błędu w sygnaturze. Wyjątki tylko na granicy.
- **Stan jawny, przekazywany argumentem.** Żadnych globali, singletonów ani mutowalnych modułów.
- **Czas, losowość, identyfikatory i sieć wstrzykiwane.** Rdzeń nie czyta ich sam.
- **Konfiguracja wczytywana raz, na starcie.** Przekazywana dalej jako jawny obiekt.
- **Kompozycja zamiast dziedziczenia.** Hierarchia klas tylko tam, gdzie narzuca ją framework.
- **Maksymalnie trzy warstwy.** Każda kolejna to koszt kontekstu i miejsce na pomyłkę.
- **Bez kontenerów DI, dekoratorów zmieniających zachowanie i metaprogramowania.** Jawne wywołania.

### Kod

- **Plik do około 300 linii, funkcja do około 30.** To konwencja projektu, nie wynik pomiaru; limit pliku egzekwuje [`scripts/check.py`](scripts/check.py).
- **Jedna nazwa na koncept w całym repo.** Bez synonimów; bez `data`, `manager`, `utils`, `helper`.
- **Bez flag w parametrach.** Wariant to osobna funkcja albo nazwany obiekt opcji.
- **Wczesne wyjścia, maksymalnie dwa poziomy zagnieżdżenia.**
- **Dane zamiast logiki.** Macierz przypadków jako tabela lub mapowanie, nie łańcuch `if`/`else`.
- **Niemutowalne struktury.** Funkcja zwraca nową wartość, nie zmienia wejścia.
- **Deterministyczna kolejność** w kolekcjach i w wyjściu, żeby diff był czytelny.
- **Wąskie API modułu.** Kilka funkcji publicznych, reszta prywatna.
- **Komentarz mówi o pułapce, nie o kodzie.** Nagłówek modułu: po co, co dostaje, co gwarantuje.

### Testy

- **Jeden test, jedna reguła.** Nazwa testu to zdanie o gwarantowanym zachowaniu.
- **Rdzeń testowany bez mocków.** Mock tylko na granicy, którą sami wyznaczyliśmy.
- **Test deterministyczny.** Bez prawdziwego zegara, sieci i losowości; inaczej wstrzyknięte.
- **Property i snapshot** tam, gdzie przypadków jest zbyt wiele na wyliczanie ręczne.
- **Przed zmianą starego kodu** powstaje test charakteryzujący obecne zachowanie.

### Zależności i narzędzia

- **Biblioteka standardowa przed pakietem.** Nowa zależność wymaga uzasadnienia.
- **Wersje przypięte, lock w repozytorium.**
- **Jeden toolchain dla narzędzi.** Żadnego drugiego systemu budowania obok istniejącego.
- **Jedna komenda sprawdzająca** w projekcie, niezależnie od języka.
- **Formatowanie i lint w konfiguracji narzędzi**, nie w dokumentacji jako prośba.

### Preferencja autora, nie architektura

- **Skrypty pomocnicze i ich testy w Pythonie**, środowisko i wersje przez `uv`, testy w `pytest`.
- Wybór dotyczy narzędzi, nie kodu projektu. Projekt z własnym toolchainem zachowuje swój.

### Czego nie robić

- **Nie buduj abstrakcji „na przyszłość”.** Wprowadzaj ją, gdy pojawi się drugi przypadek.
- **Nie dodawaj warstwy, żeby „oddzielić odpowiedzialności”.** Najpierw sprawdź, czy problem istnieje.
- **Nie wyciągaj wspólnego kodu, dopóki nie ma dwóch realnych użyć.**
- **Nie zmieniaj nazw i struktury w commicie naprawiającym błąd.**
- **Nie zostawiaj `TODO`.** Albo zrobione, albo zgłoszone jako niezrobione.

## Złoty przykład

[`examples/kotlin/`](examples/kotlin/README.md) — `TimerEngine` z projektu `workoutbase` jako
wzorzec czystego rdzenia: niemutowalny stan, czas jako argument, wyczerpujące dopasowanie
wariantów i testy pisane jak specyfikacja.

```kotlin
@Test
fun tick_throughPrepare_movesToFirstWorkRound() { … }

fun tick(state: TimerState, deltaMillis: Long): TimerTransition
```

Rdzeń nie czyta zegara — dostaje upływ czasu jako argument i zwraca nowy stan razem z listą
sygnałów do odegrania. Dzięki temu test nie potrzebuje prawdziwego czasu ani Androida.

## Dokumenty

| Plik | Na jakie pytanie odpowiada |
| --- | --- |
| [`docs/zasady-ai.md`](docs/zasady-ai.md) | Jakich reguł przestrzegać przy pisaniu kodu i dlaczego zmniejszają one liczbę błędów modelu |
| [`docs/jak-pisac-agents-md.md`](docs/jak-pisac-agents-md.md) | Jak przenieść tę wiedzę do `AGENTS.md` / `CLAUDE.md`, żeby naprawdę działała |
| [`docs/wzorce.md`](docs/wzorce.md) | Dziennik decyzji: problem, decyzja, odrzucone alternatywy, konsekwencje |
| [`docs/testy-instrukcji.md`](docs/testy-instrukcji.md) | Sondy, które próbują złamać reguły, żeby ustalić, które faktycznie wiążą |
| [`AGENTS.md`](AGENTS.md) | Plik instrukcji, który agent czyta automatycznie w tym repozytorium |

## Egzekwowanie

| Mechanizm | Co blokuje |
| --- | --- |
| [`scripts/check.py`](scripts/check.py) | Brakujące dokumenty, martwe linki, zakazane znaczniki, zbyt duże pliki, nieprzechodzące testy projektu |
| `uv run pytest` | Regresje w samym skrypcie sprawdzającym |
| `.githooks/commit-msg` | Commity bez linii `Test:` albo `Unverified:` |
| `.github/pull_request_template.md` | Pull requesty, które pomijają definicję „gotowe” |

Włącz hooki raz na klon:

```sh
git config core.hooksPath .githooks
```

Uruchom sprawdzenie (wraz z testami projektu, jeśli istnieje `pyproject.toml`):

```sh
uv run python scripts/check.py
```

Uruchom same testy skryptu sprawdzającego:

```sh
uv run pytest
```

## Jak użyć tego w nowym projekcie

- Skopiuj [`AGENTS.md`](AGENTS.md) oraz te dokumenty z `docs/`, które pasują do projektu.
- Trzymaj reguły normatywne w jednym miejscu i linkuj do nich; nigdy nie kopiuj pełnej treści dwa razy.
- Dodaj komendy specyficzne dla stacku i konfigurację narzędzi w tej samej zmianie, żeby reguły stały się wykonywalne, a nie aspiracyjne.
- Napisz złoty przykład w języku pierwszego projektu, nie wcześniej.
- Uruchom sondy z [`docs/testy-instrukcji.md`](docs/testy-instrukcji.md), gdy reguły będą już na miejscu.

## Licencja

MIT — szczegóły w pliku [`LICENSE`](LICENSE). O ile w podkatalogu nie zaznaczono inaczej,
treści są udostępniane na tej licencji.
