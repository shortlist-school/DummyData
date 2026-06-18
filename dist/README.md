# Distribution

A packaged, downloadable copy of the Tudor eDiscovery dataset.

| File | Contents | Size | MD5 |
|---|---|---|---|
| `tudor-ediscovery-dataset-v1.0.zip` | `README.md`, `docs/`, and the full `data/VOL001/` production volume | ~11.7 MB | `4782631c92d6221f542045b0943b324b` |

The archive expands to a single folder, `tudor-ediscovery-dataset/`, containing:

```
tudor-ediscovery-dataset/
├── README.md
├── docs/                     # dataset guide, characters, field dictionary,
│                             # demo scenarios, answer key, transcripts
└── data/VOL001/
    ├── NATIVES/              # native files (.eml/.docx/.xlsx/.pdf/.png/.wav/.rsmf/...)
    ├── TEXT/                 # extracted text, one .txt per document
    └── DATA/                 # loadfile.dat, loadfile.csv, chat_messages.csv, manifest
```

## Verify the download

```bash
md5sum tudor-ediscovery-dataset-v1.0.zip
# expected: 4782631c92d6221f542045b0943b324b
unzip -t tudor-ediscovery-dataset-v1.0.zip   # integrity test
```

## Use it

Unzip, then point your review platform at
`tudor-ediscovery-dataset/data/VOL001/DATA/loadfile.dat` (UTF-8; Concordance
delimiters þ / ¶ / ®) or the `loadfile.csv` mirror. Natives and extracted text
are referenced by the `NATIVELINK` / `TEXTLINK` columns. See the bundled `docs/`
for the data dictionary and ready-made demo exercises.

> This archive is a build artifact. To regenerate the dataset (and this zip)
> from source, use the generator in the repository root — the build is seeded
> and deterministic, so it reproduces byte-for-byte.
