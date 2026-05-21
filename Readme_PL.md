# Metal Gear Solid V: Ground Zeroes - badania nad polską fanowską lokalizacją

Dokumentacja techniczna i notatki badawcze do fanowskiego spolszczenia **Metal Gear Solid V: Ground Zeroes** na PC.

Repozytorium opisuje proces badania plików Fox Engine, edycji tekstów UI, konwersji `.lng#eng` do `.po`, testów fontów, pracy z paczkami gry oraz problemów z polskimi znakami diakrytycznymi.

Projekt **nie zawiera oryginalnych plików gry**.

## Status projektu

Projekt jest obecnie w fazie badań technicznych i testów.

Potwierdzone do tej pory:

- teksty UI można eksportować z plików `.lng#eng` do `.po`
- edytowane pliki `.po` można budować z powrotem do `.lng#eng`
- zmodyfikowane teksty UI mogą być widoczne w grze
- wybrane paczki UI można rozpakować, zmodyfikować i ponownie spakować
- obsługa polskich znaków nadal wymaga dalszych badań
- różne elementy UI prawdopodobnie korzystają z różnych fontów, tekstur lub ścieżek renderowania

## Główny cel

Celem projektu jest zbudowanie udokumentowanego i powtarzalnego procesu tłumaczenia interfejsu gry na język polski bez dystrybucji oryginalnych plików gry.

Projekt dokumentuje:

- gdzie znajdują się teksty UI
- jak działa konwersja plików językowych
- jakie narzędzia były używane
- które pliki zostały sprawdzone
- co zadziałało
- co nie zadziałało
- które problemy nadal wymagają dalszego researchu

## Najważniejsze narzędzia

- **GzsTool**  
  Używany do rozpakowywania i ponownego pakowania archiwów gry, między innymi `data_02.g0s`.

- **FoxEngine.TranslationTool / FfntTool**  
  Używany do pracy z plikami fontów Fox Engine, w tym z zasobami `.ffnt`.

- **Python**  
  Używany do własnych skryptów eksportujących, analizujących i budujących pliki językowe.

- **Poedit**  
  Używany do edycji tłumaczeń w formacie `.po`.

- **GIMP**  
  Używany do edycji atlasów fontów i tekstur.

- **HxD**  
  Używany do inspekcji binarnej plików oraz szybkiego sprawdzania ciągów tekstowych w plikach gry.

- **VS Code**  
  Używany do edycji skryptów, plików `.po`, XML, dokumentacji i notatek technicznych.

- **Windows CMD**  
  Bardzo ważne narzędzie w projekcie. Używane do szybkiego sprawdzania struktury folderów, listowania plików, porównywania zawartości i wyszukiwania nazw zasobów w paczkach gry.

## Rola CMD i findstr

Duża część pracy badawczej była wykonywana z poziomu Windows CMD.

Najbardziej przydatne komendy:

```bat
dir /s /b
```

Używana do szybkiego listowania plików w strukturze rozpakowanej gry.

```bat
findstr /s /i /m "RodinPro" *.fpkd
```

Używana do wyszukiwania nazw fontów lub zasobów w plikach `.fpkd`.

To podejście pomogło przejść od zgadywania do konkretnych tropów. Jednym z ważnych wyników było wskazanie pliku:

```text
gz_ui_resident_data.fpkd
```

jako istotnego tropu w badaniu fontów używanych przez UI.

W praktyce CMD okazało się jednym z najważniejszych narzędzi diagnostycznych w projekcie. Pozwalało szybko odpowiadać na pytania typu:

- czy dana nazwa zasobu występuje w paczkach gry
- w których plikach pojawia się szukany ciąg znaków
- czy badamy właściwy katalog
- czy konkretne paczki zawierają potencjalnie istotne dane fontów
- czy pliki po rozpakowaniu faktycznie znajdują się tam, gdzie zakładaliśmy

## Pipeline plików językowych

Aktualny workflow dla tekstów UI:

```text
.lng#eng -> .po -> Poedit -> .lng#eng -> repack -> test w grze
```

Własne skrypty Python używane w projekcie:

```text
export_lng_to_po.py
build_lng_from_po.py
parse_lng.py
```

Potwierdzone przykłady zmian tekstu w grze:

```text
CONTINUE -> KONTYNUUJ
GAME START -> TEST START
```

Te testy potwierdziły, że gra czyta zmodyfikowane pliki językowe.

## Główne pliki badane w projekcie

Pliki językowe UI:

```text
Assets\tpp\lang\ui\gz\gz_title.lng#eng
Assets\tpp\lang\ui\gz\gz_menu.lng#eng
Assets\tpp\lang\ui\gz\gz_hud.lng#eng
Assets\tpp\lang\ui\gz\gz_system_x36.lng#eng
Assets\tpp\lang\ui\gz\gz_announce_log.lng#eng
Assets\tpp\lang\ui\gz\gz_mission.lng#eng
Assets\tpp\lang\ui\gz\gz_weapon.lng#eng
Assets\tpp\lang\ui\gz\gz_item.lng#eng
Assets\tpp\lang\ui\gz\gz_cassette.lng#eng
Assets\tpp\lang\ui\gz\gz_loading_x36.lng#eng
```

Paczki UI:

```text
Assets\tpp\pack\ui\gz\gz_ui_default_data_steam.fpkd
Assets\tpp\pack\ui\gz\gz_ui_resident_data.fpkd
Assets\tpp\pack\ui\gz\title_datas.fpk
Assets\tpp\pack\ui\gz\title_datas.fpkd
Assets\tpp\pack\ui\gz\title_datas.pftxs
```

