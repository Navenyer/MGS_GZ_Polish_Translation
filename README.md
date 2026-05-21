# Metal Gear Solid V: Ground Zeroes - Polish Fan Localization Research

Technical documentation and research notes for a Polish fan localization of **Metal Gear Solid V: Ground Zeroes** on PC.

This repository focuses on Fox Engine localization workflows, UI text extraction, `.lng#eng` to `.po` conversion, font atlas experiments, package testing, and Polish diacritics debugging.

This project does **not** include original game files.

## Current Status

The project is currently in the technical research and testing phase.

Confirmed so far:

- UI text can be exported from `.lng#eng` files to `.po`
- edited `.po` files can be rebuilt into `.lng#eng`
- modified UI text can be displayed in-game
- selected UI packages can be unpacked, modified, and repacked
- Polish diacritics are still under investigation
- different UI elements appear to use different font resources or rendering paths

## Main Goal

The goal is to build a documented and repeatable workflow for translating the game UI into Polish without distributing original game assets.

The project documents:

- where UI text is stored
- how language files are converted and rebuilt
- which tools are used
- which files were tested
- what worked
- what failed
- what still requires research

## Tools Used

- **GzsTool**  
  Used for unpacking and repacking game archives, including `data_02.g0s`.

- **FoxEngine.TranslationTool / FfntTool**  
  Used for working with Fox Engine font files and `.ffnt` font resources.

- **Python**  
  Used for custom scripts that export, parse, and rebuild language files.

- **Poedit**  
  Used for editing translation files in `.po` format.

- **GIMP**  
  Used for editing font atlases and texture files.

- **HxD**  
  Used for binary inspection and checking strings inside game files.

- **VS Code**  
  Used for scripts, notes, XML files, and documentation.

- **Windows CMD / findstr**  
  Used for file searches and quick technical checks during investigation.

## Language File Pipeline

The current UI text workflow:

```text
.lng#eng -> .po -> Poedit -> .lng#eng -> repack -> in-game test
```

Custom Python scripts used in the project:

```text
export_lng_to_po.py
build_lng_from_po.py
parse_lng.py
```

Confirmed examples of UI text changes include:

```text
CONTINUE -> KONTYNUUJ
GAME START -> TEST START
```

These tests confirmed that the game reads modified language files.

## Main Files Investigated

UI language files:

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

UI packages:

```text
Assets\tpp\pack\ui\gz\gz_ui_default_data_steam.fpkd
Assets\tpp\pack\ui\gz\gz_ui_resident_data.fpkd
Assets\tpp\pack\ui\gz\title_datas.fpk
Assets\tpp\pack\ui\gz\title_datas.fpkd
Assets\tpp\pack\ui\gz\title_datas.pftxs
```

Font-related files investigated:

```text
LatinFont.ffnt
LatinFont.xml
LatinFont_0.png
LatinFont_1.png
font_def_ltn.ffnt
font_def_ltn_1
```

## Polish Diacritics Problem

The biggest open issue is Polish diacritics support:

```text
ą ć ę ł ń ó ś ź ż
Ą Ć Ę Ł Ń Ó Ś Ź Ż
```

During testing:

- `Ó` was displayed correctly in some cases
- characters like `Ł`, `Ż`, `Ą`, and `Ę` caused missing glyphs or inconsistent rendering
- adding glyphs to `LatinFont_0.png`, `LatinFont_1.png`, and `LatinFont.xml` was not enough for all UI screens
- some UI elements appear to use different font resources than others

A control test was performed by deliberately modifying the glyph for the letter `A`.

Result:

```text
Close-game popup: modified A visible
Main menu: modified A not visible
```

This suggests that different UI elements may use different fonts, texture packages, or rendering paths.

## Font Research Notes

Tested approaches:

### 1. Adding new Polish glyphs

Polish glyphs were added manually to font atlas textures and mapped in XML.

Problem:

- the game did not consistently render the new characters
- some UI screens ignored the modified font resources

### 2. Reusing existing characters

Another tested approach was to reuse existing characters from the font and visually replace them with Polish glyphs.

Example idea:

```text
å -> ż
ø -> ę
Æ -> Ą
```

This could allow the game to display Polish characters by using existing supported character slots.

Problem:

- results were inconsistent between UI screens
- the correct font resource still had to be identified for each UI context

### 3. Deliberately breaking known glyphs

Existing glyphs such as `A` were modified to confirm whether a specific font resource was used by the game.

This proved useful because it showed when a file was being read by one part of the UI but ignored by another.

## Known Issues

- Polish diacritics are not fully solved yet
- main menu font resources are still being investigated
- different UI screens may use different font systems
- `.subp` subtitle files still require separate research
- patch distribution needs to avoid including original game files

## Repository Structure

```text
PO/
  UI/
    Translation files in .po format

Reports/
  UI/
    Technical notes and test reports

Tools/
  Python/
    Custom scripts for language file conversion and parsing

dev_log.md
  Chronological development log

Readme.md
  English project overview

Readme_PL.md
  Polish project overview
```

## Next Steps

- Document the `.lng#eng` to `.po` workflow in detail
- Continue research on UI font resources
- Investigate `gz_ui_resident_data.fpkd`
- Compare `gz_ui_default_data_steam.fpkd`, `gz_ui_resident_data.fpkd`, and `title_datas`
- Research `.subp` subtitle files
- Prepare a safe patching workflow that does not distribute original game assets

## Disclaimer

This is a non-profit fan localization and technical research project.

This repository does not contain original game files.

All rights to **Metal Gear Solid V: Ground Zeroes** belong to Konami.
