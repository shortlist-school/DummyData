"""Loose files — standalone documents collected from custodian file-shares.

These have no parent email (they are "family-of-one" e-docs) and broaden the
document-type mix: ledgers, draft proclamations, meeting notes, inventories,
personal logs and the like. A handful are generated as near-duplicate draft
pairs (v1/v2) to give near-dedupe analytics something to find.
"""
from __future__ import annotations

import datetime as dt
import random

from . import cast, config, corpora
from .authoring import doc
from .model import Attachment, LooseFile


def _date_in_window(person_key: str) -> dt.datetime:
    p = cast.get(person_key)
    start = max(p.active_from or config.PERIOD_START, config.PERIOD_START)
    end = min(p.active_to or config.PERIOD_END, config.PERIOD_END)
    if end <= start:
        start, end = config.PERIOD_START, config.PERIOD_END
    span = (end - start).days
    day = start + dt.timedelta(days=random.randint(0, max(span, 1)))
    return dt.datetime(day.year, day.month, day.day, random.randint(7, 19), random.choice([0, 15, 30, 45]))


def _ledger(owner: str, when: dt.datetime, tag: str) -> Attachment:
    q = random.choice(["Michaelmas", "Lady Day", "Midsummer", "Christmas"])
    rows = [[random.choice(["Wages", "Diets", "Stable", "Wardrobe", "Alms", "Works", "Wine", "Spices"]),
             corpora.pounds(random.randint(10, 1800)), random.choice(["Paid", "Owing", "Part-paid"])]
            for _ in range(random.randint(5, 10))]
    return doc("xlsx", f"Treasury_Ledger_{when.year}_{q}_{tag}.xlsx",
               f"Treasury Ledger — {q} {when.year}", author=owner, created=when, modified=when,
               storyline="(loose)", confidentiality=random.choice(["", "Confidential"]),
               spec=dict(sheet="Ledger", headers=["Head of Charge", "Sum", "Status"], rows=rows,
                         note="Working ledger. Not yet audited."))


def _proclamation(owner: str, when: dt.datetime, tag: str) -> Attachment:
    topic = random.choice(corpora.COUNCIL_TOPICS)
    return doc("docx", f"Draft_Proclamation_{tag}.docx", f"Draft Proclamation touching {topic}",
               author=owner, created=when, modified=when, storyline="(loose)",
               confidentiality=random.choice(["", "Internal - Privy Council"]),
               spec=dict(paragraphs=[
                   "By the King our Sovereign Lord, and the advice of his Council:",
                   f"Whereas divers matters touching {topic} require ordering, be it proclaimed "
                   "throughout the realm that the following shall be observed by all subjects.",
                   "DRAFT — not for issue. Subject to the King's pleasure and the Council's review."]))


def _meeting_notes(owner: str, when: dt.datetime, tag: str) -> Attachment:
    topics = random.sample(corpora.COUNCIL_TOPICS, 3)
    return doc("docx", f"Council_Notes_{when.strftime('%Y%m%d')}_{tag}.docx",
               f"Privy Council Notes — {when.strftime('%d %B %Y')}", author=owner,
               created=when, modified=when, storyline="(loose)", confidentiality="Internal - Privy Council",
               spec=dict(paragraphs=[
                   f"Present: a quorum of the Council. Chaired by {cast.get(owner).name}.",
                   "Matters discussed:",
                   *[f"  - {t}: noted and referred for action." for t in topics],
                   "No other business. The Council rose at the eleventh hour."]))


def _inventory(owner: str, when: dt.datetime, tag: str) -> Attachment:
    rows = [[random.choice(["Gold cup", "Silver salt", "Tapestry", "Ruby ring", "Book of Hours",
                            "Gilt basin", "Velvet gown", "Astrolabe"]),
             random.randint(1, 6), corpora.pounds(random.randint(5, 900))]
            for _ in range(random.randint(6, 12))]
    return doc("xlsx", f"Inventory_JewelHouse_{tag}.xlsx", "Inventory of the Jewel House",
               author=owner, created=when, modified=when, storyline="(loose)", confidentiality="Confidential",
               spec=dict(sheet="Inventory", headers=["Item", "Count", "Valuation"], rows=rows))


