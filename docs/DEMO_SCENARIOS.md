# Demo Scenarios

Ten ready-made exercises that showcase a review platform against this corpus.
Each lists an **objective**, **what to try**, **what you'll find**, and the
**answer key** column that confirms the result. The instructor key is
[`ANSWER_KEY.csv`](ANSWER_KEY.csv) (deliberately kept out of the load file so the
data behaves like a fresh, unreviewed collection).

> Load `data/VOL001/DATA/loadfile.dat` (or `loadfile.csv`) first — see
> [FIELD_DEFINITIONS.md](FIELD_DEFINITIONS.md) for delimiters and encoding.

---

## 1. The central investigation — "find the affair" ⭐
**Objective:** reconstruct Queen Catherine Howard's concealed relationship with
Thomas Culpeper across every channel.

**Try this:**
- Search terms: `stair`, `hunt`, `burn this`, `Culpeper`, `Rochford`.
- Filter `FROM`/`TO` for the personal web-mail domain **`ravenmail.tudor`** — a
  classic "custodian using a personal account to evade collection" signal.
- Open the family of **`For_Your_Eyes_Only.docx`** (the love letter) and its
  parent email.
- Ingest the chat **`CHT-0001.rsmf`** ("Privy Chamber (private)") and the voice
  note **`voice_memo_Thursday.wav`** (transcribe it — see exercise 7).
- Thread the discovery: **`Confidential_Deposition_Summary.pdf`** from Cranmer to
  the King, then the examination record.

