# The Tudor eDiscovery Dataset

A rich, fully synthetic eDiscovery corpus set in the court of **King Henry VIII** —
built as a modern, narrative-driven alternative to the tired Enron dataset, with
**no real personal data anywhere in it.**

Henry, his six wives and their advisors conduct the affairs of state (and one or
two affairs of the heart) over email. The events are historically accurate; the
medium is gloriously anachronistic. Underneath the storytelling it behaves
exactly like a real collection: proper document **families**, continuous Bates
numbering, **real hash values**, email **threading**, exact and near
**duplicates**, realistic **noise**, and standard load files that ingest into any
review platform.

> **Everything here is fictional.** All names are used in a historical/parody
> context, all email addresses use a reserved fictional `.tudor` domain, and no
> message, document or image reproduces real private data. See
> [Tone & Safety](#tone--safety).

---

## Why this exists

The Enron corpus has served the industry for two decades, but it is dated, it is
everywhere, and — more importantly — it contains the **real private correspondence
of real people**, which is increasingly uncomfortable to put on a screen in front
of clients. This dataset was built to solve that:

| Requirement | How this set delivers |
|---|---|
| No real personal data | 100% generated; reserved `.tudor` domains; placeholder imagery only |
| A narrative you can follow | Six interlocking storylines across 1525–1547 |
| Variety of document types | `.eml`, `.docx`, `.xlsx`, `.pdf`, `.png`, `.txt`, `.ics`, `.rsmf`, `.wav` |
| Proper family relationships | Parent emails with child attachments, family Bates ranges |
| Corroborative metadata | Dates, authors, threads and hashes all line up across the set |
| Realistic noise | Spam, phishing, newsletters, IT notices, auto-replies, bounces |
| Something to *find* | A concealed-affair storyline planted as the central investigation |
| Chat / short-message data | Native **RSMF** files (Relativity chat) + a per-message CSV |
| Foreign-language docs | Genuine Spanish, Latin and French documents (translation exercise) |
| Audio for transcription | A real voice-note `.wav` with no extracted text (transcription exercise) |
| Safe for clients | Tasteful, pun-only humour; nothing graphic; no profanity |

---

## What's in the box (default build)

Approximately **2,000 documents** across **six collected custodians**, spanning
1525–1547:

- **1,653** emails · **188** attachments · **165** loose files · **3** RSMF chats
- File-type mix: `eml` · `docx` · `xlsx` · `pdf` · `png` · `ics` · `txt` · `rsmf` (chat) · `wav` (audio)
- **3** chat conversations (RSMF) + a **16-row** per-message chat load file
- **3** foreign-language documents (Spanish, Latin, French) and **1** audio voice note
- **~25** exact cross-custodian duplicates (for dedupe demos)
- **200** multi-message conversation threads
- **~26** planted "key documents" and **~13** privileged documents
- ~12 MB of native files

Collected custodians: **King Henry VIII, Thomas Cromwell, Archbishop Thomas
Cranmer, Queen Anne Boleyn, Queen Catherine Howard, Queen Catherine Parr.**
(Everyone else — Wolsey, More, Culpeper, the Boleyns, ambassadors, spammers — is
a non-custodian whose mail only appears because they wrote to a custodian.)

---

## The six storylines

1. **The King's Great Matter** — the annulment from Catherine of Aragon, Wolsey's
   fall, and the break with Rome.
2. **The Rise & Fall of Anne Boleyn** — marriage, Elizabeth's birth, the adultery
   investigation and trial.
3. **The Dissolution of the Monasteries** — Cromwell's great survey; valuation
   spreadsheets and treasury accounts.
4. **The Cleves Misunderstanding** — the flattering-portrait episode and an
   amicable annulment.
5. **The Howard Affair** ⭐ *the central investigation* — concealed
   correspondence over a personal web-mail account, a go-between, a love-letter
   attachment, "burn this" spoliation hints, and the discovery.
6. **Succession & Legacy** — Catherine Parr survives; the realm looks to the
   future.

Full detail in **[docs/DATASET_GUIDE.md](docs/DATASET_GUIDE.md)**.

---

## Repository layout

```
.
├── README.md                     ← you are here
├── requirements.txt              ← Python dependencies (pinned)
├── build.sh                      ← one-command (re)build
├── docs/
│   ├── DATASET_GUIDE.md          ← the narrative, custodians and design
│   ├── CHARACTERS.md             ← full cast + email addresses + history
│   ├── FIELD_DEFINITIONS.md      ← load-file data dictionary + delimiters
│   ├── DEMO_SCENARIOS.md         ← ready-made demo exercises
│   ├── ANSWER_KEY.csv            ← instructor key (kept out of the load file)
│   └── TRANSCRIPTS.md            ← ground-truth audio transcripts (instructor aid)
├── generator/                    ← the seeded Python generator
└── data/
    └── VOL001/                   ← a standard production volume
        ├── NATIVES/              ← native files, sharded into subfolders
        ├── TEXT/                 ← extracted text, one .txt per document
        └── DATA/
            ├── loadfile.dat      ← Concordance/Relativity (þ ¶ ® delimited, UTF-8)
            ├── loadfile.csv      ← universal CSV mirror (same fields)
            ├── chat_messages.csv ← per-message chat load file (RSMF alternative)
            └── build_manifest.json
```

## Specialist data types

Three extra data types round the set out beyond email and e-docs:

- **Chat / short messages (RSMF).** Three conversations ship as native
  **Relativity Short Message Format** `.rsmf` files (an RFC-822 container with an
  `rsmf_manifest.json` and shared media) — the format Relativity ingests as chat.
  The affair is *also* conducted over chat, so it correlates with the email
  trail. For platforms that prefer structured rows, `chat_messages.csv` carries
  the same messages one-per-row with conversation grouping.
- **Foreign-language documents (translation).** A Spanish appeal from Catherine
  of Aragon, a Latin papal citation (PDF), and a French diplomatic note — genuine,
  short, client-safe text for foreign-language identification and translation
  demos.
- **Audio (transcription).** A real `.wav` voice note (carried as an email
  attachment) with **no extracted text**, so it must be transcribed. The
  ground-truth transcript is in [docs/TRANSCRIPTS.md](docs/TRANSCRIPTS.md).
  Regenerating audio needs `espeak-ng` (`apt-get install espeak-ng`); the
  rendered file is already committed, so a rebuild without it simply omits audio.

---

## Loading it into a review platform

The data ships as a standard production volume — load it the way you would any
processed collection.

- **Load file:** `data/VOL001/DATA/loadfile.dat`
  - Encoding **UTF-8 (with BOM)**
  - Field delimiter **ASCII 20 (¶)**, text qualifier **þ (ASCII 254)**, in-field
    newline **® (ASCII 174)** — the standard Concordance delimiters
  - First row is the header
- **Prefer a spreadsheet?** Use `loadfile.csv` (UTF-8, comma-delimited, RFC-4180).
- **Natives** are referenced by the `NATIVELINK` column (relative to `VOL001/`).
- **Extracted text** is referenced by the `TEXTLINK` column.
- **Families** reconstruct from `BEGATTACH`/`ENDATTACH` (and `PARENTID`/
  `ATTACHMENTIDS`); **threads** from `MESSAGEID`/`INREPLYTO`/`THREADID`.

Every field is documented in **[docs/FIELD_DEFINITIONS.md](docs/FIELD_DEFINITIONS.md)**.

---

## Regenerating or rescaling

The corpus is produced by a seeded generator, so a given configuration always
rebuilds **byte-for-byte identically** (hashes included).

```bash
pip install -r requirements.txt
./build.sh                      # or: python -m generator.build

# scale the noise/routine/loose volumes up or down:
python -m generator.build --routine 2000 --noise 3000 --loose 600
```

To change the narrative, cast, dates or volumes, edit `generator/config.py`,
`generator/cast.py` and `generator/scenes.py`. The generator's design is
described in [docs/DATASET_GUIDE.md](docs/DATASET_GUIDE.md#how-the-generator-works).

---

## Tone & Safety

This is a **professional demonstration asset.** It is designed to be shown to
clients without a second thought:

- **Entirely fictional.** No real private data, no real images, no real email
  addresses (the `.tudor` TLD does not exist).
- **Tasteful humour only.** The Tudor period is famous for its beheadings; the
  jokes here are strictly pun-based gallows humour ("let us not lose our heads
  over the seating plan"). Nothing graphic, no profanity, nothing that mocks the
  real suffering of historical figures.
- **Historically educational.** Real dates and facts are woven throughout, so the
  set quietly teaches Tudor history alongside the eDiscovery tradecraft.

If you intend to present a specific document live, you can always confirm its
content first via the extracted text in `TEXT/`.
