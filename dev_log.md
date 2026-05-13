# MGS: Ground Zeroes - Dziennik Spolszczenia

Logi z prac nad lokalizacją i modyfikacją plików gry.

---

### 🔍 CHECKLISTA TESTÓW (14.05)
- [ ] **Layer Check:** Czy wielkie litery mają `Layer="1"` (LatinFont_1.png), a małe `Layer="0"`?
- [ ] **Baseline:** Czy polskie znaki nie "skaczą" w górę/dół względem sąsiadów? (Korekta przez `VerticalShift`).
- [ ] **Kerning:** Czy po literze "ł" lub "ą" następny znak nie jest za blisko? (Korekta przez `HorizontalSpace`).
- [ ] **Ogonki:** Czy dolne części "ą", "ę" są widoczne, czy ucięte przez dół ramki? (Korekta przez `Height`).
- [ ] **Encoding:** Czy gra poprawnie czyta plik XML po dodaniu znaków (brak crasha)?

**Szybka ściąga korekty (XML):**
- Litera za wysoko -> Zwiększ `VerticalShift`
- Litera ucięta od dołu -> Zwiększ `Height`
- Za mało miejsca po literze -> Zwiększ `HorizontalSpace`

---

### 13.05.2026 - Polskie znaki i XML
**Zrobione:**
* W GIMP-ie dorysowałem małe polskie litery do `LatinFont_0.png` oraz wielkie do `LatinFont_1.png` (tam było więcej miejsca).
* Z pomocą Gemini wygenerowałem wpisy `<Glyph>` dla małych liter do pliku `LatinFont.xml`.
* Skonfigurowane znaki: ą, ć, ę, ł, ń, ó, ś, ź, ż.

---

### 12.05.2026 - Tłumaczenie menu i diagnoza fontu
**Zrobione:**
* Przetłumaczone 100% wpisów w `gz_title.lng` i `gz_menu.lng` (autorskie tłumaczenie we współpracy z Gemini).
* Potwierdzona stabilność `build_lng_from_po.py`.
* Testy w grze wykazały brak polskich znaków (poza „Ó”).

**Analiza źródeł zewnętrznych:**
* Archiwum Herbaciarza – tłumaczenia dotyczą misji i zostaną wykorzystane jako baza przy sekcji `gz_mission`.

---

### 11.05.2026 - Pierwszy udany Build (POC)
**Zrobione:**
* Uruchomienie pipeline'u: `.lng` → `.po` → `.lng`.
* Pierwsze zmiany widoczne w grze: *CONTINUE* → *KONTYNUUJ*.
* Spakowanie plików do `.fpkd` i `data_02.g0s` działa poprawnie.

---

### Plan na najbliższe dni:
- [ ] Tłumaczenie sekcji `gz_system_x36` (komunikaty systemowe).
- [ ] Implementacja tłumaczeń z archiwum Herbaciarza dla sekcji `gz_mission`.
- [ ] Research formatu `.subp` (dialogi - sekcja 08).
- [ ] Decyzja: **WYNIKI** czy **REKORDY**?

---
*Narzędzia: FoxEngine.TranslationTool v0.2.5, Poedit, GIMP, VS Code + Python.*