def _personal(owner: str, when: dt.datetime, tag: str) -> Attachment:
    kind, title, text = random.choice([
        ("txt", "Hunting Log",
         "A private record of the chase.\n\nWindsor: two harts and a fine boar. The grey gelding "
         "is lame again — see the marshal.\nGreenwich: poor sport, much rain. Supped well "
         "regardless.\nHampton: a long day. The leg pains me. Resolved to ride less and dine more."),
        ("txt", "Reading List",
         "Books to be sent for:\n - Erasmus, on the education of a prince\n - The Psalms, in the "
         "new English\n - A herbal, for the still-room\n - Something light for the long evenings\n\n"
         "Note: lend nothing to the council; it never comes back."),
        ("docx", "Personal Memorandum",
         "A note to myself, to be kept private.\n\nTrust the work, not the whispers. Keep my own "
         "counsel. Write less, remember more. And keep my head about me — figuratively, one hopes."),
    ])
    if kind == "txt":
        return doc("txt", f"{title.replace(' ', '_')}_{tag}.txt", title, author=owner,
                   created=when, modified=when, storyline="(loose)", spec=dict(text=text))
    return doc("docx", f"{title.replace(' ', '_')}_{tag}.docx", title, author=owner,
               created=when, modified=when, storyline="(loose)",
               spec=dict(paragraphs=text.split("\n\n")))


def _survey(owner: str, when: dt.datetime, tag: str) -> Attachment:
    palace = random.choice(corpora.PALACES)
    return doc("pdf", f"Survey_{tag}.pdf", f"Survey of {palace}", author=owner,
               created=when, modified=when, storyline="(loose)",
               spec=dict(paragraphs=[
                   f"A survey of the fabric and furnishings of {palace}.",
                   "The roof of the great hall wants attention before winter. The kitchens are "
                   "sound. The moat requires dredging.",
                   "Estimated cost of necessary works appended."],
                   table={"headers": ["Works", "Estimate (£)"],
                          "rows": [["Roof", "120"], ["Drainage", "60"], ["Glazing", "45"]]}))


_SITTERS = ["a Lady of the Court", "a Gentleman of the Privy Chamber", "an Unknown Nobleman",
            "a Young Princess", "a Court Musician", "an Ambassador", "a Cardinal",
            "a Merchant of London", "a Lady-in-Waiting"]


def _portrait(owner: str, when: dt.datetime, tag: str) -> Attachment:
    sitter = random.choice(_SITTERS)
    return doc("png", f"Portrait_{tag}.png", f"Portrait of {sitter}", author=owner,
               created=when, modified=when, storyline="(loose)",
               spec=dict(style="portrait", caption=sitter, subtitle="oil on panel"))


def _seal(owner: str, when: dt.datetime, tag: str) -> Attachment:
    which = random.choice(["the Great Seal of the Realm", "the Privy Seal", "a Signet Impression"])
    return doc("png", f"Seal_{tag}.png", f"Impression of {which}", author=owner,
               created=when, modified=when, storyline="(loose)",
               spec=dict(style="seal", caption=which, subtitle="wax impression"))


def _plan(owner: str, when: dt.datetime, tag: str) -> Attachment:
    palace = random.choice(corpora.PALACES)
    rooms = random.sample(["Great Hall", "Presence Chamber", "Privy Chamber", "Chapel Royal",
                           "Kitchens", "Long Gallery", "Tiltyard", "Stables", "Wardrobe",
                           "Watergate", "Council Chamber", "Library"], 6)
    return doc("png", f"Plan_{tag}.png", f"Plan of {palace}", author=owner,
               created=when, modified=when, storyline="(loose)",
               spec=dict(style="parchment", caption=f"Plan of {palace}",
                         lines=[f"{i + 1}. {r}" for i, r in enumerate(rooms)]))


# (builder, weight) — images carry enough weight to land ~30 in a 150-file set.
_BUILDERS = [
    (_ledger, 3), (_proclamation, 3), (_meeting_notes, 3), (_inventory, 2),
    (_personal, 2), (_survey, 2), (_portrait, 2), (_seal, 1), (_plan, 2),
]
_BUILDER_FNS = [b for b, _ in _BUILDERS]
_BUILDER_WTS = [w for _, w in _BUILDERS]


def build_loose(count: int) -> list[LooseFile]:
    out: list[LooseFile] = []
    custodian_keys = [p.key for p in cast.CUSTODIANS]
    for i in range(count):
        owner = random.choice(custodian_keys)
        when = _date_in_window(owner)
        builder = random.choices(_BUILDER_FNS, weights=_BUILDER_WTS, k=1)[0]
        att = builder(owner, when, f"{owner}{i:03d}")
        lf = LooseFile(attachment=att, custodian=owner)
        out.append(lf)
        # ~12% spawn a near-duplicate "version 2" with a tiny change (analytics demo).
        if random.random() < 0.12:
            when2 = when + dt.timedelta(days=random.randint(1, 20))
            att2 = builder(owner, when2, f"{owner}{i:03d}v2")
            # Nudge the title/filename to mark it a later draft of the same document.
            att2.title = att.title + " (rev. 2)"
            att2.filename = att.filename.rsplit(".", 1)[0] + "_rev2." + att.filename.rsplit(".", 1)[1]
            out.append(LooseFile(attachment=att2, custodian=owner))
    return out
