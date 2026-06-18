"""Audio voice-note generation for the transcription demo.

Produces a real (robotic, espeak-ng) ``.wav`` voice memo and carries it as an
email attachment. The audio has no extractable text — it must be transcribed —
so it makes a self-contained transcription exercise. The ground-truth transcript
is exposed for the instructor key.

If espeak-ng is not installed, audio generation is skipped gracefully (the
committed corpus already contains the rendered file).
"""
from __future__ import annotations

import datetime as dt
import shutil
import subprocess
import tempfile
from pathlib import Path

from .authoring import doc, mail
from .model import Email

_ESPEAK = shutil.which("espeak-ng") or shutil.which("espeak")

# The spoken content == the ground-truth transcript (client-safe: it concerns
# secret meetings and destroying records, nothing graphic).
VOICE_NOTE_TRANSCRIPT = (
    "Your Majesty. When the King rides out to hunt on Thursday, come to the privy "
    "stair after the household sleeps. Lady Rochford will keep the door. Tell no one, "
    "and let no record of this remain. Listen to this once, and then destroy it."
)

# filename -> transcript, written to docs/TRANSCRIPTS.md by the build.
TRANSCRIPTS: dict[str, str] = {"voice_memo_Thursday.wav": VOICE_NOTE_TRANSCRIPT}


def audio_available() -> bool:
    return _ESPEAK is not None


def _tts(text: str, *, speed: int = 145, pitch: int = 40, voice: str = "en") -> bytes:
    with tempfile.TemporaryDirectory() as d:
        out = Path(d) / "v.wav"
        subprocess.run([_ESPEAK, "-v", voice, "-s", str(speed), "-p", str(pitch),
                        "-w", str(out), text], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return out.read_bytes()


def build_voice_note_emails() -> list[Email]:
    """The affair, in audio form: a voice memo from Culpeper to the Queen."""
    if not audio_available():
        return []
    wav = _tts(VOICE_NOTE_TRANSCRIPT)
    att = doc("binary", "voice_memo_Thursday.wav", "Voice Memo (Thursday)",
              author="culpeper",
              created=dt.datetime(1541, 5, 2, 21, 30), modified=dt.datetime(1541, 5, 2, 21, 30),
              storyline="Howard Affair", hot=True,
              spec={"data": wav,
                    "text": "[Audio recording, approx. 0:18. No text extracted — "
                            "requires transcription.]"})
    e = mail("hwd", dt.datetime(1541, 5, 2, 21, 35),
             ("culpeper", "t.culpeper@ravenmail.tudor"),
             to=[("catherine_howard", "kitty.h@ravenmail.tudor")],
             subject="(no subject)", category="narrative", subcategory="howard_affair",
             storyline="Howard Affair", hot=True, custodian="catherine_howard",
             attachments=[att],
             body="A voice note for you. Listen alone, then delete it. — T.\n")
    return [e]
