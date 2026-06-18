"""Storyline filler + the public ``build_narrative`` entry point.

The bespoke spine lives in :mod:`scenes`. Here we wrap that spine in a larger
body of believable, storyline-flavoured traffic — status notes, council
minutes, short replies — so each arc has realistic depth around its handful of
"gem" documents. Everything is dated within the historical window of its arc
and always involves at least one collected custodian.
"""
from __future__ import annotations

import datetime as dt
import random

from . import cast, corpora, scenes
from .authoring import compose, doc, mail, thread
from .model import Email

# --- Per-storyline configuration ------------------------------------------
# (label, subcategory, start, end, participant pool, topic bank, filler count)
_STORYLINES = [
    ("The Great Matter", "great_matter", dt.date(1527, 1, 1), dt.date(1533, 6, 30),
     ["henry", "wolsey", "cromwell", "cranmer", "more", "aragon", "chapuys", "audley", "suffolk"],
     ["the appeal to Rome", "the King's conscience", "the canon lawyers' opinions",
      "the universities' verdicts", "the Imperial ambassador's protests",
      "the drafting of the Act of Appeals", "the Queen's dower lands",
      "the oath of the clergy", "the legatine court records"], 42),
    ("Anne Boleyn", "anne_boleyn", dt.date(1533, 6, 1), dt.date(1536, 5, 30),
     ["henry", "anne_boleyn", "cromwell", "cranmer", "rich", "audley", "suffolk",
      "thomas_boleyn", "george_boleyn", "norris", "smeaton"],
     ["the coronation arrangements", "the Princess Elizabeth's household",
      "the Queen's household expenses", "the New Year's gifts",
      "the peers' summons to the Tower", "the succession oath",
      "the Queen's apartments at Greenwich"], 40),
    ("Dissolution", "dissolution", dt.date(1535, 1, 1), dt.date(1540, 6, 30),
     ["henry", "cromwell", "rich", "cranmer", "gardiner", "audley"],
     ["the survey of {abbey}", "the plate and ornaments of {abbey}",
      "the lead and bells of {abbey}", "the pensions of the religious",
      "the sale of abbey lands", "the Court of Augmentations accounts",
      "the surrender of {abbey}", "the disposal of {abbey}'s library"], 44),
    ("Cleves", "cleves", dt.date(1539, 6, 1), dt.date(1540, 7, 31),
     ["henry", "cromwell", "cranmer", "anne_cleves", "gardiner"],
     ["the Cleves alliance", "the lady's reception at Greenwich", "the German envoys",
      "the marriage treaty", "the annulment terms", "the lady's English household"], 26),
    ("Howard Affair", "howard_affair", dt.date(1540, 7, 28), dt.date(1542, 2, 13),
     ["henry", "catherine_howard", "cranmer", "rich", "gardiner", "rochford", "dereham"],
     ["the progress to the North", "the Queen's household accounts",
      "the bedchamber appointments", "the Queen's jewels and plate",
      "the secretary's appointment", "the New Year's revels"], 34),
    ("Succession", "succession", dt.date(1543, 7, 1), dt.date(1547, 1, 31),
     ["henry", "catherine_parr", "cranmer", "gardiner", "mary", "seymour_edward", "rich"],
     ["the Prince's household", "the children's tutors", "the regency council",
      "the King's physicians' reports", "the New Year's gifts",
      "the French war accounts", "the Queen's regency during the campaign"], 34),
]

_SUBJECT_TMPL = [
    "{topic} — for your consideration", "Note on {topic}", "Concerning {topic}",
    "{topic}: an update", "{topic} — action required", "Minutes touching {topic}",
    "A word about {topic}", "{topic} (further to our last)", "Query on {topic}",
]

_BODY_TMPL = [
    "I have given {topic} my closest attention and counsel that we proceed with care.",
    "The council sat this morning touching {topic}. Opinions were divided, but the King's "
    "will carried the day.",
    "Pray send me your mind on {topic} before the next sitting; I would not act without it.",
    "The matter of {topic} grows pressing and cannot be left to lie much longer.",
    "I enclose my notes on {topic} for the record, such as they are.",
    "Further to {topic}: the arrangements are in hand and I will report again within the week.",
    "I am not wholly easy about {topic}, and would value a quiet word before we commit anything "
    "to writing.",
    "All is in order regarding {topic}. There is nothing further that need trouble you for now.",
]

_SHORT_REPLIES = [
    "Noted, with thanks.", "Agreed. Proceed.", "See me before the council sits.",
    "Very well. Keep me informed.", "Approved. — H.R.", "Understood. It shall be done.",
    "I concur. Let us not lose our heads over it.", "Leave it with me.",
    "Good. Say nothing of this for now.", "Received and read.",
]


def _topic(bank: list[str]) -> str:
    t = random.choice(bank)
    if "{abbey}" in t:
        t = t.replace("{abbey}", random.choice(corpora.MONASTERIES))
    return t


