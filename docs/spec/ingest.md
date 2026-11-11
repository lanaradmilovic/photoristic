# Ingest (step 1)

Status: implemented (`culling/ingest.py`, `culling/metadata.py`, `tests/test_ingest.py`).
Decisions: [0001](../decisions/0001-nef-jpg-one-photo.md), [0002](../decisions/0002-embedded-preview-no-raw-decoding.md), [0003](../decisions/0003-camera-by-serial-group-per-camera.md).

- **Scanning:** recursive; NEF+JPG with the same stem in the same folder are one photo.
  - AppleDouble `._<name>.NEF` files (4 KB, from Mac copies) are skipped by name plus the magic
    bytes `00 05 16 07`; the count is logged.
  - The output folder is skipped when it is inside the input.
- **Hash:** streamed SHA-256 of the primary file (the NEF if present). Cached, so the I/O cost is
  paid once per wedding.
- **Metadata (exifread):**
  - `DateTimeOriginal` + `SubSecTimeOriginal`
  - serial number: `EXIF BodySerialNumber`, then `MakerNote SerialNumber`, then make+model with a
    warning (two bodies of the same model would merge)
  - make, model, orientation
- **Preview:**
  - from the JPG if present, otherwise the NEF's embedded JPEG (`rawpy.extract_thumb`), rotated by
    the NEF's IFD0 orientation (Nikon stores the embedded preview unrotated)
  - fast decoding via `Image.draft`
  - saved as preview (`ingest.preview_long_edge`, 1536) + thumb (`ingest.thumb_long_edge`, 320)
- **Parallelism:** `ProcessPoolExecutor` with `ingest.workers`.
- **Resume:** unchanged path, size and mtime plus existing outputs → the record is reused.
  `photos.json` is checkpointed every `save_every` photos.
- **Failures:** kept as `status: error` records, never dropped.

Record format: [output-format.md](output-format.md#photo-record).

Measured on talici 4a (334 NEF, Nikon D5): every NEF had a full-size embedded preview
(5568×3712), the serial was found, sub-seconds on all photos, ~57 s from OneDrive.

Not yet checked (see [plan](../plan.md#phase-1--ingest)): a two-camera wedding, ingest time for
~2,500 NEF, bodies without `BodySerialNumber` or with only a small embedded preview.
