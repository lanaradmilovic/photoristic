# Ingest (step 1)

Status: implemented (`culling/ingest.py`, `culling/metadata.py`, `tests/test_ingest.py`).
Decisions: [0001](../decisions/0001-nef-jpg-one-photo.md), [0002](../decisions/0002-embedded-preview-no-raw-decoding.md), [0003](../decisions/0003-camera-by-serial-group-per-camera.md).

- **Scanning:** recursive; NEF+JPG with the same stem in the same folder are one photo.
  - AppleDouble `._<name>.NEF` files (4 KB, from Mac copies) are skipped by name plus the magic
    bytes `00 05 16 07`; the count is logged.
  - The output folder is skipped when it is inside the input.
  - `--exclude FOLDER ...` skips folders of that name at any depth inside the input (compared
    without case), for files that are not photos of the day: montages, exports. The number of
    skipped files is logged; a name that matches nothing is a warning.
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

## Agency packages

`cull.py agency` (`culling/agency.py`) is `prepare` for a wedding sent by the agency, which
arrives twice: as handed over by the photographers and after their editor's cull in Photo
Mechanic (rejects moved to `agency.rejected_folder`, `obrisano`;
[research](../research/2026-11-26-glamur-cull.md)).

- **The cull** comes from `--after D` (photo files under a folder named `obrisano` = rejected,
  elsewhere = kept; `--exclude` folders skipped) or `--rejected F` (one file name per line; all
  other photos = kept). Matched to `photos.json` by file name without extension.
  `agency_cull.json`: `{created, source, counts, photos: {id: {name, decision}}, unmatched}`,
  decision `kept | rejected | both | missing | ambiguous` (`both`: in a kept and the rejected
  folder; `missing`: not in D; `ambiguous`: two photos share the file name).
- **Deleting originals** (default; `--keep-originals` turns it off). After `prepare` nothing reads
  an original again. A photo's NEF/JPG is deleted only when its record is `ok`, preview and
  thumbnail exist, it is in `groups.json`, and the file has the size it had at ingest; otherwise it
  stays and a warning names the reason. Copies in D with the same name are deleted with it.
  Other files (PSD, montages, files outside X) are never touched. Every deleted path is appended
  to `originals_deleted.txt`.
- **After deletion** `run_ingest` refuses to run while `originals_deleted.txt` exists (it would
  drop every photo whose file is gone); `agency` skips `prepare` then, `group` and `report` work
  as before. A re-ingest needs the originals back and the file removed.

Not yet checked (see [plan](../plan.md#phase-1--ingest)): a two-camera wedding, ingest time for
~2,500 NEF, bodies without `BodySerialNumber` or with only a small embedded preview.
