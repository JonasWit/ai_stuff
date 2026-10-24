# Zasady pisania kodu z AI

Ten dokument opisuje, jak pisać kod w tym repozytorium, żeby praca z modelem językowym
była przewidywalna. Nie jest zbiorem ludzkich „dobrych praktyk”. Jest zbiorem reguł
dobranych pod jeden cel: **mniej błędów popełnianych przez AI oraz tańsze i bezpieczniejsze
późniejsze zmiany**.

## Jak czytać ten dokument

Każda reguła odpowiada na realny tryb awarii modelu językowego: zgubienie kontekstu,
dopowiedzenie nieistniejącego API, pominięcie przypadku, naprawienie jednej kopii reguły
z dwóch, zmiana, która „wygląda na lokalną”, a dotyka pięciu plików. Reguła, która nie
adresuje żadnego z tych trybów, nie ma tu czego szukać.

Dokument jest normatywny. Jeśli kod i dokument się różnią, kod jest błędem — chyba że
zmiana została świadomie zapisana tutaj.

## Precedencja

Globalny `AGENTS.md` użytkownika daje domyślne podejście. Ten dokument je doprecyzowuje
i zaostrza dla potrzeb tego repozytorium.

Obowiązuje reguła: **bardziej szczegółowy i bardziej restrykcyjny wygrywa**. Ten dokument
może więc dodać wymóg, którego nie ma globalnie, ale nie może rozluźnić reguły globalnej —
na przykład nie może znieść obowiązku testu przed kodem.

## Miary, którymi oceniamy każdy wzorzec

### Koszt kontekstu

Ile tokenów i ile plików trzeba przeczytać, żeby zrobić poprawną zmianę. Wzorzec, który
wymaga przeczytania połowy repozytorium, jest zły — niezależnie od tego, jak czysto wygląda.

### Lokalność zmiany

Ile miejsc trzeba dotknąć, gdy zmienia się jedno wymaganie. Dobra odpowiedź to jedno
miejsce. Jeśli nowy przypadek wymaga edycji w pięciu plikach i pamiętania o dwóch
inwariantach, wzorzec jest wrogi wobec AI.

### Wykrywalność błędu

Czy pomyłka wywali kompilator albo test, czy przejdzie cicho. Preferujemy rozwiązania,
w których zapomniany przypadek jest błędem kompilacji, a nie zachowaniem, które „jakoś
działa” do pierwszego uruchomienia na produkcji.

Wzorzec, który jest elegancki po ludzku, ale wymaga trzymania w głowie globalnych
inwariantów rozsianych po wielu plikach, jest tutaj odrzucany — nawet jeśli w code review
wypada dobrze.

## Rdzeń stylu

### Czyste funkcje

Funkcje mają być deterministyczne i wolne od efektów ubocznych. Te same argumenty zawsze
dają ten sam wynik. Czytając sygnaturę, powinno dać się powiedzieć, co funkcja robi, nie
czytając jej ciała.

### Stan jako argument, nowa wartość zamiast mutacji

Funkcja, która potrzebuje stanu, dostaje go jako argument i zwraca nową wartość. Nie mutuje
stanu współdzielonego. Brak mutacji oznacza brak ukrytej kolejności wywołań — a ukryta
kolejność to jeden z najczęstszych błędów modelu przy edycji istniejącego kodu.

### Efekty uboczne w cienkich adapterach

I/O, sieć, system plików, zegar, losowość, zmienne środowiskowe — wszystko to siedzi
w cienkich wrapperach na brzegach modułu. Rdzeń logiki nie wie, że one istnieją. Dzięki
temu testy rdzenia nie potrzebują mocków, a model nie wplata `fetch` w środek obliczeń.

## Testy

### Test przed kodem, bez wyjątków

Przed wygenerowaniem jakiegokolwiek kodu powstaje test. Kolejność jest stała: failing test,
potem implementacja, potem refaktor. Nie ma „najpierw napiszę, potem dopiszę testy” —
test dopisany po fakcie opisuje kod, który już istnieje, więc niczego nie sprawdza.

### Zamknięta lista wyjątków

Wyjątek obowiązuje tylko dla zmian, które **nie mają wykonywalnego zachowania**:

- treść dokumentacji, w tym ten plik i `README.md`
- komentarze
- komunikaty commitów i opisy zmian
- formatowanie i układ pliku wymuszane przez narzędzie

Lista jest zamknięta. „Trudno napisać test”, „zmiana jest oczywista”, „to tylko rename”,
„to tylko mała poprawka” nie są wyjątkami — to są zdania, które model wypowiada, żeby
obejść regułę. Rename i refaktor mają test, bo test ma już istnieć przed zmianą; jeśli go
nie ma, najpierw powstaje test charakteryzujący obecne zachowanie.

