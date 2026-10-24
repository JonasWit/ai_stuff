# Dziennik decyzji o wzorcach

## Po co ten plik

Reguła „nowy wzorzec tylko z zapisem” bez miejsca zapisu kończy się tym, że wzorce powstają
w kodzie, a wiedza o nich w niczyjej głowie. Ten plik jest tym miejscem.

Wpis jest krótki i odpowiada na cztery pytania: jaki był problem, co postanowiono, co odrzucono
i co to za sobą pociąga. Nie jest esejem i nie jest dokumentacją — jest śladem decyzji.

## Kiedy dopisać wpis

- wprowadzasz wzorzec, którego nie ma jeszcze w repozytorium
- zmieniasz istniejący wzorzec
- świadomie odrzucasz alternatywę, która będzie wracać w rozmowach
- łamiesz regułę z `docs/zasady-ai.md` i masz do tego powód

## Szablon wpisu

```markdown
### Nazwa decyzji

**Status:** przyjęte | odrzucone | do rewizji

**Problem:** jedno zdanie o tym, co wymagało rozstrzygnięcia.

**Decyzja:** co postanowiono, w trybie rozkazującym.

**Odrzucone alternatywy:** co rozważano i dlaczego odpadło.

**Konsekwencje:** co to oznacza dla przyszłych zmian, czego nie wolno robić.
```

## Decyzje

### Repozytorium jako baza wiedzy, nie projekt

**Status:** przyjęte

**Problem:** reguły stylu i architektury dla AI są rozproszone po rozmowach, notatkach i plikach
konfiguracyjnych różnych narzędzi. Trzeba miejsce, które jest źródłem prawdy.

**Decyzja:** to repozytorium przechowuje wiedzę o architekturze i stylu kodu pod kątem pracy
z modelami językowymi oraz instrukcje, jak tę wiedzę przenosić do `AGENTS.md` i `CLAUDE.md`.
Kod projektów trafia gdzie indziej.

**Odrzucone alternatywy:** trzymanie reguł tylko w globalnym pliku instrukcji — nie da się
wersjonować ani uzasadniać; trzymanie ich w notatkach poza repozytorium — brak historii zmian.

**Konsekwencje:** dokumenty w `docs/` są kanoniczne. Globalny plik instrukcji jest ich
zdestylowaną wersją i nie może zawierać treści sprzecznych.

### Dokument normatywny oddzielony od streszczenia

**Status:** przyjęte

**Problem:** pełne uzasadnienia są za długie na kontekst startowy, a krótkie streszczenie nie
wystarcza do rozstrzygania sporów.

**Decyzja:** `docs/zasady-ai.md` jest źródłem kanonicznym. Plik `AGENTS.md` w repozytorium
zawiera streszczenie i link, a nie kopię.

**Odrzucone alternatywy:** jedno wielkie `AGENTS.md` — rozwadnia uwagę i wypada przy
kompaktowaniu kontekstu; same linki bez streszczenia — model nie ma powodu zajrzeć do środka.

**Konsekwencje:** zmiana reguły wymaga sprawdzenia obu miejsc. Duplikat pełnej treści jest
błędem.

### Zamknięta lista wyjątków od testu przed kodem

**Status:** przyjęte

**Problem:** reguła „test zawsze” bez listy wyjątków jest w praktyce nierespektowana, bo model
sam sobie znajduje usprawiedliwienie. Reguła z otwartą listą jest równie łatwa do obejścia.

**Decyzja:** wyjątki są wymienione enumeratywnie: dokumentacja, komentarze, komunikaty
commitów, formatowanie wymuszane narzędziem. Agent musi wskazać pozycję z listy, z której
korzysta.

**Odrzucone alternatywy:** „rozsądek agenta” — nieprzewidywalne; brak wyjątków — reguła
niespełnialna przy zmianie samego dokumentu.

**Konsekwencje:** nowy wyjątek wymaga wpisu w tym dzienniku i zmiany dokumentu. Rozszerzanie
listy w rozmowie jest niedozwolone.

### Dziennik decyzji zamiast katalogu wzorców

**Status:** przyjęte

**Problem:** katalog wzorców opisuje, co istnieje. Nie mówi, dlaczego istnieje i czego nie
wybrano, więc martwe wzorce żyją wiecznie, a odrzucone pomysły wracają.

**Decyzja:** wzorce są zapisywane jako decyzje z problemem, alternatywami i konsekwencjami,
w tym pliku.

**Odrzucone alternatywy:** katalog wzorców w stylu podręcznikowym — brak historii decyzji;
brak jakiegokolwiek zapisu — wiedza znika po sesji.

**Konsekwencje:** wpis bez odrzuconych alternatyw jest niekompletny, bo nie chroni przed
powrotem odrzuconego pomysłu.

