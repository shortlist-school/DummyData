"""Build orchestrator.

Run as ``python -m generator.build`` to (re)generate the entire corpus:
generate every content stream, assemble families/threads/custodians,
materialise natives + extracted text, and write the Concordance/CSV load files,
the demo answer key and a build manifest.

Volumes are seeded, so a given set of counts always reproduces byte-for-byte.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import shutil
import sys
from collections import Counter

from . import assemble as assembler
from . import chat, config, loadfiles, materialise, media, narrative, noise, routine
from . import loose as loose_mod


def _humansize(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} GB"


def write_answer_key(answers: list[dict], path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(answers[0].keys())
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(answers)


def main() -> None:
    # Pin hash randomisation so set/dict ordering (and therefore some library
    # output, notably openpyxl's xlsx bytes) is identical on every build. We
    # must re-exec because PYTHONHASHSEED can only be set before interpreter
    # start. The build is always invoked as ``python -m generator.build``.
    if os.environ.get("PYTHONHASHSEED") != "0":
        os.environ["PYTHONHASHSEED"] = "0"
        os.execve(sys.executable,
                  [sys.executable, "-m", "generator.build", *sys.argv[1:]], os.environ)

    ap = argparse.ArgumentParser(description="Generate the Tudor eDiscovery corpus.")
    ap.add_argument("--routine", type=int, default=config.TARGET_ROUTINE_EMAILS)
    ap.add_argument("--noise", type=int, default=config.TARGET_NOISE_ITEMS)
    ap.add_argument("--loose", type=int, default=config.TARGET_LOOSE_FILES)
    args = ap.parse_args()

    print("Tudor eDiscovery corpus — build starting")
    print(f"  seed={config.SEED}  period={config.PERIOD_START}..{config.PERIOD_END}")
    config.reset_seed()

    # 1. Generate every content stream (order is fixed => deterministic).
    print("  generating narrative ...")
    emails = narrative.build_narrative()
    print(f"    narrative emails: {len(emails)}")
    print("  generating audio voice note ...")
    if media.audio_available():
        emails += media.build_voice_note_emails()
    else:
        print("    (espeak-ng not found — skipping audio; install it to regenerate)")
    print("  generating routine traffic ...")
    emails += routine.build_routine(args.routine)
    print("  generating noise ...")
    emails += noise.build_noise(args.noise)
    print("  generating loose files ...")
    loose_files = loose_mod.build_loose(args.loose)
    print("  generating chat / RSMF data ...")
    chat_files, chat_rows = chat.build_chats()
    loose_files += chat_files

    # 2. Assemble: custodians, duplicates, threading, chronological order.
    print("  assembling families, duplicates and threads ...")
    units = assembler.assemble(emails, loose_files)

    # 3. Fresh output tree.
    shutil.rmtree(config.DATA_DIR, ignore_errors=True)

    # 4. Materialise natives + text + records.
    print("  materialising natives, text and metadata ...")
    records, answers = materialise.materialise(units)

    # 5. Load files.
    config.LOADFILE_DIR.mkdir(parents=True, exist_ok=True)
    loadfiles.write_dat(records, config.LOADFILE_DIR / "loadfile.dat")
    loadfiles.write_csv(records, config.LOADFILE_DIR / "loadfile.csv")

    # 5b. Supplementary chat (per-message) load file.
    if chat_rows:
        with open(config.LOADFILE_DIR / "chat_messages.csv", "w",
                  encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(chat_rows[0].keys()))
            w.writeheader()
            w.writerows(chat_rows)

    # 6. Answer key (demo aid, kept out of the load file).
    write_answer_key(answers, config.ROOT / "docs" / "ANSWER_KEY.csv")

    # 6b. Ground-truth transcripts for the audio (instructor aid).
    audio = [r for r in records if r.fileextension in ("wav", "mp3")]
    if audio:
        lines = ["# Audio Transcripts (instructor key)", "",
                 "Ground-truth transcripts for the audio files in the set. The files "
                 "themselves carry no extracted text — transcription is the exercise.", ""]
        for r in audio:
            tx = media.TRANSCRIPTS.get(r.filename, "(transcript not recorded)")
            lines += [f"## {r.docid} — `{r.filename}`",
                      f"- Custodian: {r.custodian}", f"- Family parent: {r.parentid or '(none)'}",
                      "", "> " + tx, ""]
        (config.ROOT / "docs" / "TRANSCRIPTS.md").write_text("\n".join(lines))

    # 7. Stats + manifest.
    by_type = Counter(r.recordtype for r in records)
    by_cust = Counter(r.custodian for r in records)
    total_bytes = sum(int(r.filesize) for r in records)
    dup_count = sum(1 for a in answers if a["EXACT_DUPLICATE"] == "Yes")
    hot_count = sum(1 for a in answers if a["KEY_DOCUMENT"] == "Yes")
    priv_count = sum(1 for a in answers if a["SUGGESTED_PRIVILEGE"] == "Yes")
    families = sum(1 for r in records if r.recordtype == "E-Mail")
    ext_mix = Counter(r.fileextension for r in records)

    manifest = {
        "generated": dt.datetime.now().isoformat(timespec="seconds"),
        "seed": config.SEED,
        "period": [str(config.PERIOD_START), str(config.PERIOD_END)],
        "volume": config.VOLUME,
        "total_records": len(records),
        "by_recordtype": dict(by_type),
        "by_custodian": dict(by_cust),
        "by_extension": dict(ext_mix),
        "email_families": families,
        "exact_duplicates": dup_count,
        "key_documents": hot_count,
        "suggested_privileged": priv_count,
        "native_bytes": total_bytes,
        "counts_requested": {"routine": args.routine, "noise": args.noise, "loose": args.loose},
    }
    (config.LOADFILE_DIR / "build_manifest.json").write_text(json.dumps(manifest, indent=2))

    # 8. Console summary.
    print("\nBuild complete.")
    print(f"  Total documents : {len(records)}")
    print(f"  By record type  : {dict(by_type)}")
    print(f"  Email families  : {families}")
    print(f"  Exact duplicates: {dup_count}")
    print(f"  Key documents   : {hot_count}")
    print(f"  Privileged (sugg): {priv_count}")
    print(f"  Native data size : {_humansize(total_bytes)}")
    print(f"  File-type mix    : {dict(ext_mix)}")
    print(f"  Custodian spread : {dict(by_cust)}")
    print(f"\n  Load files -> {config.LOADFILE_DIR}")
    print(f"  Answer key -> {config.ROOT / 'docs' / 'ANSWER_KEY.csv'}")


if __name__ == "__main__":
    main()