Jeśli agent korzysta z wyjątku, musi w swojej odpowiedzi wskazać, do której pozycji listy
się odwołuje. Własne kryteria są niedozwolone.

### Faza czerwona musi być zaobserwowana

Test, który przeszedł przed zmianą, niczego nie dowodzi. Agent musi zobaczyć czerwony wynik,
zanim napisze implementację. Test napisany pod istniejący kod przechodzi niezależnie od
tego, czy logika jest poprawna — i właśnie dlatego daje fałszywe poczucie bezpieczeństwa.

Test musi też faktycznie sprawdzać twierdzenie, które ma potwierdzać. Asercja na czymś
innym, niż deklarowany efekt, nie jest dowodem.

### Twierdzenie bez testu jest hipotezą

Żadne stwierdzenie o zachowaniu kodu nie może być uznane za udowodnione, jeśli nie jest
poparte testem. Dotyczy to odpowiedzi agenta, komunikatu commita, opisu zmiany i tego
dokumentu.

Sformułowania „działa”, „naprawione”, „gotowe”, „bezpieczne”, „nie wpływa na nic innego”
są dopuszczalne wyłącznie ze wskazaniem nazwy testu, który to potwierdza. Jeśli testu nie
ma, jedyne dopuszczalne sformułowanie to jawne „niezweryfikowane” wraz z informacją, co
trzeba by sprawdzić.

### Test jako specyfikacja

Jeden test odpowiada jednej regule. Nazwa testu jest zdaniem w języku domeny i mówi, jakie
zachowanie jest gwarantowane. Czytając listę nazw testów, powinno dać się odtworzyć wymagania
bez czytania implementacji. Dzięki temu nieudany test mówi agentowi dokładnie, co przestało
działać, zamiast zmuszać go do śledzenia kodu.

## Wzorce, które obniżają błąd modelu

### Typy na granicach

Dane z zewnątrz są walidowane raz, na wejściu, i zamieniane w wąski typ. Dalej rdzeń ufa
typowi i nie powtarza sprawdzeń. Model rzadko myli się w środku, gdy nie ma tam niepewnych
kształtów danych — myli się głównie na granicy, gdzie wszystko jest „jakimś obiektem”.

### Zamknięte sumy typów i wyczerpujące dopasowanie

Warianty zachowania są reprezentowane jako zamknięty zbiór typów, a obsługa wymaga
wyczerpującego dopasowania. Dodanie wariantu generuje błędy kompilacji we wszystkich
miejscach, które trzeba zaktualizować. To najskuteczniejsza znana technika zamiany cichego
pominięcia przypadku na głośny błąd.

### Błędy jako wartości w rdzeniu

Rdzeń zwraca wynik jako wartość, która w typie wymienia możliwe porażki. Wyjątki zostają na
granicy, tam gdzie zamieniają się na odpowiedź lub log. Sygnatura pokazuje wtedy każdy
przypadek, o którym trzeba pamiętać; wyjątek jest niewidoczny w sygnaturze, więc model
regularnie go pomija.

### Sygnatury bez flag

Żadnych parametrów logicznych typu `wyślij(x, true)` i żadnych długich list parametrów
pozycyjnych. Wariant zachowania to osobna funkcja albo nazwany obiekt opcji. Flaga w wywołaniu
jest nieczytelna dla człowieka i myląca dla modelu, który nie widzi definicji funkcji.

### Funkcjonalny rdzeń, imperatywna skorupa

Logika jest czysta i testowalna bez środowiska. Całe otoczenie — wejście, wyjście, konfiguracja,
czas — żyje w jednym cienkim miejscu, zwykle na dole pliku. Model edytujący logikę nie ma
wtedy pokusy, żeby dotknąć I/O, a edytujący I/O nie musi rozumieć logiki.

### Rurociąg małych kroków

Złożona transformacja to sekwencja małych, czystych funkcji o jednym wejściu i jednym wyjściu.
Nowy krok wstawia się między dwa istniejące, bez przepisywania całości. Jedna długa funkcja
proceduralna wymaga od modelu zrozumienia całości przy każdej zmianie i zaprasza do
przypadkowej modyfikacji sąsiedniego fragmentu.

### Dane zamiast logiki

Gdy zachowanie jest macierzą przypadków, wyrażamy ją jako dane: tabelę, mapowanie, listę
reguł. Model edytuje dane znacznie pewniej niż łańcuch `if`/`else`. Łańcuch warunków rośnie
w niekontrolowany sposób, a każda nowa gałąź może zmienić zachowanie sąsiedniej.

