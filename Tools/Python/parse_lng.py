from pathlib import Path
import sys

if len(sys.argv) < 2:
    print("Usage: python parse_lng.py <file>")
    sys.exit(1)

path = Path(sys.argv[1])
data = path.read_bytes()

count = int.from_bytes(data[0x0C:0x10], "little")
table = int.from_bytes(data[0x10:0x14], "little")
key_base = int.from_bytes(data[0x14:0x18], "little")
text_base = int.from_bytes(data[0x18:0x1C], "little") + 2

print("file:", path.name)
print("count:", count)
print("table:", hex(table))
print("key_base:", hex(key_base))
print("text_base:", hex(text_base))
print()

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

    text = data[text_start:text_end].rstrip(b"\x00").decode("utf-8", errors="replace")

    print(i, hex(key_offset), hex(text_offset), key, "=>", repr(text))
