"""Assembly: custodian attribution, deduplication population, threading, order.

Takes the raw output of every generator and turns it into the ordered stream of
"units" (emails and loose files) that the materialiser will number and write.
This is where the corroborative behaviour is wired in:

* each email is attributed to the custodian mailbox it was collected from;
* a controlled share of multi-custodian emails are physically duplicated so the
  dedupe-by-hash demo has real exact duplicates to find;
* Message-ID / In-Reply-To / References headers are resolved across whole
  conversations so email threading reconstructs cleanly.
"""
from __future__ import annotations

import copy
import datetime as dt
import random

from . import cast, config
from .eml_builder import message_id_for
from .model import Email, LooseFile


def _assign_custodian(e: Email) -> None:
    cps = e.custodian_participants()
    if e.custodian:  # forced by a scene (e.g. affair items recovered to a mailbox)
        e.other_custodians = [k for k in cps if k != e.custodian]
        return
    if not cps:
        e.custodian, e.other_custodians = "henry", []
        return
    sender_key = cast.custodian_of_email(e.sender[1])
    primary = sender_key or cps[0]
    e.custodian = primary
    e.other_custodians = [k for k in cps if k != primary]


def _make_duplicates(emails: list[Email]) -> list[Email]:
    """Physically duplicate a fraction of multi-custodian emails."""
    dups: list[Email] = []
    for e in emails:
        if e.other_custodians and random.random() < config.CROSS_CUSTODIAN_DUP_RATE:
            other = random.choice(e.other_custodians)
            d = copy.deepcopy(e)
            d.custodian = other
            all_custs = [e.custodian, *e.other_custodians]
            d.other_custodians = [k for k in all_custs if k != other]
            d.is_duplicate = True
            dups.append(d)
    return dups


def _resolve_threading(emails: list[Email]) -> None:
    by_key: dict[str, Email] = {}
    for e in emails:
        by_key.setdefault(e.key, e)
    for e in emails:
        e.message_id = message_id_for(e)
    for e in emails:
        if not e.in_reply_to_key:
            continue
        parent = by_key.get(e.in_reply_to_key)
        if not parent:
            continue
        e.in_reply_to_id = message_id_for(parent)
        # Walk the ancestry to build the full References chain.
        chain: list[str] = []
        cur: Email | None = parent
        guard = 0
        while cur is not None and guard < 50:
            chain.append(message_id_for(cur))
            cur = by_key.get(cur.in_reply_to_key) if cur.in_reply_to_key else None
            guard += 1
        e.references = " ".join(reversed(chain))


def _sort_date(unit) -> dt.datetime:
    if isinstance(unit, Email):
        return unit.date
    return unit.attachment.created


def assemble(emails: list[Email], loose: list[LooseFile]) -> list:
    """Return the ordered list of units (Emails + LooseFiles) ready to write."""
    for e in emails:
        _assign_custodian(e)
    emails = emails + _make_duplicates(emails)
    _resolve_threading(emails)
    units: list = [*emails, *loose]
    units.sort(key=_sort_date)
    return units
