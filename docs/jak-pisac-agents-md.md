# Jak zapisywać wiedzę w AGENTS.md i CLAUDE.md

## Po co ten dokument

Ten dokument opisuje, jak przenosić wiedzę o architekturze i stylu kodu do plików, które agent
czyta automatycznie. Reguły merytoryczne są w [`docs/zasady-ai.md`](zasady-ai.md); tutaj jest
wyłącznie warstwa dystrybucji: **co gdzie trafia, w jakiej formie i co to czyni sprawdzalnym**.

Punkt wyjścia jest niewygodny: plik instrukcji nie jest dokumentacją. Nikt go nie czyta dla
przyjemności. Model czyta go w całości, raz, na początku sesji, i potem działa pod presją
ograniczonego kontekstu. Dokument, który wymaga uważnej lektury, jest dokumentem, który nie
zadziała.

## Zasada nadrzędna

**Instrukcja to nie dokumentacja.** Dokumentacja wyjaśnia. Instrukcja rozkazuje i podaje
sposób sprawdzenia. Zdanie, którego nie da się zweryfikować, jest w instrukcji balastem —
zajmuje miejsce i obniża wagę pozostałych zdań.

Praktyczna konsekwencja: uzasadnienia, przykłady i filozofia żyją w `docs/`. W plikach
instrukcji zostaje tylko to, co musi być w kontekście od pierwszej sekundy.

## Trzy poziomy

### Poziom globalny

`~/.config/opencode/AGENTS.md` (OpenCode) albo `~/.claude/CLAUDE.md` (Claude Code). Wchodzi do
kontekstu w każdym projekcie. Miejsce na reguły uniwersalne, niezależne od stacku: dyscyplina
testów, czystość rdzenia, proces pracy, reguły komunikacji. Nic, co dotyczy jednego projektu.

Budżet: kilkadziesiąt linii. Każda dodatkowa linia to koszt w każdej sesji i mniejsza waga
pozostałych reguł.

### Poziom repozytorium

`AGENTS.md` albo `CLAUDE.md` w katalogu głównym. Wchodzi do kontekstu przy pracy w tym repo.
Miejsce na: strukturę katalogów, komendy (test, check, build), specyfikę stacku, odwołanie do
dokumentów z wiedzą, lokalne zaostrzenia reguł globalnych.

Budżet: do około osiemdziesięciu linii. Jeśli rośnie więcej, treść należy przenieść do `docs/`
i zostawić link oraz streszczenie.

### Poziom wiedzy

Katalog `docs/`: `zasady-ai.md`, `wzorce.md`, `testy-instrukcji.md`, ten plik. Nie jest
wczytywany automatycznie, więc **musi być linkowany z pliku instrukcji, w pierwszej części**.
Wiedza, do której nie prowadzi link, nie istnieje dla modelu.

Tu wolno być długim, bo tu trafia się świadomie, na żądanie.

### Warstwa skills

Procedury ładowane na żądanie: „jak dodać nowy wzorzec”, „jak przeprowadzić audyt reguł”.
Zaleta — nie zajmują kontekstu, dopóki nie są potrzebne. Wada — trzeba je wywołać, więc nie
nadają się na reguły, które mają obowiązywać zawsze. Reguły krytyczne zostają w plikach
instrukcji; skills są dla czynności, nie dla zakazów.

## Co gdzie trafia

| Treść | Miejsce | Dlaczego |
| --- | --- | --- |
| Test przed kodem, zakaz twierdzeń bez dowodu | globalny | obowiązuje w każdym projekcie |
| Czysty rdzeń, efekty na brzegach | globalny | niezależne od stacku |
| Komendy test/check/lint | repozytorium | zależą od projektu |
| Struktura katalogów i konwencje nazw | repozytorium | lokalna wiedza |
| Uzasadnienia i przykłady | `docs/` | za długie na kontekst startowy |
| Decyzje o wzorcach | `docs/wzorce.md` | historia, nie instrukcja |
| Procedura rzadkiej czynności | skill | ładowana na żądanie |
| Preferencje użytkownika co do komunikacji | globalny | niezależne od projektu |

## Forma, która działa

### Rozkaźnik i jedna reguła na punkt

