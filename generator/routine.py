"""Routine court administration — the everyday background traffic.

Not tied to any one storyline: jousts and revels, barge repairs and building
works, taxes and supplies, diplomacy and household payments. This is the bulk
of any real mailbox — mostly mundane, occasionally carrying an invoice or work
order, and exactly the kind of low-relevance material a reviewer must wade
through to reach the interesting documents.
"""
from __future__ import annotations

import datetime as dt
import random

from . import cast, config, corpora
from .authoring import compose, doc, mail, thread
from .model import Email

_COUNTIES = ["Kent", "Yorkshire", "Essex", "Norfolk", "Devon", "Somerset",
             "Surrey", "Sussex", "Lincolnshire", "Hampshire"]

_TOPICS = [
    "the royal barge repairs", "the Christmas revels", "the tiltyard schedule",
    "the New Year's gift roll", "the subsidy assessment for {county}",
    "the victualling of the fleet", "the progress to {palace}", "the wardrobe accounts",
    "the falconry mews", "the ordnance survey", "the wine shipment from Gascony",
    "the masque costumes", "the royal stables accounts", "the works at {palace}",
    "the muster of able men in {county}", "the repair of the great clock",
    "the Garter ceremony arrangements", "the embassy to France",
    "the purveyance of venison", "the kitchen accounts for the quarter",
]

# Participant pool: everyone except purely automated mailboxes.
_POOL = [p.key for p in (cast.CUSTODIANS + cast.PARTICIPANTS)]

_SHAPES = {
    "request": [
        "I pray Your favour and approval for {topic}; the matter waits only on your word.",
        "May I have leave to proceed with {topic}? The cost is modest and the need real.",
        "I write to request a decision on {topic} before the quarter-day.",
    ],
    "approval": [
        "Approved. Proceed with {topic} and render account when it is done.",
        "You have my leave for {topic}. Keep the expense within reason.",
        "Granted. See that {topic} is handled without fuss.",
    ],
    "report": [
        "For your information, {topic} is now complete and within estimate.",
        "I report that {topic} proceeds well and will be finished by month's end.",
        "A brief note on {topic}: all is in hand and nothing further is required of you.",
    ],
    "logistics": [
        "Arrangements for {topic} are as follows: carts at dawn, the household to follow, "
        "and the heavy plate to go by water.",
        "Touching {topic}, I have engaged the usual tradesmen and set the dates. Details to "
        "follow under separate cover.",
        "The plan for {topic} is settled. Pray confirm you are content and I will give the word.",
    ],
    "concern": [
        "I must raise a concern about {topic}; the costs have run ahead of the estimate and I "
        "would not commit further without your knowledge.",
        "There is a difficulty with {topic} that I think you should hear of before it grows.",
        "I am uneasy about {topic} and would welcome a quiet word at your convenience.",
    ],
}


def _fill(topic_tmpl: str) -> str:
    return (topic_tmpl
            .replace("{county}", random.choice(_COUNTIES))
            .replace("{palace}", random.choice(corpora.PALACES)))


def _active(day: dt.date) -> list[str]:
    return [k for k in _POOL if cast.get(k).active_on(day)]


def _parties(day: dt.date) -> tuple[str, list[str]]:
    active = _active(day) or ["henry"]
    sender = random.choice(active)
    others = [k for k in active if k != sender]
    n = min(random.choice([1, 1, 1, 2, 2]), len(others))
    recips = random.sample(others, n) if others else []
    if not any(cast.get(k).is_custodian for k in [sender, *recips]):
        custs = [p.key for p in cast.CUSTODIANS if p.active_on(day)] or ["henry"]
        extra = random.choice(custs)
        recips = [r for r in recips if r != sender]
        if extra != sender and extra not in recips:
            recips.append(extra)
    return sender, recips


def _rand_dt() -> dt.datetime:
    span = (config.PERIOD_END - config.PERIOD_START).days
    day = config.PERIOD_START + dt.timedelta(days=random.randint(0, span))
    return dt.datetime(day.year, day.month, day.day,
                       random.randint(6, 20), random.choice([0, 5, 10, 15, 25, 40, 50]))


