"""Global configuration for the Tudor eDiscovery dataset generator.

Every tunable knob lives here: the random seed, the date range, the target
volumes, output locations, and the Concordance load-file delimiters. The
build is fully seeded so each run reproduces identical metadata — and
identical hash values — which is exactly what makes the corpus
"corroborative" and safe to use as a stable demo asset.
"""
from __future__ import annotations

import datetime as dt
from pathlib import Path

# --- Reproducibility -------------------------------------------------------
# Fixed seed => identical files, dates and hashes on every build.
SEED = 1536  # the year of Anne Boleyn's execution; arbitrary but memorable.

# --- Time period -----------------------------------------------------------
# The corpus spans Henry VIII's "Great Matter" through to his death in 1547.
PERIOD_START = dt.date(1525, 1, 1)
PERIOD_END = dt.date(1547, 2, 28)

# --- Output locations ------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
VOLUME = "VOL001"
VOLUME_DIR = DATA_DIR / VOLUME
NATIVES_DIR = VOLUME_DIR / "NATIVES"
TEXT_DIR = VOLUME_DIR / "TEXT"
LOADFILE_DIR = VOLUME_DIR / "DATA"

# --- Bates / control numbering --------------------------------------------
BATES_PREFIX = "CROWN"
BATES_PAD = 8  # e.g. CROWN00000001

# --- Target volumes  (the "Large" profile, ~2,000 items) ------------------
# Targets only; build.py reports the exact realised counts.
TARGET_NARRATIVE_EMAILS = 340
TARGET_ROUTINE_EMAILS = 600
TARGET_NOISE_ITEMS = 760
TARGET_LOOSE_FILES = 150

# Behavioural rates.
ATTACH_RATE_NARRATIVE = 0.45   # narrative emails carrying >=1 attachment
ATTACH_RATE_ROUTINE = 0.18     # routine emails carrying >=1 attachment
CROSS_CUSTODIAN_DUP_RATE = 0.12  # multi-custodian emails physically duplicated

# --- Concordance (.dat) delimiters ----------------------------------------
# Industry-standard Concordance delimiters.
DAT_FIELD = "\x14"    # ASCII 20  ()  column separator
DAT_QUOTE = "\xfe"    # ASCII 254 (þ)  text qualifier
DAT_NEWLINE = "\xae"  # ASCII 174 (®)  in-field line break
DAT_MULTI = "; "      # multi-value separator within a field (e.g. multiple TO)


def reset_seed(extra: int = 0) -> None:
    """Re-seed both ``random`` and Faker so the build is deterministic."""
    import random

    from faker import Faker

    random.seed(SEED + extra)
    Faker.seed(SEED + extra)
