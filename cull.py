"""Command line entry point.

    python cull.py prepare --input <wedding folder> --output <output folder>
    python cull.py ingest  --input <wedding folder> --output <output folder>
    python cull.py group   --output <output folder>     # re-group after changing thresholds
    python cull.py faces   --output <output folder> [--sheets]   # face identities only
    python cull.py segments --output <output folder> [--sheets]  # day segments (segments.json)
    python cull.py report  --output <output folder>
    python cull.py label   --output <output folder> [--port 8765] [--no-browser]   # label boundaries in the browser
    python cull.py score   --output <output folder> [--groups groups.json groups.nofaces.json]
    python cull.py judge   --output <output folder> [--dry-run] [--include-faces-decided] [--max-pairs N]
    python cull.py ping-vlm                             # does the VLM server answer and serve the model?

All commands accept --config (default: config.yaml next to this file).
"""
import argparse
import logging
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

from culling.config import load_config

DEFAULT_CONFIG = Path(__file__).parent / "config.yaml"

log = logging.getLogger("cull")


def setup_logging(out_dir):
    """Console + <out_dir>/cull.log; console only when the command has no output folder."""
    fmt = logging.Formatter("%(asctime)s %(levelname)-7s %(name)s: %(message)s", "%H:%M:%S")
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(fmt)
    handlers = [console]
    if out_dir is not None:
        out_dir.mkdir(parents=True, exist_ok=True)
        logfile = logging.FileHandler(out_dir / "cull.log", encoding="utf-8")
        logfile.setFormatter(fmt)
        handlers.append(logfile)
    root = logging.getLogger()
    root.handlers = handlers
    # Third-party libraries (HTTP clients, model loading) only log warnings; our code logs info.
    root.setLevel(logging.WARNING)
    for ours in ("cull", "culling"):
        logging.getLogger(ours).setLevel(logging.INFO)


def cmd_ingest(args, config):
    from culling.ingest import run_ingest
    return run_ingest(args.input, args.output, config)


def _load_photos_or_exit(args):
    from culling.ingest import load_photos
    photos = load_photos(args.output)
    if not photos:
        sys.exit(f"No photos.json in {args.output} - run 'ingest' or 'prepare' first.")
    return photos


def cmd_faces(args, config, photos=None):
    """Detect faces, cluster them into identities, write identities.json.
    Returns the identities (None when faces are disabled)."""
    from culling.faces import (cluster_identities, detect_faces, save_identities,
                               write_identity_sheets)

    if photos is None:
        photos = _load_photos_or_exit(args)
    if not config["faces"]["enabled"]:
        log.info("Faces: disabled in config")
        return None
    faces = detect_faces(photos, args.output, config)
    identities = cluster_identities(faces, config["faces"])
    save_identities(args.output, identities)
    if getattr(args, "sheets", False):
        write_identity_sheets(args.output, photos, faces, identities)
    return identities


def cmd_group(args, config, photos=None):
    from culling.embed import compute_embeddings
    from culling.faces import photo_signatures
    from culling.grouping import group_photos, save_groups
    from culling.people import detect_people

    if photos is None:
        photos = _load_photos_or_exit(args)
    embeddings = compute_embeddings(photos, args.output, config)
    people = detect_people(photos, args.output, config)
    identities = cmd_faces(args, config, photos)
    signatures = photo_signatures(identities, config["faces"]["min_identity_faces"])
    groups = group_photos(photos, embeddings, config["grouping"], people, signatures)
    save_groups(args.output, groups, config["grouping"])
    sizes = [g["size"] for g in groups]
    log.info("Grouping done: %d photos -> %d groups (%d single, largest %d)",
             len(photos), len(groups), sizes.count(1), max(sizes, default=0))
    try:
        cmd_segments(args, config, photos)
    except Exception:   # segments are a diagnostic add-on: never lose the report because of them
        log.exception("Segments failed; the report is written without them")
        (Path(args.output) / "segments.json").unlink(missing_ok=True)
    cmd_report(args, config, photos, identities)