„Pisz test przed kodem” działa. „Należy rozważyć, czy w danym przypadku zasadnym byłoby
rozpoczęcie prac od napisania testu” nie działa. Jedna reguła na punkt, bez akapitów
wielozdaniowych.

### Najważniejsze na początku

Pierwsze kilkanaście linii ma największą wagę. Jeśli kontekst zostanie ucięty albo streszczony,
ocalały ma być zakazy, nie filozofia.

### Falsyfikowalność

Każda reguła powinna odpowiadać na pytanie „po czym poznam, że została złamana”. Reguła bez
takiego kryterium jest życzeniem.

### Stała kolejność sekcji

Ustalona kolejność: weryfikacja i testy, reguły projektowe, proces pracy, język i komunikacja.
Model uczy się układu i szybciej znajduje właściwy fragment. Zmiana kolejności przy każdej
edycji niszczy tę korzyść.

### Zakaz przymiotników bez kryterium

„Czysty kod”, „profesjonalny”, „solidny”, „zgodny z najlepszymi praktykami” — każdy model
rozumie je inaczej i żaden nie da się sprawdzić. Zamiast tego: konkretny warunek i sposób
weryfikacji.

### Jedna reguła, jedno miejsce

Ta sama zasada w globalnym pliku, w pliku repo i w `docs/` to trzy wersje, które z czasem się
rozjadą. Obowiązuje: źródło kanoniczne w `docs/`, streszczenie w pliku instrukcji, żadnych
kopii pełnej treści.

## Czego nie robić

### Nie licz na to, że model zajrzy do `docs/`

Plik nie jest wczytywany automatycznie. Bez linku na górze pliku instrukcji wiedza w `docs/`
jest niedostępna, choć formalnie istnieje.

### Nie mieszaj języków w plikach instrukcji

Jeden język na plik. Mieszanie powoduje, że model odpowiada w języku przypadkowym, a przy
edycjach powstają hybrydy zdań.

### Nie pisz reguł, których nie da się sprawdzić

Reguła bez mechanizmu weryfikacji jest dekoracją, a dekoracje uczą model, że reguły są
niewiążące.

### Nie duplikuj pełnej treści

Streszczenie w pliku instrukcji i źródło w `docs/`. Kopia pełnej treści w dwóch miejscach to
gwarantowana sprzeczność.

### Nie zostawiaj martwych reguł

Reguła, która od miesięcy nie została użyta ani złamana, zajmuje kontekst i rozwadnia resztę.
Audyt oznacza także usuwanie.

## AGENTS.md

### Jak to działa w OpenCode

`AGENTS.md` z katalogu roboczego i z katalogów nadrzędnych jest wczytywany automatycznie,
podobnie jak plik globalny z katalogu konfiguracji. Zmiana pliku w trakcie sesji jest
odświeżana, więc edycja reguł działa bez restartu.

Dodatkowo konfiguracja pozwala wskazać pliki instrukcji jawnie oraz definiować agentów
i skills. Skills są ładowane na żądanie, więc nie zastępują reguł w `AGENTS.md`.

### Subagenty

Subagent startuje z czystym kontekstem. Dziedziczy pliki instrukcji z katalogu, ale nie
dziedziczy ustaleń z rozmowy. Reguły krytyczne dla zadania trzeba powtórzyć w promptcie
subagenta; poleganie na tym, że „przeczyta AGENTS.md”, jest założeniem, nie gwarancją.

### Kompaktowanie kontekstu

W długiej sesji historia bywa streszczana. Reguły, które nie były użyte od dawna, wypadają
pierwsze. Dlatego plik instrukcji ma być krótki i mieć najważniejsze reguły na górze, a nie
dlatego, że „tak jest estetyczniej”.

## CLAUDE.md

### Jak to działa w Claude Code

Claude Code wczytuje `CLAUDE.md` automatycznie: wersję projektową z katalogu głównego oraz
wersję globalną z katalogu konfiguracji użytkownika. Obsługuje też importy innych plików przez
składnię `@ścieżka`, co pozwala trzymać długą treść poza plikiem głównym, zachowując ją
w kontekście.

