"""Load-file writers: Concordance ``.dat`` and a universal CSV mirror.

The DAT uses the industry-standard Concordance delimiters — field = ASCII 20,
text-qualifier = þ (254), in-field newline = ® (174) — written as UTF-8 so every
accent, em-dash and currency symbol in the data survives intact (the modern
convention all major review platforms accept). The CSV is plain RFC-4180 for
anything that would rather take a spreadsheet.
"""
from __future__ import annotations

import csv
from pathlib import Path

from . import config
from .metadata import FIELDS, Record

_STRIP = (config.DAT_QUOTE, config.DAT_FIELD, config.DAT_NEWLINE)


def _clean(value: str) -> str:
    """Remove stray delimiter characters and collapse newlines."""
    v = value.replace("\r\n", " ").replace("\r", " ").replace("\n", " ")
    for ch in _STRIP:
        v = v.replace(ch, " ")
    return v


def _row(record: Record) -> list[str]:
    return [getattr(record, attr) for _, attr in FIELDS]


def write_dat(records: list[Record], path: Path) -> None:
    q, fld, nl = config.DAT_QUOTE, config.DAT_FIELD, "\r\n"
    headers = [h for h, _ in FIELDS]
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        f.write(fld.join(f"{q}{h}{q}" for h in headers) + nl)
        for r in records:
            cells = (f"{q}{_clean(v)}{q}" for v in _row(r))
            f.write(fld.join(cells) + nl)


def write_csv(records: list[Record], path: Path) -> None:
    headers = [h for h, _ in FIELDS]
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        w.writerow(headers)
        for r in records:
            w.writerow(_row(r))
