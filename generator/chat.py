"""Short-message / chat data in Relativity Short Message Format (RSMF).

An ``.rsmf`` file is an RFC-822 container (so it rides through email-aware
processing) carrying an ``rsmf_manifest.json`` describing the conversation —
participants and time-ordered events — plus any shared media as MIME parts.
This is the format Relativity ingests natively as chat; on import it expands the
container into per-message items grouped under a conversation.

We also emit a flat per-message ``chat_messages.csv`` for platforms that prefer
to ingest chat as structured rows rather than RSMF.

Everything is built deterministically (fixed boundaries, message ids and JSON
ordering) so hashes are stable across rebuilds.
"""
from __future__ import annotations

import datetime as dt
import json
from dataclasses import dataclass, field
from email.message import EmailMessage
from email.utils import format_datetime

from . import attachments, cast
from .authoring import doc
from .model import Attachment, LooseFile


@dataclass
class Msg:
    ts: dt.datetime
    sender_key: str
    body: str
    system: bool = False
    media_caption: str | None = None  # if set, attach a small image to this event


@dataclass
class Conversation:
    cid: str
    name: str
    custodian: str
    participants: list[str]
    messages: list[Msg]
    hot: bool = False


def _iso(t: dt.datetime) -> str:
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def _png(caption: str, when: dt.datetime) -> bytes:
    a = Attachment(kind="png", filename="shared.png", title=caption, author_key="catherine_howard",
                   created=when, modified=when, spec=dict(style="seal", caption=caption,
                                                          subtitle="shared in chat"))
    attachments.build(a)
    return a.data


def _manifest(conv: Conversation) -> dict:
    pid = {k: str(i) for i, k in enumerate(conv.participants, start=1)}
    participants = [{"id": pid[k], "display": cast.get(k).name, "email": cast.get(k).email}
                    for k in conv.participants]
    events = []
    for j, m in enumerate(conv.messages, start=1):
        ev: dict = {"id": str(j), "timestamp": _iso(m.ts)}
        if m.system:
            ev["type"] = "system"
            ev["body"] = m.body
        else:
            ev["type"] = "message"
            ev["participant"] = pid[m.sender_key]
            ev["body"] = m.body
            if m.media_caption:
                ev["attachments"] = [{"id": f"att{j}", "display": f"shared_{j}.png"}]
        events.append(ev)
    return {"version": "1.0", "participants": participants, "events": events}


def _transcript(conv: Conversation) -> str:
    lines = [f"Conversation: {conv.name}",
             "Participants: " + ", ".join(cast.get(k).name for k in conv.participants), ""]
    for m in conv.messages:
        stamp = m.ts.strftime("%Y-%m-%d %H:%M")
        if m.system:
            lines.append(f"[{stamp}] * {m.body}")
        else:
            extra = f"  [attachment: shared image — {m.media_caption}]" if m.media_caption else ""
            lines.append(f"[{stamp}] {cast.get(m.sender_key).name}: {m.body}{extra}")
    return "\n".join(lines) + "\n"


def build_rsmf(conv: Conversation) -> tuple[bytes, str]:
    manifest = json.dumps(_manifest(conv), ensure_ascii=False, indent=2).encode("utf-8")
    sender = cast.get(conv.participants[0])
    others = [cast.get(k) for k in conv.participants[1:]]

    msg = EmailMessage()
    msg["From"] = f"{sender.name} <{sender.email}>"
    if others:
        msg["To"] = ", ".join(f"{p.name} <{p.email}>" for p in others)
    msg["Subject"] = conv.name
    msg["Date"] = format_datetime(conv.messages[-1].ts.replace(tzinfo=dt.timezone.utc))
    msg["Message-ID"] = f"<rsmf-{conv.cid}@ravenmail.tudor>"
    msg["X-RSMF-Version"] = "1.0"
    msg["MIME-Version"] = "1.0"
    n_msgs = sum(1 for m in conv.messages if not m.system)
    msg.set_content(
        "Relativity Short Message Format (RSMF) export.\n"
        f"Conversation: {conv.name}\n"
        f"Participants: {', '.join(cast.get(k).name for k in conv.participants)}\n"
        f"Messages: {n_msgs}\n")
    msg.add_attachment(manifest, maintype="application", subtype="json",
                       filename="rsmf_manifest.json")
    # Shared media referenced by the manifest.
    for j, m in enumerate(conv.messages, start=1):
        if m.media_caption:
            png = _png(m.media_caption, m.ts)
            msg.add_attachment(png, maintype="image", subtype="png", filename=f"shared_{j}.png")
    msg.set_boundary(f"----=_RSMF_{conv.cid}")
    return msg.as_bytes(), _transcript(conv)


