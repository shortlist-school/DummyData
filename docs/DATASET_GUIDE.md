# Dataset Guide

This guide explains what the corpus *is*, how it is put together, and what makes
it behave like a real collection. For ready-to-run demonstrations see
[DEMO_SCENARIOS.md](DEMO_SCENARIOS.md); for the full cast see
[CHARACTERS.md](CHARACTERS.md); for the load-file schema see
[FIELD_DEFINITIONS.md](FIELD_DEFINITIONS.md).

## Premise

The court of Henry VIII, conducting the business of the realm over email, chat
and the occasional voice note. The history is real and the dates are accurate;
the technology is a deliberate, charming anachronism. Because every byte is
fabricated there is **no real personal data** — but the set still exhibits all
the structure an eDiscovery professional cares about: families, threads,
duplicates, hashes, custodians and noise.

The period runs **1525–1547**, from the first stirrings of the King's annulment
to his death.

## The six collected custodians

A real matter collects specific mailboxes. We "collected" six, chosen so their
mailboxes intersect every storyline:

| Custodian | Why they're central |
|---|---|
| **King Henry VIII** | The hub; touches every storyline. |
| **Thomas Cromwell** | The administrative engine; runs the Dissolution; falls in 1540. |
| **Archbishop Thomas Cranmer** | Handles the annulments; receives the affair tip-off. |
| **Queen Anne Boleyn** | Storyline 2; her rise and fall. |
| **Queen Catherine Howard** | Storyline 5 — the central investigation. |
| **Queen Catherine Parr** | The survivor; winds the story down. |

Everyone else — Wolsey, More, the Boleyns, Culpeper, Dereham, Lady Rochford,
ambassadors, spammers — is a **non-custodian**. Their mail appears *only* because
they wrote to a custodian, which is exactly how a real collection behaves.

## The six storylines

Each storyline has a hand-crafted spine of "gem" documents surrounded by
procedurally generated, in-period traffic.

### 1. The King's Great Matter (1527–1533)
Henry tasks Wolsey with securing an annulment from Catherine of Aragon; Wolsey
fails and falls; Cromwell and Cranmer engineer the break with Rome.
**Key documents:** `Opinion_on_Royal_Supremacy.pdf` (privileged legal advice),
`Decree_of_Annulment_1533.docx`, Catherine's dignified protests (one in Spanish).

### 2. The Rise & Fall of Anne Boleyn (1533–1536)
Marriage, the birth of Elizabeth, the miscarriage, and the swift investigation
and trial. **Key documents:** `Schedule_of_Examinations.xlsx` (work-product
witness list), `Indictment_Crown_Matter.pdf`, Anne's final letter.

### 3. The Dissolution of the Monasteries (1535–1540)
Cromwell's great survey of monastic wealth and its transfer to the Crown — the
financial-investigation thread. **Key documents:**
`Valor_Ecclesiasticus_Summary.xlsx` (net values and plate by house),
`Treasury_Receipts_Augmentations.pdf`.

### 4. The Cleves Misunderstanding (1539–1540)
The flattering-portrait episode and an amicable annulment. **Key documents:**
`Portrait_Anne_of_Cleves_Holbein.png`, the King's wry reaction, the annulment.

### 5. The Howard Affair (1540–1542) ⭐ the central investigation
Queen Catherine Howard's concealed correspondence with Thomas Culpeper, brokered
by Lady Rochford, plus her past with Francis Dereham. It is deliberately
*discoverable* and spans every channel:

- **Email** over a personal web-mail account (`ravenmail.tudor`) to evade the
  household post — including the love letter `For_Your_Eyes_Only.docx`.
- **Chat** — the conversation `CHT-0001.rsmf` ("Privy Chamber (private)").
- **Audio** — the voice note `voice_memo_Thursday.wav`.
- **Spoliation cues** — "burn this once read", "let no record remain".
- **The discovery** — `Confidential_Deposition_Summary.pdf` from Cranmer to the
  King, then the examination record.

This is the storyline most demos build around: the evidence is real, layered
across data types, and connected by families, threads, search terms and dates.

### 6. Succession & Legacy (1543–1547)
Catherine Parr survives, organises the royal nursery, narrowly avoids the
religious conservatives, and the realm looks to the future. **Key documents:**
`Royal_Household_Education_Plan.xlsx`, `Memorandum_on_the_Succession.pdf`
(privileged).

