"""Write an Anki .apkg file. Used by build_deck.py and build_reading_deck.py."""
import hashlib
import html
import json
import os
import sqlite3
import tempfile
import time
import zipfile

# Colours that stay readable in Anki's light and dark mode.
COMMON_CSS = """
.card{font-family:Calibri,Arial,sans-serif;font-size:22px;text-align:center;color:#1F2937;background:#FFFFFF;padding:18px}
.en{font-family:Arial,sans-serif;font-weight:bold;font-size:30px;color:#1D4ED8;direction:ltr}
.ar{font-family:"Segoe UI",Tahoma,Arial,sans-serif;font-size:30px;direction:rtl;margin:10px 0}
.hint{font-size:16px;color:#6B7280;margin-top:6px}
.note{font-size:18px;background:#EEF2FF;border-radius:10px;padding:10px;margin-top:12px}
.sec{font-size:12px;letter-spacing:.1em;color:#B45309;text-transform:uppercase;margin-bottom:10px}
hr{border:0;border-top:1px solid #D1D5DB}
.card.nightMode,.card.night_mode{color:#E5E7EB;background:#1E1E1E}
.nightMode .en,.night_mode .en{color:#93C5FD}
.nightMode .hint,.night_mode .hint{color:#9CA3AF}
.nightMode .note,.night_mode .note{background:#1E293B}
.nightMode .sec,.night_mode .sec{color:#FBBF24}
.nightMode hr,.night_mode hr{border-top-color:#4B5563}
#typeans{font-size:22px;text-align:center;direction:ltr;width:90%;padding:8px;border-radius:8px;border:1px solid #9CA3AF;margin-top:14px}
code#typeans{font-family:Arial,sans-serif;border:0;direction:ltr}
.typeGood{background:#16A34A;color:#FFFFFF}
.typeBad{background:#DC2626;color:#FFFFFF}
.typeMissed{background:#6B7280;color:#FFFFFF}
"""

SCHEMA = """
CREATE TABLE col (id integer primary key, crt integer not null, mod integer not null, scm integer not null,
  ver integer not null, dty integer not null, usn integer not null, ls integer not null, conf text not null,
  models text not null, decks text not null, dconf text not null, tags text not null);
CREATE TABLE notes (id integer primary key, guid text not null, mid integer not null, mod integer not null,
  usn integer not null, tags text not null, flds text not null, sfld integer not null, csum integer not null,
  flags integer not null, data text not null);
CREATE TABLE cards (id integer primary key, nid integer not null, did integer not null, ord integer not null,
  mod integer not null, usn integer not null, type integer not null, queue integer not null, due integer not null,
  ivl integer not null, factor integer not null, reps integer not null, lapses integer not null,
  left integer not null, odue integer not null, odid integer not null, flags integer not null, data text not null);
CREATE TABLE revlog (id integer primary key, cid integer not null, usn integer not null, ease integer not null,
  ivl integer not null, lastIvl integer not null, factor integer not null, time integer not null,
  type integer not null);
CREATE TABLE graves (usn integer not null, oid integer not null, type integer not null);
CREATE INDEX ix_notes_usn on notes (usn);
CREATE INDEX ix_cards_usn on cards (usn);
CREATE INDEX ix_revlog_usn on revlog (usn);
CREATE INDEX ix_cards_nid on cards (nid);
CREATE INDEX ix_cards_sched on cards (did, queue, due);
CREATE INDEX ix_revlog_cid on revlog (cid);
CREATE INDEX ix_notes_csum on notes (csum);
"""

DCONF = {
    "1": {
        "autoplay": True, "id": 1, "maxTaken": 60, "mod": 0, "name": "Default", "replayq": True, "timer": 0,
        "usn": 0,
        "lapse": {"delays": [10], "leechAction": 0, "leechFails": 8, "minInt": 1, "mult": 0},
        "new": {"bury": True, "delays": [1, 10], "initialFactor": 2500, "ints": [1, 4, 7], "order": 1,
                "perDay": 20, "separate": True},
        "rev": {"bury": True, "ease4": 1.3, "fuzz": 0.05, "ivlFct": 1, "maxIvl": 36500, "minSpace": 1,
                "perDay": 100},
    }
}


def escape(text):
    return html.escape(text, quote=False)


