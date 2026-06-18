# Load-File Field Definitions (Data Dictionary)

The corpus ships with two equivalent load files in `data/VOL001/DATA/`:

| File | Format | Use |
|---|---|---|
| `loadfile.dat` | Concordance / Relativity, UTF-8 | Primary load file for review platforms |
| `loadfile.csv` | RFC-4180 CSV, UTF-8 | Universal fallback / open in a spreadsheet |
| `chat_messages.csv` | RFC-4180 CSV, UTF-8 | Supplementary per-message chat load file |

`loadfile.dat` and `loadfile.csv` contain the **same 38 fields** and one row per
document (~2,000 rows). `chat_messages.csv` is a separate, narrower file giving
one row **per chat message** (an alternative to ingesting the native `.rsmf`
files); its columns are `CONVERSATIONID`, `CONVERSATIONNAME`, `CUSTODIAN`,
`MESSAGEID`, `TIMESTAMP`, `SENDER`, `SENDEREMAIL`, `BODY`, `HASATTACHMENT`,
`RSMF_NATIVE`.

### Record types you will see in `RECORDTYPE`

`E-Mail`, `Attachment`, `E-Doc / Loose File`, and `Short Message (RSMF)` (the
chat containers). Notable file extensions include the usual `eml/docx/xlsx/pdf/
png/txt`, plus `ics` (calendar), `rsmf` (chat), and `wav` (audio — carries no
extracted text and requires transcription).

## Delimiters & encoding (the `.dat`)

These are the industry-standard Concordance delimiters. Configure your platform's
import to match:

| Setting | Character | Code |
|---|---|---|
| Column / field delimiter | `¶` | ASCII 20 (0x14) |
| Text qualifier | `þ` | ASCII 254 (0xFE) |
| In-field newline | `®` | ASCII 174 (0xAE) |
| Multi-value separator | `; ` | (within FROM/TO/CC/etc.) |
| Encoding | UTF-8 with BOM | — |
| Record separator | CRLF | `\r\n` |

> **Why UTF-8?** The data contains accents, em-dashes and currency symbols. UTF-8
> (the modern convention all major platforms accept) preserves them losslessly,
> whereas legacy single-byte ANSI would mangle them. The delimiter characters
> above are parsed by character, not by byte.

## Fields (in column order)

| Field | Description |
|---|---|
| `DOCID` | Unique document control number (Bates). The primary key for the record. |
| `BEGBATES` | Beginning Bates number. Equal to DOCID for native-only productions. |
| `ENDBATES` | Ending Bates number. Equal to BEGBATES for single-item natives. |
| `BEGATTACH` | First Bates number in the document **family** (the parent email). |
| `ENDATTACH` | Last Bates number in the family (the final attachment, or the doc itself). |
| `PARENTID` | DOCID of the parent email. Blank for parent emails and loose files. |
| `ATTACHMENTIDS` | Semicolon-separated DOCIDs of child attachments (populated on parents). |
| `RECORDTYPE` | `E-Mail`, `Attachment`, or `E-Doc / Loose File`. |
| `CUSTODIAN` | The mailbox / source the document was collected from. |
| `ALLCUSTODIANS` | Every custodian who holds a copy (the dedupe 'other custodians' field). |
| `FROM` | Sender (emails only), as `Display Name <address>`. |
| `TO` | To recipients, semicolon-separated (emails only). |
| `CC` | CC recipients (emails only). |
| `BCC` | BCC recipients, present on the sender's copy (emails only). |
| `SUBJECT` | Email subject line (emails only). |
| `DATESENT` | Date sent, `MM/DD/YYYY` (emails; attachments inherit the family date). |
| `TIMESENT` | Time sent, `HH:MM:SS` 24-hour. |
| `DATERECEIVED` | Date received, `MM/DD/YYYY`. |
| `TIMERECEIVED` | Time received, `HH:MM:SS`. |
| `DATECREATED` | Document-property created date (attachments & loose files). |
| `DATEMODIFIED` | Document-property last-modified date (attachments & loose files). |
| `AUTHOR` | Document author from file properties; the sender for emails. |
| `LASTMODIFIEDBY` | Last person to modify the document (file properties). |
| `FILENAME` | Original file name of the native. |
| `FILEEXTENSION` | File extension (`eml`, `docx`, `xlsx`, `pdf`, `png`, `txt`, `ics`). |
| `FILETYPE` | Human-readable file-type label. |
| `FILESIZE` | Size of the native file in bytes. |
| `PAGECOUNT` | Estimated page / item count. |
| `MD5HASH` | MD5 of the native bytes. Use for de-duplication and integrity checks. |
| `SHA1HASH` | SHA-1 of the native bytes. |
| `MESSAGEID` | RFC-822 Message-ID (emails). Anchor for threading. |
| `INREPLYTO` | Message-ID of the email this message replies to. |
| `THREADID` | Conversation identifier; groups all messages in a thread. |
| `IMPORTANCE` | `Low`, `Normal` or `High` (from the email priority header). |
| `HASATTACHMENTS` | `Y`/`N` — whether an email carries attachments. |
| `ATTACHMENTCOUNT` | Number of attachments in the family. |
| `NATIVELINK` | Relative path to the native file (from the volume root, e.g. `VOL001/`). |
| `TEXTLINK` | Relative path to the extracted-text file. |

## Families & threading at a glance

- **Reconstruct a family:** all records sharing a `BEGATTACH` value belong to one
  family; the parent email's `ATTACHMENTIDS` lists its children, and each child's
  `PARENTID` points back to the parent.
- **Reconstruct a thread:** group by `THREADID`, then order by `DATESENT`; the
  `INREPLYTO` → `MESSAGEID` links give the exact reply tree.
- **Find duplicates:** group by `MD5HASH`; identical hashes across different
  `CUSTODIAN` values are exact cross-custodian duplicates.

## The answer key (kept separate on purpose)

Review work-product — which documents are "key," which are likely privileged,
which storyline a document belongs to — is **not** in the load file, so the set
behaves like a freshly processed, not-yet-reviewed collection. That information
lives in [`ANSWER_KEY.csv`](ANSWER_KEY.csv) for instructors and demo operators.
