"""Authoring helpers shared by every content generator.

These keep the storyline scripts and the procedural generators terse: a short
``mail(...)`` / ``doc(...)`` call instead of a wall of keyword arguments, plus
address resolution that accepts cast keys, ``(key, alt-email)`` pairs, or raw
``(name, email)`` tuples for external personas.
"""
from __future__ import annotations

import datetime as dt
import itertools
import random

from . import cast
from .model import Addr, Attachment, Email, addr

_key_counter = itertools.count(1)


def newkey(prefix: str) -> str:
    """Stable, monotonically increasing message key, e.g. ``gm-00042``."""
    return f"{prefix}-{next(_key_counter):05d}"


def who(spec) -> Addr:
    """Resolve an address spec to an ``(name, email)`` tuple.

    Accepts a cast key (``'henry'``), a ``(key, alt_email)`` pair, or an
    explicit ``(display_name, email)`` tuple for non-cast personas.
    """
    if isinstance(spec, tuple):
        first, second = spec
        if first in cast.BY_KEY:
            return addr(first, second)
        return (first, second)
    return addr(spec)


def whos(specs) -> list[Addr]:
    return [who(s) for s in (specs or [])]


def ext(name: str, email: str) -> Addr:
    """An explicit external address (spam senders, vendors, etc.)."""
    return (name, email)


def mail(prefix: str, date: dt.datetime, sender, *, to=None, cc=None, bcc=None,
         subject: str = "", body: str = "", category: str = "routine", **kw) -> Email:
    return Email(
        key=newkey(prefix), date=date, sender=who(sender),
        to=whos(to), cc=whos(cc), bcc=whos(bcc),
        subject=subject, body=body, category=category, **kw,
    )


def doc(kind: str, filename: str, title: str, author: str, created: dt.datetime,
        modified: dt.datetime | None = None, spec: dict | None = None, **kw) -> Attachment:
    return Attachment(
        kind=kind, filename=filename, title=title, author_key=author,
        created=created, modified=modified or created, spec=spec or {}, **kw,
    )


def compose(salutation: str, paragraphs: list[str], sign_off: str, signer: str,
            footer: str = "") -> str:
    """Assemble a typical letter-style email body."""
    blocks = [salutation, ""]
    for p in paragraphs:
        blocks.append(p)
        blocks.append("")
    blocks.append(sign_off)
    blocks.append(signer)
    if footer:
        blocks.extend(["", "--", footer])
    return "\n".join(blocks).strip() + "\n"


def at(year: int, month: int, day: int, hour: int = 9, minute: int = 0) -> dt.datetime:
    return dt.datetime(year, month, day, hour, minute)


def jitter(base: dt.datetime, max_minutes: int = 240) -> dt.datetime:
    """Nudge a timestamp by a deterministic-but-random amount."""
    return base + dt.timedelta(minutes=random.randint(0, max_minutes))


def thread(emails: list[Email], thread_key: str) -> list[Email]:
    """Wire a list of emails into one conversation (sets reply/reference keys)."""
    prev_key = ""
    for e in emails:
        e.thread_key = thread_key
        if prev_key:
            e.in_reply_to_key = prev_key
        prev_key = e.key
    return emails
