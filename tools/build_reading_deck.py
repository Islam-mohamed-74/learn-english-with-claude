"""Build Claude_words_for_reading.apkg from Claude_words_for_reading.txt.

Run:  python tools/build_reading_deck.py   (from the English folder)
Then in Anki: File > Import > Claude_words_for_reading.apkg

Each word keeps the same id as long as the word itself does not change,
so importing again adds the new words and keeps your progress on the old ones.
"""
import os
import re

from anki_package import COMMON_CSS, escape, read_lines, write_package

HERE = os.path.dirname(os.path.abspath(__file__))
NAME = "Claude_words_for_reading"
FOLDER = os.path.join(HERE, "..", "reading")

CSS = COMMON_CSS + """
.sent{font-size:22px;direction:ltr;margin-top:14px}
.sent b{color:#1D4ED8}
.sentar{font-family:"Segoe UI",Tahoma,Arial,sans-serif;font-size:20px;direction:rtl;color:#6B7280}
.hook{font-family:"Segoe UI",Tahoma,Arial,sans-serif;font-size:20px;direction:rtl;background:#FEF3C7;border-radius:10px;padding:10px;margin-top:14px}
.nightMode .sent b,.night_mode .sent b{color:#93C5FD}
.nightMode .sentar,.night_mode .sentar{color:#9CA3AF}
.nightMode .hook,.night_mode .hook{background:#3B2F0B}
"""

MODEL = {
    "id": 1760000003,
    "name": "Claude Word",
    "fields": ["Word", "Meaning", "Sentence", "SentenceArabic", "Hook"],
    "rtl_fields": ["Meaning", "SentenceArabic", "Hook"],
    "css": CSS,
    "templates": [
        {
            "name": "English to Arabic",
            "qfmt": '<div class="en">{{Word}}</div><div class="sent">{{Sentence}}</div>',
            "afmt": '{{FrontSide}}<hr id=answer><div class="ar">{{Meaning}}</div>'
                    '<div class="sentar">{{SentenceArabic}}</div>'
                    '{{#Hook}}<div class="hook">{{Hook}}</div>{{/Hook}}',
        },
    ],
}


def highlight(word, sentence):
    """Bold the word (or one of its forms, like 'carries' for 'carry') inside the sentence."""
    stem = re.escape(word[:-1]) if word[-1] in "ey" else re.escape(word)
    pattern = r"\b(" + re.escape(word) + r"\w*|" + stem + r"(?:ies|ied|ing|ed)" + r")\b"
    return re.sub(pattern, r"<b>\1</b>", escape(sentence), count=1, flags=re.I)


def read_words():
    notes, seen = [], {}
    for number, _section, parts in read_lines(os.path.join(FOLDER, NAME + ".txt")):
        if len(parts) != 5 or not all(parts[:3]):
            raise SystemExit(f"Line {number}: write it as word|meaning|sentence|sentence in Arabic|hook")
        word, meaning, sentence, sentence_ar, hook = parts
        if word in seen:
            raise SystemExit(f"Line {number}: this word is already on line {seen[word]}: {word}")
        seen[word] = number
        marked = highlight(word, sentence)
        if "<b>" not in marked:
            raise SystemExit(f"Line {number}: the sentence does not contain the word: {word}")
        notes.append((word, [escape(word), escape(meaning), marked, escape(sentence_ar), escape(hook)],
                      ["claude", "reading"]))
    return notes


if __name__ == "__main__":
    write_package(
        os.path.join(FOLDER, NAME + ".apkg"), 1760000004, "Claude::Words for Reading", MODEL, read_words(),
        key_prefix="claude-word:", id_base=1762000000000,
    )
