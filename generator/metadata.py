"""Load-file record model and the standard eDiscovery field set.

One :class:`Record` is produced per document (email, attachment or loose file).
The field list mirrors what a processing engine (LAW, Nuix, Relativity
Processing) emits: family ranges, custodian, email headers, source-file
metadata, hash values, page counts and links to the native and extracted text.

Review work-product (privilege calls, issue tags, "hot" flags) is deliberately
*not* here — that lives in the separate answer key so the corpus behaves like a
freshly processed, not-yet-reviewed set.
"""
from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field

from .model import Addr, render_addr

# Human-readable file-type labels, keyed by extension.
FILETYPE_BY_EXT = {
    "eml": "E-mail Message",
    "docx": "Microsoft Word Document",
    "xlsx": "Microsoft Excel Spreadsheet",
    "pdf": "Adobe PDF Document",
    "png": "PNG Image",
    "txt": "Plain Text Document",
    "ics": "iCalendar Appointment",
    "rsmf": "Short Message (RSMF)",
    "wav": "Audio Recording (WAV)",
    "mp3": "Audio Recording (MP3)",
}

RECORDTYPE = {"email": "E-Mail", "attachment": "Attachment", "loose": "E-Doc / Loose File"}


def fdate(d: dt.datetime | None) -> str:
    return d.strftime("%m/%d/%Y") if d else ""


def ftime(d: dt.datetime | None) -> str:
    return d.strftime("%H:%M:%S") if d else ""


def join_addrs(addrs: list[Addr]) -> str:
    return "; ".join(render_addr(a) for a in addrs)


def page_count(kind: str, text: str) -> int:
    if kind in ("pdf", "docx"):
        return max(1, round(len(text) / 1800))
    if kind == "txt":
        return max(1, round(len(text) / 3000))
    if kind == "eml":
        return max(1, round(len(text) / 2400))
    return 1  # xlsx, png


@dataclass
class Record:
    docid: str = ""
    begbates: str = ""
    endbates: str = ""
    begattach: str = ""
    endattach: str = ""
    parentid: str = ""
    attachmentids: str = ""
    recordtype: str = ""
    custodian: str = ""
    allcustodians: str = ""
    email_from: str = ""
    email_to: str = ""
    email_cc: str = ""
    email_bcc: str = ""
    subject: str = ""
    datesent: str = ""
    timesent: str = ""
    datereceived: str = ""
    timereceived: str = ""
    datecreated: str = ""
    datemodified: str = ""
    author: str = ""
    lastmodifiedby: str = ""
    filename: str = ""
    fileextension: str = ""
    filetype: str = ""
    filesize: str = ""
    pagecount: str = ""
    md5: str = ""
    sha1: str = ""
    messageid: str = ""
    inreplyto: str = ""
    threadid: str = ""
    importance: str = ""
    hasattachments: str = ""
    attachmentcount: str = ""
    nativelink: str = ""
    textlink: str = ""


# Column header -> Record attribute, in load-file order.
FIELDS: list[tuple[str, str]] = [
    ("DOCID", "docid"),
    ("BEGBATES", "begbates"),
    ("ENDBATES", "endbates"),
    ("BEGATTACH", "begattach"),
    ("ENDATTACH", "endattach"),
    ("PARENTID", "parentid"),
    ("ATTACHMENTIDS", "attachmentids"),
    ("RECORDTYPE", "recordtype"),
    ("CUSTODIAN", "custodian"),
    ("ALLCUSTODIANS", "allcustodians"),
    ("FROM", "email_from"),
    ("TO", "email_to"),
    ("CC", "email_cc"),
    ("BCC", "email_bcc"),
    ("SUBJECT", "subject"),
    ("DATESENT", "datesent"),
    ("TIMESENT", "timesent"),
    ("DATERECEIVED", "datereceived"),
    ("TIMERECEIVED", "timereceived"),
    ("DATECREATED", "datecreated"),
    ("DATEMODIFIED", "datemodified"),
    ("AUTHOR", "author"),
    ("LASTMODIFIEDBY", "lastmodifiedby"),
    ("FILENAME", "filename"),
    ("FILEEXTENSION", "fileextension"),
    ("FILETYPE", "filetype"),
    ("FILESIZE", "filesize"),
    ("PAGECOUNT", "pagecount"),
    ("MD5HASH", "md5"),
    ("SHA1HASH", "sha1"),
    ("MESSAGEID", "messageid"),
    ("INREPLYTO", "inreplyto"),
    ("THREADID", "threadid"),
    ("IMPORTANCE", "importance"),
    ("HASATTACHMENTS", "hasattachments"),
    ("ATTACHMENTCOUNT", "attachmentcount"),
    ("NATIVELINK", "nativelink"),
    ("TEXTLINK", "textlink"),
]