def _attachment_for(topic: str, sender: str, when: dt.datetime, key: str) -> doc:
    created = when - dt.timedelta(days=random.randint(0, 4))
    roll = random.random()
    if roll < 0.4:
        rows = [[random.choice(["Timber", "Lead", "Wax", "Cloth of gold", "Wine (tun)",
                                "Wages", "Cartage", "Candles"]),
                 random.randint(1, 40), corpora.pounds(random.randint(2, 600))]
                for _ in range(random.randint(3, 8))]
        return doc("xlsx", f"Invoice_{key}.xlsx", f"Account — {topic}", author=sender,
                   created=created, modified=when, storyline="(routine)",
                   spec=dict(sheet="Account", headers=["Item", "Qty", "Cost"], rows=rows,
                             note="Submitted to the Office of the Treasurer."))
    if roll < 0.75:
        return doc("docx", f"WorkOrder_{key}.docx", f"Work Order — {topic}", author=sender,
                   created=created, modified=when, storyline="(routine)",
                   spec=dict(paragraphs=[
                       f"Work order touching {topic}.",
                       "The undersigned authorises the works described, to be completed with "
                       "due economy and accounted for upon completion.",
                       f"Authorised by {cast.get(sender).name}."]))
    return doc("pdf", f"Report_{key}.pdf", f"Report — {topic}", author=sender,
               created=created, modified=when, storyline="(routine)",
               spec=dict(paragraphs=[
                   f"This report concerns {topic}.",
                   "The matter has been attended to as instructed. No further action is "
                   "required at this time.", "Submitted for the record."]))


def build_routine(count: int) -> list[Email]:
    out: list[Email] = []
    i = 0
    while i < count:
        when = _rand_dt()
        sender, recips = _parties(when.date())
        if not recips:
            continue
        topic = _fill(random.choice(_TOPICS))
        shape = random.choices(list(_SHAPES), weights=[24, 14, 26, 18, 18], k=1)[0]
        paras = [random.choice(_SHAPES[shape]).format(topic=topic)]
        if random.random() < 0.18:
            paras.append(random.choice(corpora.BEHEADING_QUIPS))
        subject = random.choice([
            f"{topic.capitalize()}", f"Re: {topic}", f"{topic.capitalize()} — for approval",
            f"Note: {topic}", f"{topic.capitalize()} (quarterly)",
        ])
        body = compose(random.choice(corpora.SALUTATIONS), paras,
                       random.choice(corpora.SIGN_OFFS), cast.get(sender).name,
                       footer=random.choice(corpora.EMAIL_FOOTERS))
        e = mail("rtn", when, sender, to=recips, subject=subject, body=body,
                 category="routine", subcategory=shape, storyline="(routine)",
                 importance=random.choice(["Normal", "Normal", "Normal", "Normal", "High", "Low"]),
                 confidentiality=random.choice(["", "", "", "", "Confidential"]))
        if random.random() < config.ATTACH_RATE_ROUTINE:
            e.attachments.append(_attachment_for(topic, sender, when, e.key))
        out.append(e)
        i += 1
        # ~28% get a short approval/ack reply, forming a thread.
        if random.random() < 0.28 and recips:
            replier = recips[0]
            r_when = when + dt.timedelta(days=random.randint(0, 3), hours=random.randint(1, 9))
            reply_body = random.choice(_SHAPES["approval"]).format(topic=topic)
            re_subj = subject if subject.lower().startswith("re:") else "Re: " + subject
            reply = mail("rtn", r_when, replier, to=[sender],
                         cc=[r for r in recips if r != replier],
                         subject=re_subj,
                         body=compose("", [reply_body], "—", cast.get(replier).name),
                         category="routine", subcategory="approval", storyline="(routine)")
            thread([e, reply], f"rtn-{e.key}")
            out.append(reply)
            i += 1
    return out