def cmd_segments(args, config, photos=None):
    """Cut the day into segments at shooting pauses, write segments.json (and the
    contact sheets with --sheets). Returns the segments data (None when disabled)."""
    from culling.segments import run_segments

    if photos is None:
        photos = _load_photos_or_exit(args)
    if not config["segments"]["enabled"]:
        log.info("Segments: disabled in config")
        return None
    return run_segments(args.output, config, photos, sheets=getattr(args, "sheets", False))


def cmd_report(args, config, photos=None, identities=None):
    from culling.embed import load_cache
    from culling.faces import load_identities
    from culling.grouping import load_groups
    from culling.ingest import read_photos_file
    from culling.labels import boundaries, load_labels
    from culling.report import write_report
    from culling.segments import load_segments

    photos_file = read_photos_file(args.output) or {}
    if photos is None:
        photos = photos_file.get("photos", [])
    groups_data = load_groups(args.output)
    input_dir = getattr(args, "input", None) or photos_file.get("input_dir")
    if identities is None and config["faces"]["enabled"]:
        identities = load_identities(args.output)
    embeddings = load_cache(args.output, config["embedding"]["model_name"])
    label_data = {"boundaries": boundaries(photos, groups_data, embeddings),
                  "labels": load_labels(args.output)}
    path = write_report(args.output, photos, groups_data, input_dir, identities, label_data,
                        segments_data=load_segments(args.output) if config["segments"]["enabled"] else None)
    log.info("Report: %s", path.resolve())


def cmd_prepare(args, config):
    photos = cmd_ingest(args, config)
    cmd_group(args, config, photos)


def cmd_label(args, config):
    """Rebuild the report (so the boundaries are current), then serve it for labelling."""
    from culling.labelserver import serve

    _load_photos_or_exit(args)
    cmd_report(args, config)
    serve(args.output, port=args.port, open_browser=not args.no_browser)


def cmd_score(args, config):
    import json

    from culling.embed import load_cache
    from culling.labels import (attach_boundary_info, boundaries, errors_sheet_name,
                                format_comparison, format_report, load_labels, score,
                                write_errors_sheet)

    if len(args.groups) > 2:
        sys.exit("--groups takes one or two files")
    photos = _load_photos_or_exit(args)
    labels = load_labels(args.output)
    if not labels:
        sys.exit(f"No labels in {args.output / 'labels.json'} - run 'label' first.")
    embeddings = load_cache(args.output, config["embedding"]["model_name"])
    results = []
    for name in args.groups:
        path = Path(name) if Path(name).is_absolute() else args.output / name
        with open(path, encoding="utf-8") as f:
            groups_data = json.load(f)
        result = score(labels, photos, groups_data)
        attach_boundary_info(result["errors"], boundaries(photos, groups_data, embeddings))
        sheet = write_errors_sheet(args.output, result["errors"], errors_sheet_name(path))
        print(format_report(path.name, result))
        print(f"errors sheet: {sheet}" if sheet else "errors sheet: none (no errors)")
        print()
        results.append((path.name, result))
    if len(results) == 2:
        print(format_comparison(*results[0], *results[1]))
    return results


def _vlm_help(vlm, error):
    port = urlparse(vlm["base_url"]).port or 8000
    return (f"VLM: {error}\n"
            f"The server at {vlm['base_url']} does not answer or does not serve {vlm['model']}. Start the vLLM "
            f"server or the SSH tunnel (ssh -L {port}:localhost:8000 <host>) and set {vlm['api_key_env']} if the "
            f"server needs a key; `python cull.py ping-vlm` checks the connection.")


