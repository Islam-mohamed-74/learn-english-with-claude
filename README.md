# Learn English with Claude and Anki

This is a full setup for learning English with Claude as your teacher. It was built for an Arabic speaker
(Egyptian) who works as a developer, started at level A2, and wants to reach B2.

You do not study a general book. **You study your own English**: the sentences you need to write, the words
you need to read, and the mistakes you really make.

This page explains the idea, why each part exists, and how to build your own copy.

---

## 1. The idea in six lines

1. Claude reads your old chats and finds your level and your repeated mistakes.
2. Claude writes **cards** for what you need: sentences to write and words to read.
3. You study the cards in **Anki**, a free app, about 45 to 60 minutes a day.
4. While you work with Claude on anything, Claude corrects your English and saves each mistake.
5. When you write in Arabic, Claude shows you the English and saves it. Later it becomes a card.
6. Your cards grow from your own mistakes, so you always study what you need most.

---

## 2. What is Anki, and why Anki?

Anki is a free flashcard app for computer and phone ([apps.ankiweb.net](https://apps.ankiweb.net)).

A card has a front (the question) and a back (the answer). You see the front, you answer, then you tell Anki
if it was easy or hard.

**Why it works:** we forget new things fast. Anki shows each card again just before you forget it: after 1
day, then 4 days, then 10 days, then a month. Easy cards come rarely. Hard cards come often. This is called
*spaced repetition*. It is the most efficient way to keep thousands of things in memory.

**Why it fits this plan:** you do not need a teacher every day. Anki is the daily work. Claude only makes the
cards and corrects you when you chat.

---

## 3. The parts, and why each one exists

### Writing: chunks, not single words

A **chunk** is a short ready sentence, like `Can you check this for me?` or `It worked yesterday, but it
doesn't work today.`

**Why chunks:** a learner at A2 knows many words but puts them in the wrong order: `are you have all message`.
A chunk comes with the right word order and the right small words (`a`, `the`, `to`, `do`). You learn the
grammar without studying grammar.

**Where the chunks come from:** from your own messages, in English and in Arabic. They are the sentences you
really need, in correct English, with a translation in your own dialect.

**How the card works:** you see the Arabic and you **type** the English. Anki shows your wrong letters in red.
Anki is the checker, so you can practise alone. A second card goes the other way, English to Arabic.

### Linking words

Words like `because`, `although`, `unless`, `as soon as`, `so that`, `however`.

**Why:** they are the main difference between A2 writing and B1 or B2 writing. A2 writes one idea per
sentence. B1 joins two ideas: `Although it works, I don't like the design.` They are stored as chunks in the
writing deck, in groups by job: reason, contrast, condition, time, result, adding.

### Reading: the words your teacher really uses

Reading here means **understanding**, not pronunciation.

**How the list was made:** Claude counted every word in its own replies to the learner (143,000 words in 68
chats). The result: about 1,650 word families cover 98% of everything Claude writes to him. He already used
735 of them himself. So about 800 words were left to learn, and the most used words come first.

**Why 98%:** when you know 98% of the words in a text, you meet 1 unknown word in 50, and you can guess it.

**How the card works:** the front has the word and a real sentence. The back has the meaning, the sentence in
Arabic, and a **memory hook**.

**Why hooks:** a strange picture is easier to remember than a translation. Claude writes the hooks, in your
dialect. Two kinds:
- a sound trick: `cost` sounds like كوسة, so تخيل كيلو الكوسة بقى بـ 500 جنيه. دي التكلفة!
- the parts of the word: `refund` = `re` (back) + `fund` (money), so the money runs back to your pocket.

### The mistake log

File: `writing/my-mistakes.md`. It has two tables:

- **Spelling:** each word you spell wrong, and how many times. The top of the table is where to focus.
- **Mistake log:** each corrected sentence with its date and its **grammar rule**.

**Why:** after a month you ask Claude "which grammar rules do I need to study?" Claude counts the rules in the
log and gives you a short, true list. You study three rules, not a whole grammar book.

### The Arabic log

File: `writing/arabic-log.md`.

**Why:** when you write to Claude in Arabic, it means you did not know how to say it in English. That sentence
is the most useful thing to learn. Claude shows the English and saves the pair. When you say "add the Arabic
log", the new sentences become cards.

### The rule for every chat

One small file, `~/.claude/CLAUDE.md`, is read by every Claude Code chat in every project. It tells Claude to
correct your English, save your mistakes, and log your Arabic, **after** it finishes your real work.

**Why:** Claude does not remember old chats. Without this file, a new chat knows nothing about your English
plan. With it, every chat is also a small English lesson.

---

## 4. What is in this folder

```
CLAUDE.md        what every new chat in this folder reads first: who you are, your goal, the rules
PLAN.md          your plan: goal, where you are, daily routine, stages
PROGRESS.md      one line for each session and each level check
global-rule.md   the text to put in ~/.claude/CLAUDE.md (the rule for every chat)
writing/         the chunks, your mistake log, your Arabic log
reading/         the reading words
listening/       empty: start later
speaking/        empty: start later (shadowing, pronunciation)
tools/           scripts that build the Anki files from the text files
```

**How the cards are stored:** each deck is a plain text file, one card per line. You can read it and edit it.
A script turns it into an Anki file (`.apkg`). When you add lines and build again, Anki adds the new cards and
keeps your progress on the old ones.

**What this template already has:** 77 linking-word chunks, and a small sample of 20 chunks and 20 reading
words so you can see the format. The translations and hooks are in Egyptian Arabic. Your own
chunks and words must come from **your** chats.

---

## 5. How to set up your own copy

You need: [Anki](https://apps.ankiweb.net), [Claude Code](https://claude.com/claude-code), and
[Python 3](https://www.python.org/downloads/).

1. Copy this folder to your computer. Name it what you like, for example `English\Claude-teacher`.
2. Open Claude Code in that folder.
3. Paste the **start prompt** from section 8.
4. Claude reads your chats, tells you your level, fills in the files, and builds your decks.
5. In Anki: **File**, then **Import**, and pick each `.apkg` file.
6. Study every day with the routine below.

**Import options in Anki:** turn off "Import any learning progress" and "Import any deck presets". Keep
"Merge note types" on, and keep both "Update" options on "If newer".

---

## 6. The daily routine (45 to 60 minutes)

1. Finish the Anki reviews that are due.
2. Learn 25 new reading words.
3. Learn 10 new writing chunks. Type the English.
4. Optional: when you have a chat open, write 3 to 5 sentences and let Claude correct them.

If the reviews take more than 60 minutes, lower the new cards for a week. Do not stop.

Once a month, ask Claude to test your level and write the result in `PROGRESS.md`.

---

## 7. Honest limits

- The numbers in this plan (days, hours, word counts) are estimates. Learners differ.
- A2 to B2 usually takes about 400 to 600 hours of study. At one hour a day that is more than a year.
- Cards are not enough alone. You also need to read real text and write real messages every day.
- Listening and speaking are not built yet. They come after the first stage.
- Claude makes mistakes too. If a translation or a hook sounds wrong in your dialect, tell Claude and fix it.

---

## 8. The start prompt

Paste this into Claude Code, in your copy of this folder. Change the parts in capital letters.

```
Read README.md, CLAUDE.md and global-rule.md in this folder. I want the same setup for me.

About me: my name is NAME. My first language is ARABIC DIALECT (for example Egyptian Arabic). My job is JOB.
My goal is English level B2.

Do this in order, and tell me what you did after each step:
1. Read my saved Claude Code chats and tell me my English level (A1 to C2), with my 5 most common mistakes.
2. Fill in CLAUDE.md, PLAN.md and PROGRESS.md for me.
3. Writing: make chunks from my own messages, English and Arabic, with translations in my dialect. Keep the
   linking-word chunks that are already here. Add them to writing/Claude_chunks_for_writing.txt.
4. Reading: count the words in your replies to me, find the words I do not use myself, and write a card for
   each one in reading/Claude_words_for_reading.txt, with a real sentence and a memory hook in my dialect.
   Most used words first.
5. Fill in the spelling table and the mistake log in writing/my-mistakes.md from my chats.
6. Build the two Anki files with the scripts in tools/.
7. Show me the text of global-rule.md with my folder path in it, and ask me before you write it to
   ~/.claude/CLAUDE.md.

Use simple English with me: short sentences, one idea per sentence.
```

The same prompt in Arabic, if you prefer to start in Arabic:

```
اقرأ README.md و CLAUDE.md و global-rule.md اللي في الفولدر ده. أنا عايز نفس النظام ده ليا.

عني: اسمي NAME. لغتي الأولى ARABIC DIALECT. شغلي JOB. هدفي أوصل B2 في الإنجليزي.

اعمل الخطوات اللي في الـ start prompt الإنجليزي في README.md بالترتيب، وبعد كل خطوة قولي عملت إيه.
رد عليا بإنجليزي بسيط: جمل قصيرة، وفكرة واحدة في كل جملة.
```