Pliki związane z fontami:

```text
LatinFont.ffnt
LatinFont.xml
LatinFont_0.png
LatinFont_1.png
font_def_ltn.ffnt
font_def_ltn_1
```

## Problem z polskimi znakami

Największym otwartym problemem jest pełna obsługa polskich znaków:

```text
ą ć ę ł ń ó ś ź ż
Ą Ć Ę Ł Ń Ó Ś Ź Ż
```

Podczas testów zaobserwowano:

- `Ó` potrafiło wyświetlać się poprawnie w części przypadków
- znaki takie jak `Ł`, `Ż`, `Ą` i `Ę` powodowały puste miejsca, brak glifów albo niespójne renderowanie
- dodanie glifów do `LatinFont_0.png`, `LatinFont_1.png` oraz `LatinFont.xml` nie wystarczyło dla wszystkich ekranów UI
- część UI prawdopodobnie korzysta z innych zasobów fontów niż początkowo zakładano

Wykonano test kontrolny polegający na celowym uszkodzeniu litery `A`.

Wynik:

```text
Popup zamykania gry: zmodyfikowana litera A widoczna
Główne menu: zmodyfikowana litera A niewidoczna
```

To sugeruje, że różne elementy UI mogą korzystać z różnych fontów, tekstur, paczek lub ścieżek renderowania.

## Badania nad fontami

Testowane były trzy główne podejścia.

### 1. Dodanie nowych polskich glifów

Polskie znaki zostały dodane ręcznie do atlasów fontów i opisane w XML.

Problem:

- gra nie renderowała nowych znaków konsekwentnie
- część ekranów UI ignorowała zmodyfikowane zasoby fontów
- poprawny wygląd PNG i XML nie oznaczał automatycznie poprawnego efektu w grze

### 2. Użycie istniejących znaków jako zamienników

Testowane było podejście polegające na wykorzystaniu istniejących znaków z fontu i zastąpieniu ich wizualnie polskimi glifami.

Przykładowa idea:

```text
å -> ż
ø -> ę
Æ -> Ą
```

Dzięki temu tekst w plikach gry mógłby używać znaków już obsługiwanych przez font, a wizualnie wyświetlać polskie litery.

Problem:

- wyniki były niespójne między różnymi ekranami UI
- nadal trzeba było ustalić, który font i która tekstura są używane w konkretnym miejscu gry

### 3. Celowe psucie znanych glifów

Modyfikowano istniejące znaki, na przykład literę `A`, aby sprawdzić, czy dana część UI faktycznie używa badanego fontu.

Ten test okazał się bardzo pomocny, bo pozwolił odróżnić sytuację:

```text
plik został poprawnie zmieniony
```

od sytuacji:

```text
gra w tym miejscu w ogóle nie korzysta z tego pliku
```

To był jeden z ważniejszych momentów w projekcie, bo zatrzymał zgadywanie i pokazał, że problem nie leży wyłącznie w samych glifach.

## Co działa

- eksport `.lng#eng` do `.po`
- edycja tekstów w Poedit
- budowanie `.lng#eng` z `.po`
- widoczne zmiany tekstów UI w grze
- podstawowe testy rozpakowywania i pakowania zasobów
- analiza paczek `.fpk`, `.fpkd` i `.pftxs`
- wyszukiwanie nazw zasobów przez CMD i `findstr`
- dokumentowanie testów i wyników w repozytorium

## Co nadal wymaga badań

- pełna obsługa polskich znaków w głównym menu
- identyfikacja wszystkich fontów używanych przez UI
- różnice między fontami używanymi w popupach, menu i innych elementach interfejsu
- struktura i edycja plików `.subp` dla napisów dialogowych
- stabilny sposób dystrybucji patcha bez dołączania oryginalnych plików gry
- przygotowanie prostego instalatora lub patchera

## Struktura repozytorium

```text
PO/
  UI/
    Pliki tłumaczeń w formacie .po

Reports/
  UI/
    Notatki techniczne i raporty z testów

Tools/
  Python/
    Własne skrypty do konwersji i analizy plików językowych

dev_log.md
  Chronologiczny dziennik prac

README.md
  Angielski opis projektu

Readme_PL.md
  Polski opis projektu
```

## Następne kroki

- dokładniej opisać workflow `.lng#eng` do `.po`
- kontynuować badanie zasobów fontów UI
- zbadać dokładniej `gz_ui_resident_data.fpkd`
- porównać `gz_ui_default_data_steam.fpkd`, `gz_ui_resident_data.fpkd` i `title_datas`
- rozpocząć osobny research plików `.subp`
- przygotować bezpieczny workflow patchowania bez dystrybucji oryginalnych assetów gry
- uporządkować dziennik prac w `dev_log.md`

## Zasada projektu

Każda zmiana musi być potwierdzona w grze.

Nie wystarczy, że:

- plik ma nową datę modyfikacji
- PNG wygląda poprawnie
- XML ma wpisany nowy glif
- paczka została ponownie zbudowana
- tekst wygląda dobrze w edytorze

Liczy się dopiero efekt w grze.

W tym projekcie jedna litera potrafi zatrzymać cały pipeline. I właśnie dlatego dokumentujemy nie tylko sukcesy, ale też błędne tropy.

## Disclaimer

This is a non-profit fan localization and technical research project.

This repository does not contain original game files.

All rights to **Metal Gear Solid V: Ground Zeroes** belong to Konami.
