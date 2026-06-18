"""Build real, parseable ``.eml`` (RFC-822) messages from Email objects.

The output is standards-compliant MIME that any review platform ingests:
proper ``From/To/Cc/Date/Subject`` headers, ``Message-ID`` plus
``In-Reply-To``/``References`` for threading, priority/sensitivity headers, and
base64 MIME parts for attachments. Boundaries are derived from the message key
so the bytes — and therefore the hash values — are stable across builds.
"""
from __future__ import annotations

import datetime as dt
import re
from email.message import EmailMessage
from email.utils import format_datetime

from .model import Email, render_addr, render_addrs

_MIME_BY_EXT = {
    "docx": ("application", "vnd.openxmlformats-officedocument.wordprocessingml.document"),
    "xlsx": ("application", "vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
    "pdf": ("application", "pdf"),
    "png": ("image", "png"),
    "txt": ("text", "plain"),
    "ics": ("text", "calendar"),
    "wav": ("audio", "x-wav"),
    "mp3": ("audio", "mpeg"),
    "json": ("application", "json"),
}


def _mime_for(filename: str) -> tuple[str, str]:
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return _MIME_BY_EXT.get(ext, ("application", "octet-stream"))

_PRIORITY = {"High": ("1", "High"), "Low": ("5", "Low"), "Normal": (None, "Normal")}
_RE_PREFIX = re.compile(r"^(re|fw|fwd):\s*", re.IGNORECASE)


def domain_of(email_addr: str) -> str:
    return email_addr.split("@")[-1]


def message_id_for(email: Email) -> str:
    return f"<{email.key}@{domain_of(email.sender[1])}>"


def base_subject(subject: str) -> str:
    s = subject
    while _RE_PREFIX.match(s):
        s = _RE_PREFIX.sub("", s, count=1)
    return s.strip()


def build_eml(email: Email) -> tuple[bytes, str]:
    """Return ``(raw_bytes, extracted_text)`` for a single email."""
    msg = EmailMessage()
    msg["From"] = render_addr(email.sender)
    if email.to:
        msg["To"] = render_addrs(email.to)
    if email.cc:
        msg["Cc"] = render_addrs(email.cc)
    if email.bcc:
        msg["Bcc"] = render_addrs(email.bcc)
    msg["Subject"] = email.subject
    msg["Date"] = format_datetime(email.date.replace(tzinfo=dt.timezone.utc))
    msg["Message-ID"] = email.message_id or message_id_for(email)
    if email.in_reply_to_id:
        msg["In-Reply-To"] = email.in_reply_to_id
    if email.references:
        msg["References"] = email.references
    msg["Thread-Topic"] = base_subject(email.subject)
    msg["MIME-Version"] = "1.0"

    prio_code, prio_label = _PRIORITY.get(email.importance, (None, "Normal"))
    if prio_code:
        msg["X-Priority"] = prio_code
    msg["Importance"] = prio_label
    if email.confidentiality:
        msg["Sensitivity"] = "Company-Confidential"
    msg["X-Mailer"] = "RoyalPost Courier 1.0"

    body = email.body
    msg.set_content(body)

    for att in email.attachments:
        maintype, subtype = _mime_for(att.filename)
        msg.add_attachment(att.data, maintype=maintype, subtype=subtype, filename=att.filename)

    if email.attachments:
        # Deterministic boundary keeps multipart bytes stable.
        msg.set_boundary(f"----=_TudorPost_{email.key}")

    return msg.as_bytes(), _extract_text(email)


def _extract_text(email: Email) -> str:
    lines = [f"From: {render_addr(email.sender)}"]
    if email.to:
        lines.append(f"To: {render_addrs(email.to)}")
    if email.cc:
        lines.append(f"Cc: {render_addrs(email.cc)}")
    lines.append(f"Sent: {email.date.strftime('%A, %d %B %Y %I:%M %p')}")
    lines.append(f"Subject: {email.subject}")
    if email.attachments:
        lines.append("Attachments: " + "; ".join(a.filename for a in email.attachments))
    lines.append("")
    lines.append(email.body)
    return "\n".join(lines)
