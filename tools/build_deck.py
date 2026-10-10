"""Build Claude_chunks_for_writing.apkg from Claude_chunks_for_writing.txt.

Run:  python tools/build_deck.py   (from the English folder)
Then in Anki: File > Import > Claude_chunks_for_writing.apkg

Each chunk keeps the same id as long as its English text does not change,
so importing again adds the new chunks and keeps your progress on the old ones.
"""
import os

from anki_package import COMMON_CSS, escape, read_lines, write_package

HERE = os.path.dirname(os.path.abspath(__file__))
NAME = "Claude_chunks_for_writing"
FOLDER = os.path.join(HERE, "..", "writing")

SEC = '<div class="sec">{{Section}}</div>'
NOTE = '{{#Note}}<div class="note">{{Note}}</div>{{/Note}}'
MODEL = {
    "id": 1760000001,
    "name": "Claude Chunk",
    "fields": ["English", "Arabic", "Note", "Section"],
    "rtl_fields": ["Arabic"],
    "css": COMMON_CSS,
    "templates": [
        {
            "name": "Arabic to English",
            "qfmt": SEC + '<div class="ar">{{Arabic}}</div><div class="hint">Type it in English.</div>'
                    '{{type:English}}',
            "afmt": '{{FrontSide}}<hr id=answer><div class="en">{{English}}</div>' + NOTE,
        },
        {
            "name": "English to Arabic",
            "qfmt": SEC + '<div class="en">{{English}}</div>',
            "afmt": '{{FrontSide}}<hr id=answer><div class="ar">{{Arabic}}</div>' + NOTE,
        },
    ],
}


def read_chunks():
    notes, seen = [], {}
    for number, section, parts in read_lines(os.path.join(FOLDER, NAME + ".txt")):
        if len(parts) not in (2, 3) or not parts[0] or not parts[1]:
            raise SystemExit(f"Line {number}: write it as English|Arabic")
        english, arabic = parts[0], parts[1]
        note = parts[2] if len(parts) == 3 else ""
        if english in seen:
            raise SystemExit(f"Line {number}: this English chunk is already on line {seen[english]}: {english}")
        seen[english] = number
        section = section or "Chunks"
        tag = section.lower().replace(" ", "-").replace("/", "")
        notes.append((english, [escape(english), escape(arabic), escape(note), escape(section)],
                      ["claude", "writing", tag]))
    return notes


if __name__ == "__main__":
    write_package(
        os.path.join(FOLDER, NAME + ".apkg"), 1760000002, "Claude::Chunks for Writing", MODEL, read_chunks(),
        key_prefix="claude-chunk:", id_base=1760000000000,
    )
