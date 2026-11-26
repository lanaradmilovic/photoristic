"""A wedding as the agency sends it: their cull, and the originals deleted once they are not needed.

The agency's editor culls in Photo Mechanic and moves rejected photos into a folder
(`agency.rejected_folder`, "obrisano"). Their decision is read either from that "after"
folder or from a plain list of rejected file names (`dir /b > obrisano.txt`), matched to
photos.json by file name without extension, and written to agency_cull.json.

After `prepare`, nothing reads the original files again: previews, thumbnails, embeddings
and faces live in the output folder. `delete_originals` removes the originals of every
photo that is fully processed, and the copies in the "after" folder, and writes the list to
originals_deleted.txt. While that file exists, ingest refuses to run (it would drop every
photo whose file is gone).
"""
import json
import logging
import os
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from culling.ingest import DELETED_MARKER, JPG_EXTS, NEF_EXTS, load_photos

log = logging.getLogger(__name__)

CULL_FILE = "agency_cull.json"
PHOTO_EXTS = set(JPG_EXTS) | set(NEF_EXTS)


def _stem(name):
    return Path(name.strip()).stem.lower()


def read_rejected_list(path):
    """File names, one per line (`dir /b` output); paths and blank lines are fine."""
    names = []
    for line in Path(path).read_text(encoding="utf-8-sig", errors="replace").splitlines():
        line = line.strip().strip('"')
        if line and Path(line.replace("\\", "/")).suffix.lower() in PHOTO_EXTS:
            names.append(Path(line.replace("\\", "/")).name)
    return names


def scan_after_folder(after_dir, rejected_folder, exclude_names=()):
    """{stem: set of 'kept'/'rejected'} and the photo files found, from the agency's folder.
    Folders named in `exclude_names` (montages) are skipped, as in ingest."""
    exclude = {n.lower() for n in exclude_names}
    seen = defaultdict(set)
    files = []
    for path in sorted(Path(after_dir).rglob("*")):
        if not path.is_file() or path.suffix.lower() not in PHOTO_EXTS or path.name.startswith("._"):
            continue
        folders = [part.lower() for part in path.relative_to(after_dir).parts[:-1]]
        if exclude & set(folders):
            continue
        rejected = rejected_folder.lower() in folders
        seen[_stem(path.name)].add("rejected" if rejected else "kept")
        files.append(path)
    return seen, files


def build_cull(photos, seen, source, complete):
    """Decision per photo id. `complete` = the source lists kept photos too (an "after"
    folder); otherwise every photo not listed as rejected counts as kept."""
    by_stem = defaultdict(list)
    for p in photos:
        by_stem[_stem(p["primary_path"])].append(p)
    out, counts = {}, defaultdict(int)
    for stem, plist in by_stem.items():
        marks = seen.get(stem, set())
        if len(plist) > 1:
            decision = "ambiguous"          # two photos share a file name
        elif marks == {"rejected"}:
            decision = "rejected"
        elif marks == {"kept"}:
            decision = "kept"
        elif marks:
            decision = "both"               # in a kept folder and in the rejected folder
        else:
            decision = "missing" if complete else "kept"
        for p in plist:
            out[p["id"]] = {"name": Path(p["primary_path"]).name, "decision": decision}
            counts[decision] += 1
    unmatched = sorted(s for s in seen if s not in by_stem)
    return {"created": datetime.now().isoformat(timespec="seconds"), "source": str(source),
            "counts": dict(counts), "photos": out, "unmatched": unmatched}


def import_cull(out_dir, config, rejected_list=None, after_dir=None, exclude_names=()):
    """Write agency_cull.json; returns (cull, photo files of the after folder)."""
    photos = load_photos(out_dir)
    if after_dir:
        seen, files = scan_after_folder(after_dir, config["agency"]["rejected_folder"], exclude_names)
        cull = build_cull(photos, seen, after_dir, complete=True)
    else:
        seen = {_stem(n): {"rejected"} for n in read_rejected_list(rejected_list)}
        files = []
        cull = build_cull(photos, seen, rejected_list, complete=False)
    path = Path(out_dir) / CULL_FILE
    path.write_text(json.dumps(cull, indent=1, ensure_ascii=False), encoding="utf-8")
    log.info("Agency cull: %s -> %s", dict(cull["counts"]), path)
    if cull["unmatched"]:
        log.warning("%d names of the agency's list match no photo, e.g. %s",
                    len(cull["unmatched"]), ", ".join(cull["unmatched"][:5]))
    return cull, files


def deletable(out_dir, photos, groups_data):
    """Photos whose originals may go: ingested ok, preview and thumbnail written, in a group,
    and the file on disk is still the one that was ingested. Returns (ok, kept_back)."""
    out_dir = Path(out_dir)
    grouped = {pid for g in (groups_data or {}).get("groups", []) for pid in g["photo_ids"]}
    ok, kept_back = [], []
    for p in photos:
        files = [f for f in (p.get("nef_path"), p.get("jpg_path")) if f]
        reason = None
        if p.get("status") != "ok":
            reason = "ingest failed"
        elif not (out_dir / p["preview_file"]).exists() or not (out_dir / p["thumb_file"]).exists():
            reason = "preview missing"
        elif p["id"] not in grouped:
            reason = "not grouped"
        elif not os.path.exists(p["primary_path"]) or os.path.getsize(p["primary_path"]) != p["file_size"]:
            reason = "file changed or gone"
        (kept_back if reason else ok).append((p, files, reason))
    return ok, kept_back


def delete_originals(out_dir, input_dir, photos, groups_data, after_files=(), cull=None):
    """Delete originals of fully processed photos and their copies in the after folder.
    Only files listed in photos.json (under input_dir) and after-folder copies whose name
    matches a deleted photo are touched. Returns (n_files, bytes)."""
    out_dir, input_dir = Path(out_dir), Path(input_dir).resolve()
    ok, kept_back = deletable(out_dir, photos, groups_data)
    for p, _, reason in kept_back:
        log.warning("Keeping %s: %s", p["primary_path"], reason)
    targets = []
    for p, files, _ in ok:
        for f in files:
            if input_dir in Path(f).resolve().parents:
                targets.append(Path(f))
    done_stems = {_stem(p["primary_path"]) for p, _, _ in ok}
    ambiguous = {_stem(v["name"]) for v in (cull or {}).get("photos", {}).values()
                 if v["decision"] == "ambiguous"}
    targets += [f for f in after_files if _stem(f.name) in done_stems and _stem(f.name) not in ambiguous]
    marker = out_dir / DELETED_MARKER
    n, size = 0, 0
    with open(marker, "a", encoding="utf-8") as log_file:
        log_file.write(f"# {datetime.now().isoformat(timespec='seconds')}\n")
        for f in targets:
            try:
                s = f.stat().st_size
                f.unlink()
            except OSError as e:
                log.warning("Could not delete %s: %s", f, e)
                continue
            log_file.write(f"{f}\n")
            n, size = n + 1, size + s
    log.info("Deleted %d original files (%.1f GB); %d photos kept back; list in %s",
             n, size / 1e9, len(kept_back), marker)
    return n, size