# --- The conversations -----------------------------------------------------
def _conversations() -> list[Conversation]:
    return [
        Conversation(
            "CHT-0001", "Privy Chamber (private)", "catherine_howard",
            ["catherine_howard", "culpeper", "rochford"], hot=True,
            messages=[
                Msg(dt.datetime(1541, 8, 14, 22, 0), "rochford", "This is a private conversation.", system=True),
                Msg(dt.datetime(1541, 8, 14, 22, 2), "rochford", "All is ready for tonight. The back stair is unwatched."),
                Msg(dt.datetime(1541, 8, 14, 22, 4), "catherine_howard", "Is the King gone to hunt?"),
                Msg(dt.datetime(1541, 8, 14, 22, 5), "rochford", "At first light. He will not return before dusk."),
                Msg(dt.datetime(1541, 8, 14, 22, 9), "culpeper", "I will come when the household sleeps. Say nothing to the other ladies."),
                Msg(dt.datetime(1541, 8, 14, 22, 12), "catherine_howard", "Burn these messages after. Promise me."),
                Msg(dt.datetime(1541, 8, 14, 22, 13), "culpeper", "I promise. A token, until tonight.", media_caption="a token"),
                Msg(dt.datetime(1541, 8, 14, 22, 15), "catherine_howard", "Until tonight. Delete this."),
            ]),
        Conversation(
            "CHT-0002", "Privy Council — working group", "cromwell",
            ["cromwell", "cranmer", "rich", "henry"],
            messages=[
                Msg(dt.datetime(1535, 7, 3, 9, 0), "cromwell", "Gentlemen, the valuations are in. Glastonbury is a goldmine."),
                Msg(dt.datetime(1535, 7, 3, 9, 1), "rich", "Literally. The plate alone runs to thousands of ounces."),
                Msg(dt.datetime(1535, 7, 3, 9, 3), "cranmer", "Let us proceed carefully. The North is restless about the smaller houses."),
                Msg(dt.datetime(1535, 7, 3, 9, 5), "henry", "Proceed. And let us not lose our heads over the paperwork."),
                Msg(dt.datetime(1535, 7, 3, 9, 6), "cromwell", "Noted, Your Majesty. I will send the schedule by this afternoon."),
            ]),
        Conversation(
            "CHT-0003", "Texts with Suffolk", "henry",
            ["henry", "suffolk"],
            messages=[
                Msg(dt.datetime(1533, 6, 12, 11, 0), "suffolk", "Tiltyard at noon? Bring the new Italian armour."),
                Msg(dt.datetime(1533, 6, 12, 11, 2), "henry", "I will be there. Loser buys the wine."),
                Msg(dt.datetime(1533, 6, 12, 11, 3), "suffolk", "You always say that and never lose."),
                Msg(dt.datetime(1533, 6, 12, 11, 4), "henry", "King's privilege, Charles."),
            ]),
    ]


def build_chats() -> tuple[list[LooseFile], list[dict]]:
    """Return RSMF loose-file units and flat per-message rows for the chat CSV."""
    files: list[LooseFile] = []
    rows: list[dict] = []
    for conv in _conversations():
        data, transcript = build_rsmf(conv)
        att = doc("binary", f"{conv.cid}.rsmf", conv.name, author=conv.participants[0],
                  created=conv.messages[0].ts, modified=conv.messages[-1].ts,
                  storyline="Howard Affair" if conv.hot else "(chat)", hot=conv.hot,
                  spec={"data": data, "text": transcript})
        files.append(LooseFile(attachment=att, custodian=conv.custodian,
                               recordtype="Short Message (RSMF)"))
        for j, m in enumerate(conv.messages, start=1):
            if m.system:
                continue
            p = cast.get(m.sender_key)
            rows.append({
                "CONVERSATIONID": conv.cid,
                "CONVERSATIONNAME": conv.name,
                "CUSTODIAN": cast.get(conv.custodian).name,
                "MESSAGEID": f"{conv.cid}-{j:03d}",
                "TIMESTAMP": _iso(m.ts),
                "SENDER": p.name,
                "SENDEREMAIL": p.email,
                "BODY": m.body,
                "HASATTACHMENT": "Y" if m.media_caption else "N",
                "RSMF_NATIVE": f"{conv.cid}.rsmf",
            })
    return files, rows
