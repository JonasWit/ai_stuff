# ai_stuff

Baza wiedzy o pisaniu i utrzymywaniu kodu z agentami AI: które reguły zmniejszają liczbę
błędów modelu, dlaczego działają i jak je zapisać, żeby agent faktycznie ich przestrzegał.
To nie jest aplikacja i nie ma tu kodu projektowego.

Założenie wyjściowe: reguła, która żyje wyłącznie w prozie, jest prawdopodobieństwem, nie
gwarancją. Każda reguła opisana tutaj powinna docelowo przesunąć się w dół drabiny
egzekwowania — do komendy, hooka, CI albo uprawnień.

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
| `scripts/check.py` | Brakujące dokumenty, martwe linki, zakazane znaczniki, zbyt duże pliki, nieprzechodzące testy projektu |
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

- Skopiuj `AGENTS.md` oraz te dokumenty z `docs/`, które pasują do projektu.
- Trzymaj reguły normatywne w jednym miejscu i linkuj do nich; nigdy nie kopiuj pełnej treści dwa razy.
- Dodaj komendy specyficzne dla stacku i konfigurację narzędzi w tej samej zmianie, żeby reguły stały się wykonywalne, a nie aspiracyjne.
- Napisz złoty przykład w języku pierwszego projektu, nie wcześniej.
- Uruchom sondy z `docs/testy-instrukcji.md`, gdy reguły będą już na miejscu.

## Licencja

O ile w podkatalogu nie zaznaczono inaczej, treści są udostępniane na licencji MIT.