### Jedno źródło prawdy dla reguły

Każda reguła biznesowa istnieje w dokładnie jednym miejscu. Duplikacja to główne źródło
błędu „agent naprawił jedną kopię”. Jeśli ta sama walidacja występuje w dwóch plikach, to
nie jest kwestia estetyki — to gwarantowana niespójność przy następnej zmianie.

### Nazwy jako wyszukiwarka

Każdy koncept ma dokładnie jedną nazwę w całym repozytorium. Żadnych synonimów typu `user`,
`account`, `client` na to samo. Żadnych worków `data`, `manager`, `utils`, `helper`, `handler`,
`process`. Nazwa ma pozwalać na znalezienie wszystkich miejsc przez jedno wyszukanie; model
pracuje głównie wyszukiwaniem, więc nazwy są jego interfejsem do kodu.

### Jeden plik, jeden temat

Plik odpowiada jednemu tematowi i mieści się w rozsądnym budżecie rozmiaru, tak żeby dało się
go przeczytać w całości. Nazwa pliku jest ścieżką wyszukiwania do tematu. Plik, który trzeba
czytać fragmentami, jest plikiem, którego model nie zrozumie.

### Stały szkielet pliku

Kolejność sekcji jest zawsze taka sama: typy, funkcje czyste, adaptery na końcu. Model wie,
gdzie dopisać nowy element, i nie tworzy nowej konwencji przy każdej zmianie.

### Konwencje mechaniczne

Formatowanie, kolejność importów i układ wymusza narzędzie, nie dokument i nie dobre chęci.
Dokument tłumaczy tylko „dlaczego”. Reguła, której nie da się sprawdzić maszynowo, będzie
łamana pod presją kontekstu.

### Komentarz o pułapkach, nie o kodzie

Komentarz nie opisuje, co robi kod — to widać w kodzie. Komentarz mówi, dlaczego coś jest
zrobione w nietypowy sposób, czego nie wolno zmienić i jaka pułapka czyha w danym miejscu.
Każdy moduł zaczyna się krótkim nagłówkiem: po co istnieje, co dostaje, co gwarantuje.
Agent czyta ten nagłówek przed edycją i wie, czego nie może zepsuć.

### Pętla zwrotna w jednej komendzie

Typecheck, testy i lint uruchamiają się jedną komendą i kończą w kilka sekund. Agent ma
wtedy deterministyczną informację zwrotną i sam poprawia własny błąd, zamiast zgadywać.
Wolna pętla albo kilka komend to zaproszenie do „sprawdzę to później”.

### Testy property i snapshot

Właściwości („dla dowolnego wejścia zachodzi X”) i snapshoty pinują zachowanie, którego
model nie jest w stanie przeanalizować w całości. Snapshot dodatkowo czyni każdą zmianę
wyjścia widoczną w diffie, więc przypadkowa modyfikacja nie przechodzi niezauważona.

### Zależności przypięte i minimalne

Każda zależność to powierzchnia, na której model może zhalucynować API, oraz wersja, której
zachowanie może się zmienić. Wersje są przypięte, a nowa zależność wymaga uzasadnienia.
Standardowa biblioteka wygrywa z pakietem, jeśli różnica jest niewielka.

### Zakaz zgadywania API

Przed użyciem zewnętrznego API agent czyta definicje typów dostępne w repozytorium albo
dokumentację wskazaną w projekcie. Nie odtwarza sygnatur z pamięci. Jeśli API nie da się
potwierdzić, agent to zgłasza, zamiast pisać kod „na wyczucie”.

### Jeden cel na zmianę

Jedna zmiana realizuje jedno wymaganie. Zakaz refaktoru przy okazji, zakaz przemianowywania
niepowiązanych rzeczy, zakaz „przy okazji poprawiłem też”. Mały diff jest sprawdzalny;
duży diff ukrywa błąd i uniemożliwia przypisanie regresji do przyczyny.

## Antywzorce

### Dziedziczenie i hierarchie klas

Hierarchia wymusza czytanie wielu plików, żeby zrozumieć jedną metodę, i rozprasza odpowiedzialność
między warstwy. Kompozycja i funkcje; dziedziczenie tylko tam, gdzie jest narzucone przez
platformę.

### Metaprogramowanie i magia

