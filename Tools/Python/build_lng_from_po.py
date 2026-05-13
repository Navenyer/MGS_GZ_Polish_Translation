from pathlib import Path
import sys
import ast

SEPARATOR = b"\x00\x01\x00"


def parse_po_string(line: str) -> str:
    line = line.strip()
    if not line.startswith('"'):
        return ""
    return ast.literal_eval(line)


def read_po(path: Path) -> dict[str, str]:
    translations = {}

    current_context = None
    current_msgid = ""
    current_msgstr = ""
    active = None

    def finish_entry():
        nonlocal current_context, current_msgid, current_msgstr, active

        if current_context and "::" in current_context:
            key = current_context.split("::", 1)[1]
            if current_msgstr:
                translations[key] = current_msgstr

        current_context = None
        current_msgid = ""
        current_msgstr = ""
        active = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()

        if not line:
            finish_entry()
            continue

        if line.startswith("msgctxt "):
            current_context = parse_po_string(line[len("msgctxt ") :])
            active = "msgctxt"
            continue

        if line.startswith("msgid "):
            current_msgid = parse_po_string(line[len("msgid ") :])
            active = "msgid"
            continue

        if line.startswith("msgstr "):
            current_msgstr = parse_po_string(line[len("msgstr ") :])
            active = "msgstr"
            continue

        if line.startswith('"'):
            value = parse_po_string(line)
            if active == "msgctxt":
                current_context = (current_context or "") + value
            elif active == "msgid":
                current_msgid += value
            elif active == "msgstr":
                current_msgstr += value

    finish_entry()
    return translations


def read_lng(path: Path):
    data = path.read_bytes()

    count = int.from_bytes(data[0x0C:0x10], "little")
    table = int.from_bytes(data[0x10:0x14], "little")
    key_base = int.from_bytes(data[0x14:0x18], "little")
    text_base_header = int.from_bytes(data[0x18:0x1C], "little")
    text_base = text_base_header + 2

    entries = []

    for i in range(count):
        row = table + i * 8

        key_offset = int.from_bytes(data[row : row + 4], "little")
        text_offset = int.from_bytes(data[row + 4 : row + 8], "little")

        key_start = key_base + key_offset
        key_end = data.find(b"\x00", key_start)
        key = data[key_start:key_end].decode("ascii", errors="replace")

        text_start = text_base + text_offset
        text_end = data.find(SEPARATOR, text_start)

        if text_end == -1:
            text_end = len(data)

        text = (
            data[text_start:text_end].rstrip(b"\x00").decode("utf-8", errors="replace")
        )

        entries.append(
            {
                "index": i,
                "row": row,
                "key": key,
                "key_offset": key_offset,
                "text_offset": text_offset,
                "text": text,
            }
        )

    return data, entries, text_base


def build_lng(original_lng: Path, po_path: Path, output_path: Path):
    data, entries, text_base = read_lng(original_lng)
    translations = read_po(po_path)

    prefix = bytearray(data[:text_base])
    text_blob = bytearray()

    changed = 0

    for i, entry in enumerate(entries):
        key = entry["key"]
        original_text = entry["text"]

        new_text = translations.get(key, original_text)
        new_text = new_text.replace("\r\n", "\n").replace("\r", "\n")

        if new_text != original_text:
            changed += 1

        new_offset = len(text_blob)

        row = entry["row"]
        prefix[row + 4 : row + 8] = new_offset.to_bytes(4, "little")

        text_blob += new_text.encode("utf-8")

        if i < len(entries) - 1:
            text_blob += SEPARATOR
        else:
            text_blob += b"\x00"

    output_path.write_bytes(prefix + text_blob)

    print(f"Original LNG: {original_lng}")
    print(f"PO file:      {po_path}")
    print(f"Output LNG:   {output_path}")
    print(f"Entries:      {len(entries)}")
    print(f"Changed:      {changed}")


def main():
    if len(sys.argv) != 4:
        print("Usage:")
        print(
            "python build_lng_from_po.py <original.lng#eng> <translation.po> <output.lng#eng>"
        )
        sys.exit(1)

    original_lng = Path(sys.argv[1])
    po_path = Path(sys.argv[2])
    output_path = Path(sys.argv[3])

    if not original_lng.exists():
        print(f"Original LNG not found: {original_lng}")
        sys.exit(1)

    if not po_path.exists():
        print(f"PO file not found: {po_path}")
        sys.exit(1)

    build_lng(original_lng, po_path, output_path)


if __name__ == "__main__":
    main()