def read_lines(path):
    """Yield (line number, section, parts) for every 'a|b|c' line. '## x' starts a section, '#' is a comment."""
    section = ""
    with open(path, encoding="utf-8-sig") as f:
        for number, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            if line.startswith("##"):
                section = line[2:].strip()
                continue
            if line.startswith("#"):
                continue
            yield number, section, [p.strip() for p in line.split("|")]


def _model(model, deck_id, now):
    fields = [
        {"name": name, "ord": i, "font": "Arial", "media": [], "rtl": name in model["rtl_fields"], "size": 20,
         "sticky": False}
        for i, name in enumerate(model["fields"])
    ]
    templates = [
        {**t, "ord": i, "bafmt": "", "bqfmt": "", "bfont": "", "bsize": 0, "did": None}
        for i, t in enumerate(model["templates"])
    ]
    return {
        str(model["id"]): {
            "css": model["css"], "did": deck_id, "flds": fields, "id": str(model["id"]),
            "latexPost": "\\end{document}",
            "latexPre": "\\documentclass[12pt]{article}\n\\begin{document}\n",
            "latexsvg": False, "mod": now, "name": model["name"],
            "req": [[i, "any", [0]] for i in range(len(templates))],
            "sortf": 0, "tags": [], "tmpls": templates, "type": 0, "usn": -1, "vers": [],
        }
    }


def _decks(deck_id, deck_name, now):
    def deck(one_id, name):
        return {
            "collapsed": False, "conf": 1, "desc": "", "dyn": 0, "extendNew": 10, "extendRev": 50,
            "id": one_id, "lrnToday": [0, 0], "mod": now, "name": name, "newToday": [0, 0],
            "revToday": [0, 0], "timeToday": [0, 0], "usn": -1,
        }
    return {"1": deck(1, "Default"), str(deck_id): deck(deck_id, deck_name)}


def write_package(output, deck_id, deck_name, model, notes, key_prefix, id_base):
    """notes: list of (key, fields, tags). A note keeps its id as long as its key does not change,
    so importing the package again adds new notes and keeps the progress on the old ones."""
    now = int(time.time())
    conf = {
        "activeDecks": [1], "addToCur": True, "collapseTime": 1200, "curDeck": 1, "curModel": str(model["id"]),
        "dueCounts": True, "estTimes": True, "newBury": True, "newSpread": 0, "nextPos": 1,
        "sortBackwards": False, "sortType": "noteFld", "timeLim": 0,
    }
    folder = tempfile.mkdtemp()
    db_path = os.path.join(folder, "collection.anki2")
    db = sqlite3.connect(db_path)
    db.executescript(SCHEMA)
    db.execute(
        "insert into col values (1,?,?,?,11,0,0,0,?,?,?,?,'{}')",
        (now, now * 1000, now * 1000, json.dumps(conf), json.dumps(_model(model, deck_id, now)),
         json.dumps(_decks(deck_id, deck_name, now)), json.dumps(DCONF)),
    )
    used_ids = set()
    for position, (key, fields, tags) in enumerate(notes):
        number = int(hashlib.sha1((key_prefix + key).encode("utf-8")).hexdigest(), 16)
        note_id = id_base + (number % 300000000) * 3
        while note_id in used_ids:
            note_id += 3
        used_ids.add(note_id)
        guid = "cc" + format(number % 16 ** 12, "012x")
        checksum = int(hashlib.sha1(fields[0].encode("utf-8")).hexdigest()[:8], 16)
        db.execute(
            "insert into notes values (?,?,?,?,-1,?,?,?,?,0,'')",
            (note_id, guid, model["id"], now, " " + " ".join(tags) + " ", "\x1f".join(fields), fields[0],
             checksum),
        )
        for order in range(len(model["templates"])):
            db.execute(
                "insert into cards values (?,?,?,?,?,-1,0,0,?,0,0,0,0,0,0,0,0,'')",
                (note_id + 1 + order, note_id, deck_id, order, now, position),
            )
    db.commit()
    db.close()
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as package:
        package.write(db_path, "collection.anki2")
        package.writestr("media", "{}")
    os.remove(db_path)
    os.rmdir(folder)
    print(f"{len(notes)} notes, {len(notes) * len(model['templates'])} cards -> {output}")