Makra, dynamiczny dispatch, dekoratory zmieniające zachowanie, kontenery wstrzykiwania zależności,
konfiguracja oparta na nazwach konwencji — wszystko to jest niewidoczne przy czytaniu jednego
pliku. Model nie jest w stanie przewidzieć, co się wydarzy, więc nie jest w stanie bezpiecznie
zmienić kodu.

### Warstwy dla warstw

Każda dodatkowa warstwa abstrakcji to koszt kontekstu i miejsce, w którym można pomylić się
co do tego, gdzie trafia logika. Dwie, maksymalnie trzy warstwy. Nazwy typu
`AbstractFactoryBuilderProxy` są sygnałem, że projekt wymknął się spod kontroli.

### Worki `utils` i `helpers`

Plik bez nazwy domenowej przyciąga wszystko, co nie pasuje gdzie indziej, i staje się
niewyszukiwalny. Funkcja trafia do modułu tematycznego albo nie trafia nigdzie.

### Flagi w parametrach

Parametr logiczny zmienia zachowanie funkcji w sposób niewidoczny w miejscu wywołania.
Osobna funkcja, osobna ścieżka, osobny test.

### Głębokie zagnieżdżenie

Więcej niż dwa poziomy zagnieżdżenia to sygnał, że brakuje wczesnych wyjść albo podziału na
kroki. Model gubi się w zagnieżdżonych warunkach i myli poziom, w którym aktualnie jest.

### Mutowalny stan globalny i singletony

Ukryty stan czyni funkcje niedeterministycznymi i uzależnia wynik od kolejności wywołań.
Stan jest przekazywany jawnie.

### Konfiguracja rozproszona

Zachowanie sterowane zmienną środowiskową odczytywaną w głębokiej warstwie jest nie do
prześledzenia. Konfiguracja jest wczytywana raz, na granicy, i przekazywana dalej jako
argument.

### Wzorce GoF bez zysku

Wzorzec projektowy stosujemy tylko wtedy, gdy realnie zmniejsza koszt kontekstu, lokalność
zmiany albo wykrywalność błędu. `Strategy` jako mapa funkcji — tak. `Visitor` i rozbudowane
fabryki — prawie nigdy. Nazwa wzorca nie jest argumentem.

## Proces pracy agenta

### Najpierw znajdź istniejący wzorzec

Przed napisaniem kodu agent szuka w repozytorium, jak rozwiązano już podobny problem, i powtarza
ten wzorzec. Spójność z lokalnym idiomem jest ważniejsza niż to, czy istnieje lepszy wzorzec
gdzieś indziej.

### Nowy wzorzec tylko z zapisem w dokumencie

Jeśli żaden istniejący wzorzec nie pasuje, agent może wprowadzić nowy — ale w tej samej zmianie
zapisuje go w tym dokumencie. Inaczej repozytorium z każdą sesją nabiera nowych, sprzecznych
konwencji.

### Nie zgaduj intencji

Przy niejednoznacznym wymaganiu agent pyta, zamiast wybierać interpretację. Błędne założenie
jest tańsze do wyłapania przed kodem niż po nim.

### Nie refaktoryzuj przy okazji

Zmiana dotyczy jednego celu. Rzeczy niezwiązane, nawet wyraźnie złe, są zgłaszane, a nie
naprawiane w tym samym diffie.

### Nie zostawiaj TODO

Kod z `TODO` jest niedokończony. Albo zadanie jest zrobione, albo jest jawnie zgłoszone jako
niezrobione wraz z powodem i konsekwencjami.

### Zgłoś niepewność

Agent wskazuje miejsca, których nie zweryfikował testem, i ryzyka, których nie potrafi wykluczyć.
Milczenie w sprawie niepewności jest zgłoszeniem fałszywej pewności.

## Definicja „gotowe”

Zmiana jest gotowa, gdy test został napisany przed implementacją, przeszedł fazę czerwoną,
a następnie zieloną, cała pętla zwrotna przechodzi, żadne twierdzenie w opisie zmiany nie
zostało bez wskazania testu, a zależności nie wzrosły bez uzasadnienia.

## Przenoszenie zasad do narzędzi

Zasada, którą da się sprawdzić maszynowo, jest przenoszona do konfiguracji narzędzi przy
wyborze stacku. Dokument opisuje „dlaczego”, narzędzia wymuszają „co”.

Do wymuszenia w konfiguracji, gdy stack zostanie wybrany:

- tryb ścisły typowania i zakaz typów niejawnych oraz `any`
- wyczerpujące dopasowanie wariantów jako błąd kompilacji
- limit rozmiaru pliku
- formatowanie i kolejność importów
- lint uruchamiany razem z testami w jednej komendzie
- brak ostrzeżeń jako warunek zielonej pętli
