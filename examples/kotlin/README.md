# Złoty przykład: TimerEngine (Kotlin)

Wzorzec czystego rdzenia w Kotlinie, skopiowany bez zmian z projektu `workoutbase`.

## Co pokazuje

- **Niemutowalny stan** — `TimerState` i `TimerConfig` są `data class`, a każda operacja
  zwraca nowy stan zamiast zmieniać istniejący.
- **Czas jako argument** — `tick(state, deltaMillis)` nie czyta zegara, więc testy nie
  potrzebują prawdziwego czasu.
- **Zamknięte warianty** — `TimerPhase` i `TimerCue` to enumy, a `when` w silniku jest
  wyczerpujące; nowy wariant to błąd kompilacji, nie cicha luka.
- **Walidacja na granicy** — `TimerConfig` sprawdza zakresy w `init`, więc dalej rdzeń
  nie powtarza tych samych warunków.
- **Wynik jako wartość** — `TimerTransition` zwraca nowy stan razem z listą sygnałów,
  które trzeba odegrać; rdzeń nie wie, że istnieje dźwięk czy wibracja.
- **Testy jako specyfikacja** — nazwy testów są zdaniami o gwarantowanym zachowaniu,
  jeden test odpowiada jednej regule, zero mocków.

## Jak czytać

Najpierw `TimerEngineTest.kt`, potem `TimerEngine.kt`. Testy mówią, co timer ma robić;
implementacja pokazuje, jak zbudować to bez efektów ubocznych.

## Czego ten katalog nie robi

Nie jest budowany ani uruchamiany w tym repozytorium. Nie ma tu toolchainu Kotlina —
pliki są referencją do czytania i kopiowania. Aby je uruchomić, potrzebny jest projekt
Kotlin z JUnit, taki jak `workoutbase`.

## Pochodzenie i utrzymanie

Pliki pochodzą z aplikacji `workoutbase` (pakiet `com.wtk_apps.workoutbase.timer`).
Przy zmianie zasad w `docs/zasady-ai.md` sprawdź, czy przykład nadal je ilustruje;
jeśli nie, popraw przykład w tej samej zmianie.