**What you'll find:** a tightly connected evidence set spanning email, chat and
audio, with explicit spoliation cues ("burn this once read", "let no record
remain").

**Answer key:** `STORYLINE = Howard Affair`, `KEY_DOCUMENT = Yes`.

---

## 2. Privilege review
**Objective:** identify legal advice that should be withheld or logged.

**Try this:** search `privileged`, `Attorney-Client`, `work product`,
`for Your Majesty's eyes only`; review the `Sensitivity` header on emails.

**What you'll find (~13 documents):** e.g. `Opinion_on_Royal_Supremacy.pdf`
(attorney-client), `Schedule_of_Examinations.xlsx` (work product),
`Examination_Transcript.docx`, `Memorandum_on_the_Succession.pdf`. The privilege
signal lives in the document text and headers — *not* in a metadata field — so
reviewers must actually read.

**Answer key:** `SUGGESTED_PRIVILEGE = Yes`.

---

## 3. De-duplication by hash
**Objective:** demonstrate exact-duplicate detection across custodians.

**Try this:** group by `MD5HASH`; look for identical hashes sitting under
different `CUSTODIAN` values (and confirm against `ALLCUSTODIANS`).

**What you'll find (~25 documents):** the same email collected from two
mailboxes, byte-identical. A great lead-in to global vs. custodian dedupe.

**Answer key:** `EXACT_DUPLICATE = Yes`.

---

## 4. Email threading / conversation analysis
**Objective:** reconstruct conversations rather than reading messages in
isolation.

**Try this:** group by `THREADID`, order by `DATESENT`, and follow
`INREPLYTO → MESSAGEID`. Trace the **Royal Supremacy** thread (Great Matter) or
the **affair discovery** thread (Cranmer ↔ Henry).

**What you'll find:** ~200 multi-message threads, including "Re:" chains that
also generate near-duplicate content.

---

## 5. Family relationships
**Objective:** keep parents and attachments together.

**Try this:** reconstruct families with `BEGATTACH`/`ENDATTACH` (and
`PARENTID`/`ATTACHMENTIDS`). Open the **Dissolution valuation** family — the email
forwarding **`Valor_Ecclesiasticus_Summary.xlsx`**.

**Bonus (families + dedupe together):** that same spreadsheet appears in *two*
emails — Sir Richard Rich's original and Cromwell's forward to the King — so it
is one hash living in two families. Perfect for discussing family-aware dedupe.

---

## 6. Foreign-language identification & translation
**Objective:** surface documents that need a linguist.

**Try this:** run language identification, or search distinctive tokens
(`esposa`, `Citatio`, `Roi Très-Chrétien`).

**What you'll find (3 documents):**
- **Spanish** — `De vuestra fiel esposa` (Catherine of Aragon to the King).
- **Latin** — `Citatio_Apostolica.pdf` (the papal citation).
- **French** — `Compliments du Roi Très-Chrétien` (the French embassy).

**Answer key:** `SUBCATEGORY = foreign_language`.

---

## 7. Audio transcription
**Objective:** handle media with no extractable text.

**Try this:** locate `voice_memo_Thursday.wav` (filter `FILEEXTENSION = wav`); note
its extracted text says transcription is required. Run your transcription tool,
then search the transcript.

**What you'll find:** an ~18-second voice note arranging a secret meeting and
asking that no record be kept — directly corroborating exercise 1. Compare your
output against the ground truth in [TRANSCRIPTS.md](TRANSCRIPTS.md).

---

## 8. Chat / short-message review (RSMF)
**Objective:** ingest and review modern chat data.

**Try this:** load the three **`.rsmf`** files as short-message data (Relativity
ingests RSMF natively), or import **`chat_messages.csv`** for a per-message view.
Review `CHT-0001` (the affair), `CHT-0002` (a Privy Council working group) and
`CHT-0003` (texts with Suffolk).

**What you'll find:** conversation-grouped messages with participants, timestamps
and a shared image — and a direct cross-channel link from the affair chat to the
email and audio evidence.

**Answer key:** `RECORDTYPE = Short Message (RSMF)`.

---

## 9. Financial investigation
**Objective:** follow the money in the Dissolution of the Monasteries.

**Try this:** pull the spreadsheets and financial PDFs —
`Valor_Ecclesiasticus_Summary.xlsx`, `Treasury_Receipts_Augmentations.pdf`, and
the routine `Invoice_*.xlsx` / `Treasury_Ledger_*` files. Sort by value; trace
plate and receipts.

**What you'll find:** net annual values and plate by monastery, and receipts into
the Court of Augmentations — a self-contained financial-analysis thread.

**Answer key:** `STORYLINE = Dissolution`.

---

## 10. Culling the noise (recall vs. precision)
**Objective:** suppress junk and measure the effect.

**Try this:** identify spam/newsletter/IT/auto-reply/bounce traffic by sender
domain — `yeoldepizzahut.tudor`, `royal-spanish-lottery.tudor`,
`account-secure-crown.tudor`, `tudortimesweekly.tudor`, `joustingmonthly.tudor` —
and by subject patterns ("Undeliverable:", "Automatic reply:", "Invitation:").
Bulk-tag and suppress, then re-run a substantive search and compare hit counts.

**What you'll find:** roughly 40% of the set is realistic noise — including a
deliberately obvious phishing email for security-awareness demos.

**Answer key:** `CATEGORY = noise` (with `SUBCATEGORY` giving the noise type).

---

### Quick reference — the planted "gem" documents

| Document | Storyline | Why it matters |
|---|---|---|
| `Opinion_on_Royal_Supremacy.pdf` | Great Matter | Privileged legal advice |
| `Schedule_of_Examinations.xlsx` | Anne Boleyn | Work-product witness list |
| `Valor_Ecclesiasticus_Summary.xlsx` | Dissolution | The money |
| `For_Your_Eyes_Only.docx` | Howard Affair | The love letter |
| `CHT-0001.rsmf` | Howard Affair | The affair, in chat |
| `voice_memo_Thursday.wav` | Howard Affair | The affair, in audio |
| `Confidential_Deposition_Summary.pdf` | Howard Affair | The discovery |
| `Citatio_Apostolica.pdf` | Great Matter | Latin (translation) |
| `Memorandum_on_the_Succession.pdf` | Succession | Privileged |
