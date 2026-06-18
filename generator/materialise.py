"""Materialisation: turn assembled units into files on disk + load-file records.

Walks the ordered units, assigns sequential Bates/control numbers, builds each
native (and its extracted text), computes hashes from the real bytes, writes the
production tree, and returns one :class:`~generator.metadata.Record` per
document with all family relationships wired up.
"""
from __future__ import annotations

import copy
import hashlib
import re

from . import attachments as att_builder
from . import cast, config
from .eml_builder import build_eml
from .metadata import (
    FILETYPE_BY_EXT,
    RECORDTYPE,
    Record,
    fdate,
    ftime,
    join_addrs,
    page_count,
)
from .model import Attachment, Email, LooseFile

_SAFE = re.compile(r"[^A-Za-z0-9 _.-]+")


def _safe_name(subject: str) -> str:
    name = _SAFE.sub("", subject).strip() or "message"
    return name[:60]


def _names(keys: list[str]) -> str:
    return "; ".join(cast.get(k).name for k in keys)


def _ext_of(filename: str) -> str:
    return filename.rsplit(".", 1)[-1].lower() if "." in filename else ""


class Materialiser:
    def __init__(self) -> None:
        self.n = 0
        self.records: list[Record] = []
        self.answers: list[dict] = []

    def _answer(self, docid: str, custodian: str, category: str, subcategory: str,
                storyline: str, hot: bool, confidentiality: str, filename: str,
                subject: str, is_duplicate: bool = False) -> None:
        self.answers.append({
            "DOCID": docid,
            "CUSTODIAN": cast.get(custodian).name if custodian in cast.BY_KEY else custodian,
            "CATEGORY": category,
            "SUBCATEGORY": subcategory,
            "STORYLINE": storyline,
            "KEY_DOCUMENT": "Yes" if hot else "No",
            "CONFIDENTIALITY": confidentiality,
            "SUGGESTED_PRIVILEGE": "Yes" if "Privileged" in (confidentiality or "") else "No",
            "EXACT_DUPLICATE": "Yes" if is_duplicate else "No",
            "FILENAME": filename,
            "SUBJECT_OR_TITLE": subject,
        })

    # --- low-level helpers -------------------------------------------------
    def _next(self) -> tuple[str, int]:
        self.n += 1
        return f"{config.BATES_PREFIX}{self.n:0{config.BATES_PAD}d}", self.n

    def _write(self, docid: str, idx: int, ext: str, data: bytes, text: str) -> tuple[str, str]:
        shard = f"{(idx - 1) // 250:03d}"
        ndir = config.NATIVES_DIR / shard
        tdir = config.TEXT_DIR / shard
        ndir.mkdir(parents=True, exist_ok=True)
        tdir.mkdir(parents=True, exist_ok=True)
        (ndir / f"{docid}.{ext}").write_bytes(data)
        (tdir / f"{docid}.txt").write_text(text, encoding="utf-8")
        return f"NATIVES\\{shard}\\{docid}.{ext}", f"TEXT\\{shard}\\{docid}.txt"

    @staticmethod
    def _hashes(data: bytes) -> tuple[str, str]:
        return hashlib.md5(data).hexdigest().upper(), hashlib.sha1(data).hexdigest().upper()

    # --- record builders ---------------------------------------------------
    def _email_record(self, e: Email, docid: str, idx: int, eml_bytes: bytes, eml_text: str,
                       begatt: str, endatt: str, child_ids: list[str]) -> Record:
        md5, sha1 = self._hashes(eml_bytes)
        nlink, tlink = self._write(docid, idx, "eml", eml_bytes, eml_text)
        all_cust = sorted({e.custodian, *e.other_custodians})
        return Record(
            docid=docid, begbates=docid, endbates=docid, begattach=begatt, endattach=endatt,
            parentid="", attachmentids="; ".join(child_ids), recordtype=RECORDTYPE["email"],
            custodian=cast.get(e.custodian).name, allcustodians=_names(all_cust),
            email_from=join_addrs([e.sender]), email_to=join_addrs(e.to),
            email_cc=join_addrs(e.cc), email_bcc=join_addrs(e.bcc), subject=e.subject,
            datesent=fdate(e.date), timesent=ftime(e.date),
            datereceived=fdate(e.date), timereceived=ftime(e.date),
            datecreated=fdate(e.date), datemodified=fdate(e.date),
            author=e.sender[0], lastmodifiedby=e.sender[0],
            filename=f"{_safe_name(e.subject)}.eml", fileextension="eml",
            filetype=FILETYPE_BY_EXT["eml"], filesize=str(len(eml_bytes)),
            pagecount=str(page_count("eml", eml_text)), md5=md5, sha1=sha1,
            messageid=e.message_id, inreplyto=e.in_reply_to_id,
            threadid=e.thread_key or e.message_id, importance=e.importance,
            hasattachments="Y" if child_ids else "N", attachmentcount=str(len(child_ids)),
            nativelink=nlink, textlink=tlink,
        )

    def _attachment_record(self, a: Attachment, docid: str, idx: int, parent: Email,
                           begatt: str, endatt: str) -> Record:
        md5, sha1 = self._hashes(a.data)
        ext = _ext_of(a.filename)
        nlink, tlink = self._write(docid, idx, ext, a.data, a.text)
        all_cust = sorted({parent.custodian, *parent.other_custodians})
        return Record(
            docid=docid, begbates=docid, endbates=docid, begattach=begatt, endattach=endatt,
            parentid=parent.docid, attachmentids="", recordtype=RECORDTYPE["attachment"],
            custodian=cast.get(parent.custodian).name, allcustodians=_names(all_cust),
            subject="",
            datesent=fdate(parent.date), timesent=ftime(parent.date),  # family date
            datecreated=fdate(a.created), datemodified=fdate(a.modified),
            author=cast.get(a.author_key).name, lastmodifiedby=cast.get(a.author_key).name,
            filename=a.filename, fileextension=ext,
            filetype=FILETYPE_BY_EXT.get(ext, "Unknown"), filesize=str(len(a.data)),
            pagecount=str(page_count(a.kind, a.text)), md5=md5, sha1=sha1,
            threadid=parent.thread_key or parent.message_id,
            hasattachments="", attachmentcount="", nativelink=nlink, textlink=tlink,
        )

    def _loose_record(self, lf: LooseFile, docid: str, idx: int) -> Record:
        a = lf.attachment
        md5, sha1 = self._hashes(a.data)
        ext = _ext_of(a.filename)
        nlink, tlink = self._write(docid, idx, ext, a.data, a.text)
        all_cust = sorted({lf.custodian, *lf.other_custodians})
        return Record(
            docid=docid, begbates=docid, endbates=docid, begattach=docid, endattach=docid,
            recordtype=lf.recordtype or RECORDTYPE["loose"], custodian=cast.get(lf.custodian).name,
            allcustodians=_names(all_cust),
            datecreated=fdate(a.created), datemodified=fdate(a.modified),
            author=cast.get(a.author_key).name, lastmodifiedby=cast.get(a.author_key).name,
            filename=a.filename, fileextension=ext,
            filetype=FILETYPE_BY_EXT.get(ext, "Unknown"), filesize=str(len(a.data)),
            pagecount=str(page_count(a.kind, a.text)), md5=md5, sha1=sha1,
            hasattachments="N", attachmentcount="0", nativelink=nlink, textlink=tlink,
        )

    # --- main loop ---------------------------------------------------------
    def run(self, units: list) -> list[Record]:
        for unit in units:
            if isinstance(unit, Email):
                self._do_email(unit)
            elif isinstance(unit, LooseFile):
                self._do_loose(unit)
        return self.records

    def _do_email(self, e: Email) -> None:
        # Independent attachment objects (so shared/forwarded files get their own
        # DocIDs while keeping identical bytes), then build their natives.
        atts = [copy.deepcopy(a) for a in e.attachments]
        for a in atts:
            att_builder.build(a)
        e.attachments = atts
        eml_bytes, eml_text = build_eml(e)

        parent_docid, parent_idx = self._next()
        e.docid = parent_docid
        child_ids: list[str] = []
        child_meta: list[tuple[Attachment, str, int]] = []
        for a in atts:
            cid, cidx = self._next()
            a.docid = cid
            child_ids.append(cid)
            child_meta.append((a, cid, cidx))
        endatt = child_ids[-1] if child_ids else parent_docid

        self.records.append(self._email_record(
            e, parent_docid, parent_idx, eml_bytes, eml_text, parent_docid, endatt, child_ids))
        self._answer(parent_docid, e.custodian, e.category, e.subcategory, e.storyline,
                     e.hot, e.confidentiality, f"{_safe_name(e.subject)}.eml", e.subject,
                     e.is_duplicate)
        for a, cid, cidx in child_meta:
            self.records.append(self._attachment_record(a, cid, cidx, e, parent_docid, endatt))
            self._answer(cid, e.custodian, e.category, e.subcategory, a.storyline or e.storyline,
                         a.hot or e.hot, a.confidentiality, a.filename, a.title, e.is_duplicate)

    def _do_loose(self, lf: LooseFile) -> None:
        a = copy.deepcopy(lf.attachment)
        att_builder.build(a)
        lf.attachment = a
        docid, idx = self._next()
        a.docid = docid
        self.records.append(self._loose_record(lf, docid, idx))
        self._answer(docid, lf.custodian, "loose", a.kind, a.storyline, a.hot,
                     a.confidentiality, a.filename, a.title)


def materialise(units: list) -> tuple[list[Record], list[dict]]:
    m = Materialiser()
    m.run(units)
    return m.records, m.answers