## Specialist data types

- **Chat / RSMF.** Three conversations as native Relativity Short Message Format
  files (`CHT-0001`–`CHT-0003.rsmf`): the affair, a Privy Council working group,
  and casual "texts" with the Duke of Suffolk. Each is an RFC-822 container
  holding an `rsmf_manifest.json` (participants + time-ordered events) and any
  shared media. `chat_messages.csv` is the per-message equivalent.
- **Foreign-language documents.** A Spanish appeal (`De vuestra fiel esposa`), a
  Latin papal citation (`Citatio_Apostolica.pdf`) and a French diplomatic note
  (`Compliments du Roi Très-Chrétien`).
- **Audio.** `voice_memo_Thursday.wav` — a real (robotic TTS) voice note with no
  extractable text; transcript in [TRANSCRIPTS.md](TRANSCRIPTS.md).

## The noise

Roughly 40% of the set is realistic chaff addressed to custodians: Pizza Hut
promotions, an advance-fee "Spanish lottery", an (obvious) phishing attempt, the
*Tudor Times Weekly* and *Jousting Monthly* newsletters (which quietly carry real
historical facts), IT/scriptorium notices, out-of-office auto-replies,
delivery-failure bounces, calendar invites, and vendor marketing. This is what
makes culling, search-term precision and noise-suppression demos meaningful.

## What makes the metadata "corroborative"

The set is internally consistent in the ways a real, processed collection is:

- **Dates line up** with real history and with each other (documents are created
  before the emails that send them; the affair clusters in 1541).
- **Hashes are real** — every `MD5HASH`/`SHA1HASH` is computed from the actual
  native bytes, so dedupe and integrity checks genuinely work.
- **Families** are wired through `BEGATTACH`/`ENDATTACH`, `PARENTID` and
  `ATTACHMENTIDS`.
- **Threads** reconstruct from `MESSAGEID`/`INREPLYTO`/`REFERENCES` and `THREADID`.
- **Exact duplicates** exist across custodians (same email collected from two
  mailboxes → identical hash) for dedupe demos.
- **Near-duplicates** exist via forwarded chains and `_rev2` draft pairs.

## How the generator works

The corpus is produced by a small, seeded Python package in `generator/`:

| Module | Responsibility |
|---|---|
| `config.py` | Seed, date range, volumes, output paths, Concordance delimiters |
| `cast.py` | People, mailboxes, roles, custodian flags, active windows |
| `corpora.py` | Shared content banks (salutations, facts, tasteful quips, places) |
| `scenes.py` | The bespoke storyline spine + foreign-language documents |
| `narrative.py` | Storyline filler around the spine |
| `routine.py` | Cross-cutting court administration |
| `noise.py` | Spam, phishing, newsletters, IT notices, auto-replies, bounces |
| `loose.py` | Standalone e-docs (ledgers, proclamations, images, drafts) |
| `chat.py` | RSMF chat files + per-message CSV |
| `media.py` | Audio voice-note generation (espeak-ng) |
| `attachments.py` | Native builders: docx, xlsx, pdf, png, txt, binary |
| `eml_builder.py` | RFC-822 `.eml` assembly with threading headers |
| `assemble.py` | Custodian attribution, duplicates, threading, ordering |
| `materialise.py` | Bates numbering, file writing, hashing, record building |
| `metadata.py` | The load-file field set and per-document record |
| `loadfiles.py` | Concordance `.dat` and CSV writers |
| `build.py` | Orchestrates the whole build |

### Reproducibility

The build is seeded and pins `PYTHONHASHSEED`, and every native is generated with
fixed timestamps and identifiers. As a result a given configuration rebuilds
**byte-for-byte identically**, hash values included — so the dataset is a stable
asset you can cite, share and diff.

```bash
python -m generator.build                         # default ~2,000 docs
python -m generator.build --noise 3000 --routine 2000 --loose 600   # scale up
```

To rework the story, edit `cast.py`, `scenes.py` and `narrative.py`; to retune
volumes or the period, edit `config.py`.

## A note on tone

This is a professional asset. The Tudor era's executions are handled with
light, pun-only gallows humour ("let us not lose our heads over the seating
plan"); there is nothing graphic and no profanity, and the real suffering of
historical figures is never made the butt of a joke. Everything is fictional.
