"""The intermediate data model.

Every content generator (narrative, routine, noise, loose files) emits plain
``Email`` / ``Attachment`` / ``LooseFile`` objects. A later "materialise" pass
turns these into real native files, extracted text, hash values and load-file
rows. Keeping generation and materialisation separate keeps each side simple.
"""
from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field

from . import cast

# An address is a (display-name, email) pair.
Addr = tuple[str, str]


def addr(person_key: str, email: str | None = None) -> Addr:
    """Build an address tuple from a cast key (optionally a specific alt)."""
    p = cast.get(person_key)
    return (p.name, email or p.email)


def email_of(a: Addr) -> str:
    return a[1].lower()


def render_addr(a: Addr) -> str:
    return f"{a[0]} <{a[1]}>"


def render_addrs(addrs: list[Addr]) -> str:
    return ", ".join(render_addr(a) for a in addrs)


@dataclass
class Attachment:
    """A child document carried by an email (or, standalone, a loose file)."""

    kind: str                 # 'docx' | 'xlsx' | 'pdf' | 'png' | 'txt'
    filename: str             # e.g. 'Annulment_Petition_v3.docx'
    title: str
    author_key: str           # cast key of the document author
    created: dt.datetime
    modified: dt.datetime
    spec: dict = field(default_factory=dict)   # kind-specific content
    confidentiality: str = ""
    storyline: str = ""
    hot: bool = False
    # populated during materialisation:
    data: bytes = b""
    text: str = ""
    docid: str = ""
    md5: str = ""
    sha1: str = ""


@dataclass
class Email:
    """A single email message (one mailbox copy = one materialised record)."""

    key: str                  # stable unique key (drives Message-ID & dedup)
    date: dt.datetime
    sender: Addr
    to: list[Addr] = field(default_factory=list)
    cc: list[Addr] = field(default_factory=list)
    bcc: list[Addr] = field(default_factory=list)
    subject: str = ""
    body: str = ""
    category: str = "routine"     # 'narrative' | 'routine' | 'noise'
    subcategory: str = ""
    storyline: str = ""
    thread_key: str = ""
    in_reply_to_key: str = ""
    attachments: list[Attachment] = field(default_factory=list)
    importance: str = "Normal"    # Low | Normal | High
    confidentiality: str = ""
    hot: bool = False
    # populated during assembly / materialisation:
    message_id: str = ""
    in_reply_to_id: str = ""
    references: str = ""
    custodian: str = ""           # primary collected custodian (mailbox)
    other_custodians: list[str] = field(default_factory=list)
    is_duplicate: bool = False    # physical cross-custodian duplicate
    docid: str = ""
    md5: str = ""
    sha1: str = ""

    # --- convenience -------------------------------------------------------
    def all_addrs(self) -> list[Addr]:
        return [self.sender, *self.to, *self.cc, *self.bcc]

    def participant_emails(self) -> list[str]:
        return [email_of(a) for a in self.all_addrs()]

    def custodian_participants(self) -> list[str]:
        """Distinct custodian keys among everyone on the email."""
        seen: list[str] = []
        for e in self.participant_emails():
            k = cast.custodian_of_email(e)
            if k and k not in seen:
                seen.append(k)
        return seen


@dataclass
class LooseFile:
    """A standalone (non-email) document collected from a custodian's files."""

    attachment: Attachment
    custodian: str
    other_custodians: list[str] = field(default_factory=list)
    recordtype: str = ""  # override (e.g. "Short Message (RSMF)"); blank => default
