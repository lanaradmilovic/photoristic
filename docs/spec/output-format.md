# Output folder

Each step reads the previous step's files from the output folder and writes its own, so steps
can be re-run independently and the pipeline resumes after an interruption.

| File | Written by | Content |
|---|---|---|
| `photos.json` | ingest | `{created, input_dir, photos: [record…]}`, one record per photo, failures included |
| `previews/<id>.jpg` | ingest | oriented preview, long edge `ingest.preview_long_edge` (1536); input for the VLM |
| `thumbs/<id>.jpg` | ingest | oriented thumbnail, long edge `ingest.thumb_long_edge` (320); used for the report and embeddings |
| `embeddings.npz` | group | `keys` (sha256), `vectors` (L2-normalized), `model_name` |
| `people.json` | group | `{model_name, has_people: {sha256: bool}}` from person detection |
| `faces.npz` | group / faces | per face: `face_key` (sha256), `face_bbox`, `face_score`, `face_kps` (5×2, preview px), `face_emb` (512-d); `photo_keys` lists every processed photo |
| `identities.json` | group / faces | `{threshold, identities: {label: {n_faces, n_photos}}, photos: {sha256: {ids, faces, n_faces}}}` |
| `faces_sheets/<label>.jpg` | faces --sheets | contact sheet of all faces of one identity (review only) |
| `groups.json` | group | `{created, config_used, n_groups, n_photos, groups: [group…]}` |
| `segments.json` | group / segments | day segments at shooting pauses, with per-segment statistics, see [segments.md](segments.md) |
| `segments_sheets/<segment_id>.jpg` | segments --sheets | contact sheet of one segment (review only) |
| `report.html` | group / report | visual check of the groups; also the labelling tool (*Label mode*) |
| `labels.json` | label | ground truth, see [labels.md](labels.md) |
| `errors.jpg`, `errors.<suffix>.jpg` | score | contact sheet of the boundaries where the grouping disagrees with the labels (`errors.nofaces.jpg` for `groups.nofaces.json`) |
| `judge_pairs.json` | judge | the grey-zone pairs selected for the VLM judge, with the selection statistics |
| `judge_pairs.jpg` | judge | contact sheet of those pairs (`judge_pairs_02.jpg`, … when very long) |
| `judge_pairs/<a>_<b>.jpg` | judge | one side-by-side image per pair, exactly what is sent to the VLM |
| `judge_verdicts.json` | judge | the VLM's verdict per pair (written after every pair; resume state) and the comparison with `labels.json` |
| `cull.log` | all | file names, counts, timings and errors; never image content |

Judge file schemas are in [vlm-judge.md](vlm-judge.md#files).

## Photo record

`photos.json` → `photos[]`:

| Field | Meaning |
|---|---|
| `id` | First 16 hex characters of the SHA-256 of the primary file (the NEF if present). Byte-identical copies get a `-dupN` suffix. Failed hashing gives `err-…`. |
| `sha256` | Full hash of the primary file. Used as the cache key for embeddings, faces and labels. |
| `primary_path`, `nef_path`, `jpg_path` | Absolute paths. `primary_path` is the NEF if present. |
| `preview_source` | `jpg` or `nef_embedded`. |
| `preview_file`, `thumb_file` | Paths relative to the output folder. |
| `capture_time` | ISO 8601 local camera time, e.g. `2024-06-15T16:23:45.370000`. `null` if unknown. |
| `capture_time_has_subsec` | Whether sub-second precision came from EXIF. |
| `camera_id` | `SN<serial>`, or `<make> <model>` if there is no serial. |
| `camera_serial`, `camera_make`, `camera_model` | Raw EXIF values. |
| `orientation` | EXIF orientation (1–8) that was applied to the preview. |
| `preview_w/h`, `original_preview_w/h` | Size of the saved preview and of the source JPEG. |
| `file_size`, `mtime_ns` | Used for resume. |
| `status`, `error` | `ok` or `error`, plus the reason. |
| `flags` | Any of `no_timestamp`, `no_camera_serial`, `preview_fallback`, `duplicate_file`. |

## Group record

`groups.json` → `groups[]`:

| Field | Meaning |
|---|---|
| `group_id` | e.g. `g0001` |
| `camera_id` | Camera the group belongs to. |
| `photo_ids` | Photo ids in capture order. |
| `size`, `start`, `end` | Number of photos and time span. |
| `consecutive_similarities`, `consecutive_gaps_seconds` | Between neighbours; length is `size-1`. For a look-back photo they are the time since the group's last photo and the similarity to its best-matching photo. |
| `joined_by` | For each photo after the first: `neighbour`, `lookback`, or `moved` (moved by boundary refinement). |
| `min_similarity` | Weakest link in the group. |
| `boundary_similarity`, `boundary_gap_seconds` | Between this group's first photo and the previous photo of the same camera, i.e. why the cut happened. |
| `split_from`, `split_part` | Set when an oversized group was split, e.g. `split_part: [2, 3]` (only with `max_group_size > 0`). |
| `flags` | `split`, `lookback`, `moved`, `faces` (a photo joined only because both show the same identified people), `faces_split` (a join the usual rules allowed was blocked because the identified people differ), `ingest_error`, `no_timestamp`, `no_embedding`. |