### Złoty przykład dopiero przy pierwszym stacku

**Status:** przyjęte

**Problem:** przykład referencyjny jest najskuteczniejszym nośnikiem stylu, ale napisany
w zgadywanym języku uczy nie tego, co trzeba.

**Decyzja:** wzorcowy moduł powstaje w języku pierwszego realnego projektu, razem z jego
konfiguracją narzędzi.

**Odrzucone alternatywy:** przykład w TypeScripcie lub Pythonie już teraz — ryzyko, że stack
będzie inny; przykład pseudokodowy — nie da się uruchomić, więc nie jest testowalny.

**Konsekwencje:** do czasu pierwszego projektu reguły są wyłącznie opisowe, a ich egzekwowanie
ogranicza się do `scripts/check.py`, hooka i szablonu PR.

### Skrypt sprawdzający bez zależności od stacku

**Status:** przyjęte

**Problem:** bez stacku nie ma czego uruchamiać, więc „jedna komenda” mogłaby nie istnieć
przez wiele tygodni — a reguła bez komendy jest prozą.

**Decyzja:** `scripts/check.py` sprawdza to, co jest sprawdzalne zawsze: wymagane pliki,
martwe linki w dokumentach, zakazane znaczniki, budżet rozmiaru pliku. Po pojawieniu się stacku
ta sama komenda uruchomi jego testy.

**Odrzucone alternatywy:** czekanie na stack — reguła bez egzekwowania; ciężki runner zależny
od Node — sprzeczny z minimalizmem zależności.

**Konsekwencje:** skrypt ma własne testy w `scripts/tests/`, uruchamiane przez `uv run pytest`.
Każde nowe sprawdzenie wymaga testu.

### Skrypty i testy w Pythonie zarządzanym przez uv

**Status:** przyjęte jako preferencja autora

**Problem:** narzędzia pomocnicze trzeba uruchamiać jedną komendą na każdej maszynie, bez
ręcznego instalowania interpretera i bibliotek. Pierwsza wersja była w PowerShellu, co wiązało
narzędzia z Windowsem i utrudniało testowanie.

**Decyzja:** skrypty pomocnicze i ich testy w tym repozytorium są w Pythonie. Środowisko i wersje
zarządza `uv`, testy piszemy w `pytest` i uruchamiamy przez `uv run pytest`. Zależności deklaruje
`pyproject.toml`, wersje są przypięte w `uv.lock`. To wybór narzędzia, nie zasada architektury.

**Odrzucone alternatywy:** PowerShell — tylko Windows, brak wygodnego frameworka testowego;
Node — drugi toolchain obok Pythona; globalny `pip` — niedeterministyczne środowisko, zależne
od tego, co już jest zainstalowane.

**Konsekwencje:** każdy nowy skrypt ma test w `scripts/tests/`. Uruchomienie nie wymaga
aktywowania środowiska ani ręcznej instalacji zależności. Reguły architektoniczne pozostają
niezależne od języka; projekt z własnym toolchainem zachowuje swój.

### Podsumowanie dla człowieka w README

**Status:** przyjęte

**Problem:** jednostronicowe podsumowanie wyborów w osobnym pliku wymagało dodatkowego kliknięcia,
a przy wejściu do repozytorium człowiek i tak otwiera `README.md`.

**Decyzja:** podsumowanie preferowanych wyborów mieszka w `README.md`. Dokumenty w `docs/`
zawierają uzasadnienia, szczegóły i dziennik decyzji.

**Odrzucone alternatywy:** osobny plik w `docs/` — dodatkowy krok i ryzyko rozjazdu; brak
podsumowania — wejście wymaga czytania całego dokumentu.

**Konsekwencje:** `README.md` jest jedynym miejscem na skrót. Zmiana reguły wymaga sprawdzenia
`README.md` i `docs/zasady-ai.md`.

### Złoty przykład z workoutbase

**Status:** przyjęte — zastępuje wcześniejszą decyzję „złoty przykład dopiero przy pierwszym stacku”

**Problem:** reguły opisowe nie pokazują, jak wygląda ich realizacja w prawdziwym kodzie, a stack
pierwszego projektu już istnieje: Kotlin w `workoutbase`.

**Decyzja:** `examples/kotlin/` zawiera `TimerEngine` i jego testy skopiowane z `workoutbase` bez
zmian, z opisem, co ilustrują i czego w tym katalogu nie ma.

**Odrzucone alternatywy:** napisanie nowego przykładu od zera — duplikowałoby istniejący, sprawdzony
kod; trzymanie przykładu wyłącznie w `workoutbase` — wiedza nie byłaby dostępna poza tym projektem.

**Konsekwencje:** przykład jest referencją, nie budowanym modułem. Zmiana zasad wymaga sprawdzenia,
czy przykład nadal je ilustruje.
