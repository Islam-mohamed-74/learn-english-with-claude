# My English plan

**Goal:** B2 in general English. **First step:** B1.
**Teacher:** Claude. **Start:** FILL IN. **Level at start:** FILL IN.

## Where we are (updated FILL IN)

| Skill | Done | Left |
|---|---|---|
| Writing | FILL IN | FILL IN |
| Reading | FILL IN | FILL IN |
| Listening | Nothing yet | Discuss with Claude first. |
| Speaking | Nothing yet | Discuss with Claude first (shadowing, pronunciation). |

**Working on now:** Stage 1. **Next step:** import the two decks and do the daily routine.

## My daily routine (45 to 60 minutes)

1. **Anki reviews first.** Finish every card that is due in all decks.
2. **New reading words: 25.** Deck `Claude::Words for Reading`.
3. **New writing chunks: 10.** Deck `Claude::Chunks for Writing`. I type the English, and Anki shows my mistakes in red.
4. **Optional, when I have a chat open:** write 3 to 5 sentences. Claude corrects them and saves the mistakes
   in `writing/my-mistakes.md`.

Steps 1 to 3 need only Anki. I do not need a chat every day.

If the reviews take more than 60 minutes, I lower the new cards for a week. I do not stop.

## The stages

### Stage 1: write to Claude and understand Claude (about 2 to 3 months)

- Finish the writing chunks and the reading words.
- Fix my repeated mistakes (`writing/my-mistakes.md`).
- **Done when:** I write a 5-sentence message with 1 mistake or none, and I read a Claude report and stop at
  fewer than 1 word in 50.

### Stage 2: B1 in general English

- General words: a general word list. Decide with Claude.
- Read short general texts every day: an article, tweets, normal chats.
- Write longer: one paragraph a day, corrected by Claude.
- Start listening and shadowing. Discuss the method with Claude first.

### Stage 3: B2

- Longer reading and listening with no help.
- Write emails and reports. Join two or three ideas in one correct sentence.
- Speaking practice.

## Checking my level

Once a month Claude tests me and writes the result in `PROGRESS.md`.

## One honest number

A2 to B2 usually takes about 400 to 600 hours of study. This is a common estimate, not exact. At 1 hour a
day it is more than a year. Small steps, B1 first.

## How to add cards

- **Ask Claude:** "add these chunks" or "add these words".
- **From my first language:** when I write to Claude in it, the English is saved in `writing/arabic-log.md`.
  I say "add the Arabic log" and the new sentences go into the writing deck.
- **Or by myself:** add lines to the `.txt` file in `writing/` or `reading/`, then run
  `python tools/build_deck.py` or `python tools/build_reading_deck.py`, then import the `.apkg` in Anki.
