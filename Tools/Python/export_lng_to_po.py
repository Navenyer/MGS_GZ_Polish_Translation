from pathlib import Path
import sys


def escape_po(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def read_lng(path: Path):
    data = path.read_bytes()

    count = int.from_bytes(data[0x0C:0x10], "little")
    table = int.from_bytes(data[0x10:0x14], "little")
    key_base = int.from_bytes(data[0x14:0x18], "little")
    text_base = int.from_bytes(data[0x18:0x1C], "little") + 2

    entries = []

    for i in range(count):
        row = table + i * 8

        key_offset = int.from_bytes(data[row : row + 4], "little")
        text_offset = int.from_bytes(data[row + 4 : row + 8], "little")

        key_start = key_base + key_offset
        key_end = data.find(b"\x00", key_start)
        key = data[key_start:key_end].decode("ascii", errors="replace")

        text_start = text_base + text_offset
        text_end = data.find(b"\x00\x01\x00", text_start)
        if text_end == -1:
            text_end = len(data)

        text = (
            data[text_start:text_end].rstrip(b"\x00").decode("utf-8", errors="replace")
        )

        entries.append((key, text))

    return entries


def write_po(input_path: Path, entries):
    output_path = input_path.with_suffix(input_path.suffix + ".po")

    lines = []
    lines.append('msgid ""')
    lines.append('msgstr ""')
    lines.append('"Project-Id-Version: MGSV GZ\\n"')
    lines.append('"Last-Translator: Naven\\n"')
    lines.append('"Language-Team: Naven\\n"')
    lines.append('"Language: pl_PL\\n"')
    lines.append('"Content-Type: text/plain; charset=UTF-8\\n"')
    lines.append('"Content-Transfer-Encoding: 8bit\\n"')
    lines.append(
        '"Plural-Forms: nplurals=3; plural=(n==1 ? 0 : n%10>=2 && n%10<=4 && (n%100<12 || n%100>14) ? 1 : 2);\\n"'
    )
    lines.append("")

    for key, text in entries:
        context = f"{input_path.name}::{key}"

        lines.append(f'msgctxt "{escape_po(context)}"')
        lines.append(f'msgid "{escape_po(text)}"')
        lines.append('msgstr ""')
        lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


def main():
    if len(sys.argv) < 2:
        print("Usage: python export_lng_to_po.py <file.lng#eng>")
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        print(f"File not found: {input_path}")
        sys.exit(1)

    entries = read_lng(input_path)
    output_path = write_po(input_path, entries)

    print(f"Exported {len(entries)} entries")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()
