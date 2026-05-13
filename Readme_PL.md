# MGS: Ground Zeroes - Polish Translation Project

Projekt spolszczenia MGS:GZ. Obecnie faza implementacji fontów i tłumaczenia UI.

## Progress
- UI (gz_title, gz_menu): 100%
- System/Logs: In progress
- Font: WIP (dodane polskie glify do tekstur)

## Setup i Tooling
- FoxEngine.TranslationTool (v0.2.5)
- Skrypt build_lng_from_po.py do rebuildowania .lng
- GIMP (edycja LatinFont_0.png i LatinFont_1.png)

## Notatki techniczne (Fonty)
Glify dodane ręcznie do tekstur. Parametry w LatinFont.xml:
- Layer 0: LatinFont_0 (małe litery)
- Layer 1: LatinFont_1 (wielkie litery)
- VerticalShift: dla małych liter ustawione na 34 (bazowane na oryginalnych offsetach gry).
- Height: 40px dla małych, ~60px dla wielkich (zapas pod ogonki).

## Devlog
13.05.2026: 
Dodanie małych polskich znaków do LatinFont_0.png + mapowanie w XML. Poprawka pionowego pozycjonowania (VerticalShift).

12.05.2026: 
Full translate gz_title i gz_menu. Wykorzystana pamięć TM z archiwum Herbaciarza (ok. 30% dopasowań).

## To-do
- [ ] Sekcje gz_system_x36 i gz_mission.
- [ ] Research plików .subp (hardcoded napisy).
- [ ] Korekta terminologii (Wyniki vs Rekordy).