def cmd_judge(args, config):
    """Grey-zone pairs for the VLM judge: select them, write the pair images and (without
    --dry-run) ask the server and compare with labels.json. Not part of `prepare`."""
    from culling.judge import run_judge
    from culling.vlm import VLMError

    try:
        run_judge(args.output, config, dry_run=args.dry_run,
                  include_faces_decided=True if args.include_faces_decided else None,
                  max_pairs=args.max_pairs)
    except VLMError as e:
        sys.exit(_vlm_help(config["vlm"], e) + "\nProgress, if any, is saved in judge_verdicts.json; "
                 "rerun the command to resume.")


def cmd_ping_vlm(args, config):
    from culling.vlm import VLMError, make_client

    vlm = config["vlm"]
    try:
        client = make_client(vlm)
    except ValueError as e:  # unknown vlm.provider: a config error, not a server problem
        sys.exit(str(e))
    try:
        models = client.ping()
    except VLMError as e:
        sys.exit(_vlm_help(vlm, e))
    print(f"{vlm['base_url']} serves {vlm['model']} (models: {', '.join(models)})")


def main():
    parser = argparse.ArgumentParser(description="Wedding photo culling pipeline")
    sub = parser.add_subparsers(dest="command", required=True)

    def add(name, help_text, needs_input, needs_output=True):
        p = sub.add_parser(name, help=help_text)
        if needs_input:
            p.add_argument("--input", required=True, type=Path, help="wedding folder with NEF/JPG files")
        if needs_output:
            p.add_argument("--output", required=True, type=Path, help="output folder for this wedding")
        p.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="config YAML")
        return p

    add("prepare", "ingest + embeddings + grouping + HTML report", True)
    add("ingest", "extract previews and metadata only", True)
    add("group", "embeddings + people + faces + grouping + report from an existing ingest", False)
    faces = add("faces", "face detection + identity clustering only (identities.json)", False)
    faces.add_argument("--sheets", action="store_true",
                       help="also write faces_sheets/<identity>.jpg contact sheets for review")
    segments = add("segments", "cut the day into segments at shooting pauses (segments.json)", False)
    segments.add_argument("--sheets", action="store_true",
                          help="also write segments_sheets/<segment>.jpg contact sheets for review")
    add("report", "regenerate report.html from photos.json and groups.json", False)
    label = add("label", "serve report.html locally and save ground-truth labels to labels.json", False)
    label.add_argument("--port", type=int, default=8765, help="local port (default 8765)")
    label.add_argument("--no-browser", action="store_true", help="do not open the browser")
    score = add("score", "compare labels.json with one or two groups files", False)
    score.add_argument("--groups", nargs="+", default=["groups.json"], metavar="FILE",
                       help="groups file(s) inside the output folder, or absolute paths (default groups.json)")
    judge = add("judge", "grey-zone pairs (similarity judge.sim_low..sim_high) judged by the VLM; writes "
                         "judge_pairs.json, judge_pairs.jpg, judge_pairs/ and judge_verdicts.json", False)
    judge.add_argument("--dry-run", action="store_true",
                       help="select the pairs and write the images, print the estimate, send nothing")
    judge.add_argument("--include-faces-decided", action="store_true",
                       help="also send pairs that face identities already decided (same/different)")
    judge.add_argument("--max-pairs", type=int, default=None, metavar="N",
                       help="judge at most N pairs (default: judge.max_pairs, 0 = all)")
    add("ping-vlm", "check that the VLM server (config vlm) answers and serves the model", False,
        needs_output=False)
    args = parser.parse_args()

    config = load_config(args.config)
    setup_logging(getattr(args, "output", None))
    log.info("Command: %s (config %s)", args.command, args.config)
    started = time.time()
    commands = {"prepare": cmd_prepare, "ingest": cmd_ingest, "group": cmd_group,
                "faces": cmd_faces, "segments": cmd_segments, "report": cmd_report, "label": cmd_label, "score": cmd_score,
                "judge": cmd_judge, "ping-vlm": cmd_ping_vlm}
    commands[args.command](args, config)
    log.info("Finished in %.1f s", time.time() - started)


if __name__ == "__main__":
    main()