Pliki `CLAUDE.md` mogą istnieć w podkatalogach i są dołączane przy pracy w danym obszarze
repozytorium — to dobre miejsce na wiedzę lokalną, na przykład o jednym module.

### Różnica względem AGENTS.md

Model dystrybucji jest podobny, więc treść można utrzymywać wspólnie. Jeśli repo używa obu
plików, jeden jest źródłem, drugi odsyła do niego importem albo linkiem. Dwie niezależne
kopie to najczęstszy powód rozjazdu reguł między narzędziami.

### Co przenieść z AGENTS.md

Wszystko, co dotyczy zakazów i weryfikacji. To, co specyficzne dla OpenCode — nazwy narzędzi,
skille, konfiguracja agentów — zostaje w `AGENTS.md` albo w pliku konfiguracyjnym, bo w Claude
Code nie ma odpowiednika.

## Drabina egzekwowania

Kolejne szczeble mają coraz większą moc. Reguła powinna stać najniżej, jak to możliwe, ale
nie niżej, niż wymaga jej stawka.

- **Proza** — model może pominąć. Wystarczy dla preferencji i sądów.
- **Checklista** — wymaga od agenta przejścia punkt po punkcie. Działa, dopóki nikt nie
  odhaczy bezmyślnie.
- **Komenda** — jedna komenda daje surowy wynik. Agent musi go pokazać.
- **Hook** — commit bez wymaganego pola nie powstaje. Obejście istnieje, ale jest widoczne.
- **CI** — wynik blokuje merge, niezależnie od dobrej woli modelu i człowieka.
- **Wymagany status i ochrona gałęzi** — czerwone nie wejdzie, nawet przez `--no-verify`.
- **Uprawnienia** — agent fizycznie nie może wykonać operacji. Najmocniejsze, najbardziej
  niewygodne.

Reguła testowa należy co najmniej do szczebla komendy. Reguła dotycząca commitów należy do
hooka. Reguła dotycząca merge — do CI i ochrony gałęzi.

## Szablon pliku instrukcji

Poniższy szkielet jest punktem startowym dla nowego repozytorium. Kolejność sekcji jest częścią
kontraktu.

```markdown
# Agent Instructions

Read docs/<zasady>.md before writing code.

## Verification and tests

- Test before code, no exceptions except changes with no executable behavior.
- Watch the test fail before implementing.
- No claim without a test; otherwise mark it "unverified".
- Run `./scripts/check` and paste the raw output.

## Design rules

- Pure core, side effects in thin adapters.
- Closed types with exhaustive matching.
- One source of truth per rule, one name per concept.
- No inheritance, no metaprogramming, no DI containers.

## Working process

- Follow the existing pattern in this repository.
- Document a new pattern in the same change.
- Ask when the requirement is ambiguous.
- One change, one purpose.

## Structure and commands

- Test command: ...
- Check command: ...
- Source layout: ...

## Precedence

Global instructions provide defaults. This file tightens them. When they conflict, the more
specific and more restrictive rule wins; this file may not loosen a global rule.
```

## Checklista walidacji

Przed uznaniem pliku instrukcji za gotowy sprawdź:

- Czy pierwsze kilkanaście linii zawiera reguły, których złamanie jest najdroższe?
- Czy każda reguła mówi, po czym poznać, że została złamana?
- Czy żadna reguła nie wymaga przeczytania innego pliku, żeby ją zrozumieć?
- Czy każda dłuższa treść jest w `docs/`, a w pliku instrukcji jest link na górze?
- Czy nie ma duplikatu pełnej treści w dwóch plikach?
- Czy komendy podane w pliku faktycznie istnieją i przechodzą w czystym klonie?
- Czy plik zmieściłby się w jednym ekranie?

## Utrzymanie

Zmiana reguły to zmiana w źródle kanonicznym plus, jeśli trzeba, w streszczeniu. Nowy wzorzec
dopisuje się do [`docs/wzorce.md`](wzorce.md). Skuteczność reguł sprawdza się sondami z
[`docs/testy-instrukcji.md`](testy-instrukcji.md). Reguła, która nie przechodzi sondy, wymaga
przeniesienia na wyższy szczebel drabiny egzekwowania albo usunięcia.
