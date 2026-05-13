# MGS: Ground Zeroes - Polish Localization Project

This repository documents the technical process of translating *Metal Gear Solid: Ground Zeroes* into Polish. The project involves reverse engineering Fox Engine asset files, manual font glyph injection, and automated translation pipelines.

## 🛠️ Tech Stack & Tools
* **Fox Engine Translation Tool:** For extracting and repacking `.fnt` and `.pft` files.
* **GIMP:** Manual pixel-art editing of font textures (`LatinFont_0.png` and `LatinFont_1.png`).
* **Python:** Custom scripts for converting `.lng` binaries to `.po` gettext format.
* **Poedit:** Industry-standard translation software.

## 🖋️ Font Implementation details
To support Polish characters (ą, ć, ę, ł, ń, ó, ś, ź, ż), new glyphs were manually added to the game's original textures.
* **Coordinate Mapping:** Managed via `LatinFont.xml`.
* **Vertical Positioning:** Adjusted via `VerticalShift` to match the original game's baseline.
* **Texture Layers:** Split between Layer 0 (lowercase) and Layer 1 (uppercase) for optimized space management.

## 📂 Project Structure
* `/lang` - Translated `.po` and compiled `.lng` files.
* `/font` - Modified PNG textures and XML glyph maps.
* `dev_log_v_0.3.md` - Chronological development log (in Polish).

---
*Disclaimer: This is a non-profit fan project. All rights to the game belong to Konami.*