def _active(pool: list[str], day: dt.date) -> list[str]:
    return [k for k in pool if cast.get(k).active_on(day)]


def _pick_parties(pool: list[str], day: dt.date) -> tuple[str, list[str]]:
    """Choose a sender and recipients, guaranteeing >=1 custodian is on the email."""
    active = _active(pool, day)
    if len(active) < 2:
        active = _active([p.key for p in cast.CUSTODIANS], day) or ["henry"]
    sender = random.choice(active)
    others = [k for k in active if k != sender]
    n = min(random.choice([1, 1, 1, 2, 2, 3]), len(others))
    recips = random.sample(others, n) if others else []
    parties = [sender, *recips]
    if not any(cast.get(k).is_custodian for k in parties):
        # Henry is always active, so there is always an active custodian to add.
        custs = [p.key for p in cast.CUSTODIANS if p.active_on(day)] or ["henry"]
        extra = random.choice(custs)
        recips = [r for r in recips if r != sender]
        if extra != sender and extra not in recips:
            recips.append(extra)
    return sender, recips


def _rand_dt(start: dt.date, end: dt.date) -> dt.datetime:
    span = (end - start).days
    day = start + dt.timedelta(days=random.randint(0, max(span, 1)))
    return dt.datetime(day.year, day.month, day.day,
                       random.randint(6, 21), random.choice([0, 5, 12, 15, 20, 30, 45]))


def _filler_email(label: str, subcat: str, topic: str, when: dt.datetime,
                  sender: str, recips: list[str]) -> Email:
    subject = random.choice(_SUBJECT_TMPL).format(topic=topic)
    paras = [random.choice(_BODY_TMPL).format(topic=topic)]
    if random.random() < 0.30:
        paras.append(random.choice(corpora.BEHEADING_QUIPS))
    signer = cast.get(sender).name.split()[-1]
    body = compose(random.choice(corpora.SALUTATIONS), paras,
                   random.choice(corpora.SIGN_OFFS), cast.get(sender).name,
                   footer=random.choice(corpora.EMAIL_FOOTERS))
    e = mail("nar", when, sender, to=recips, subject=subject, body=body,
             category="narrative", subcategory=subcat, storyline=label,
             importance=random.choice(["Normal", "Normal", "Normal", "High"]),
             confidentiality=random.choice(["", "", "", "Confidential", "Internal - Privy Council"]))
    # ~18% carry a simple attachment, forming a family.
    if random.random() < 0.18:
        created = when - dt.timedelta(days=random.randint(0, 3))
        if random.random() < 0.5:
            att = doc("docx", f"Notes_{subcat}_{e.key}.docx", f"Notes on {topic}",
                      author=sender, created=created, modified=when, storyline=label,
                      spec=dict(paragraphs=[
                          f"Memorandum touching {topic}.",
                          random.choice(_BODY_TMPL).format(topic=topic),
                          "For discussion at the next sitting of the council."]))
        else:
            rows = [[f"Item {i+1}", random.choice(corpora.COUNCIL_TOPICS).title(),
                     corpora.pounds(random.randint(40, 9000))] for i in range(random.randint(3, 7))]
            att = doc("xlsx", f"Schedule_{subcat}_{e.key}.xlsx", f"Schedule — {topic}",
                      author=sender, created=created, modified=when, storyline=label,
                      spec=dict(sheet="Schedule", headers=["Item", "Matter", "Sum"], rows=rows))
        e.attachments.append(att)
    return e


def _storyline_filler(label, subcat, start, end, pool, topics, count) -> list[Email]:
    out: list[Email] = []
    i = 0
    while i < count:
        when = _rand_dt(start, end)
        sender, recips = _pick_parties(pool, when.date())
        if not recips:
            continue
        topic = _topic(topics)
        e = _filler_email(label, subcat, topic, when, sender, recips)
        out.append(e)
        i += 1
        # ~30% spawn a short threaded reply the next day.
        if random.random() < 0.30 and recips:
            replier = recips[0]
            r_when = when + dt.timedelta(days=random.randint(0, 2), hours=random.randint(1, 8))
            # CC the rest of the original recipients so the thread (and any
            # custodian on it) stays intact.
            re_subj = e.subject if e.subject.lower().startswith("re:") else "Re: " + e.subject
            reply = mail("nar", r_when, replier, to=[sender],
                         cc=[r for r in recips if r != replier],
                         subject=re_subj,
                         body=random.choice(_SHORT_REPLIES) + "\n", category="narrative",
                         subcategory=subcat, storyline=label)
            thread([e, reply], f"{subcat}-filler-{e.key}")
            out.append(reply)
            i += 1
    return out


def build_narrative() -> list[Email]:
    """The full narrative corpus: bespoke spine + storyline filler."""
    out: list[Email] = list(scenes.all_scenes())
    for (label, subcat, start, end, pool, topics, count) in _STORYLINES:
        out += _storyline_filler(label, subcat, start, end, pool, topics, count)
    return out
