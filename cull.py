"""Command line entry point.

    python cull.py prepare --input <wedding folder> --output <output folder>
    python cull.py ingest  --input <wedding folder> --output <output folder>
    python cull.py group   --output <output folder>     # re-group after changing thresholds
    python cull.py faces   --output <output folder> [--sheets]   # face identities only
    python cull.py report  --output <output folder>

All commands accept --config (default: config.yaml next to this file).
"""
import argparse
import logging
import sys
import time
from pathlib import Path

from culling.config import load_config

DEFAULT_CONFIG = Path(__file__).parent / "config.yaml"

log = logging.getLogger("cull")


def setup_logging(out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    fmt = logging.Formatter("%(asctime)s %(levelname)-7s %(name)s: %(message)s", "%H:%M:%S")
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(fmt)
    logfile = logging.FileHandler(out_dir / "cull.log", encoding="utf-8")
    logfile.setFormatter(fmt)
    root = logging.getLogger()
    root.handlers = [console, logfile]
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
    cmd_report(args, config, photos, identities)


def cmd_report(args, config, photos=None, identities=None):
    from culling.faces import load_identities
    from culling.grouping import load_groups
    from culling.ingest import read_photos_file
    from culling.report import write_report

    photos_file = read_photos_file(args.output) or {}
    if photos is None:
        photos = photos_file.get("photos", [])
    groups_data = load_groups(args.output)
    input_dir = getattr(args, "input", None) or photos_file.get("input_dir")
    if identities is None and config["faces"]["enabled"]:
        identities = load_identities(args.output)
    path = write_report(args.output, photos, groups_data, input_dir, identities)
    log.info("Report: %s", path.resolve())


def cmd_prepare(args, config):
    photos = cmd_ingest(args, config)
    cmd_group(args, config, photos)


def main():
    parser = argparse.ArgumentParser(description="Wedding photo culling pipeline")
    sub = parser.add_subparsers(dest="command", required=True)

    def add(name, help_text, needs_input):
        p = sub.add_parser(name, help=help_text)
        if needs_input:
            p.add_argument("--input", required=True, type=Path, help="wedding folder with NEF/JPG files")
        p.add_argument("--output", required=True, type=Path, help="output folder for this wedding")
        p.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="config YAML")
        return p

    add("prepare", "ingest + embeddings + grouping + HTML report", True)
    add("ingest", "extract previews and metadata only", True)
    add("group", "embeddings + people + faces + grouping + report from an existing ingest", False)
    faces = add("faces", "face detection + identity clustering only (identities.json)", False)
    faces.add_argument("--sheets", action="store_true",
                       help="also write faces_sheets/<identity>.jpg contact sheets for review")
    add("report", "regenerate report.html from photos.json and groups.json", False)
    args = parser.parse_args()

    config = load_config(args.config)
    setup_logging(args.output)
    log.info("Command: %s (config %s)", args.command, args.config)
    started = time.time()
    commands = {"prepare": cmd_prepare, "ingest": cmd_ingest, "group": cmd_group,
                "faces": cmd_faces, "report": cmd_report}
    commands[args.command](args, config)
    log.info("Finished in %.1f s", time.time() - started)


if __name__ == "__main__":
    main()
