"""Command line entry point.

    python cull.py prepare --input <wedding folder> --output <output folder>
    python cull.py ingest  --input <wedding folder> --output <output folder>
    python cull.py group   --output <output folder>     # re-group after changing thresholds
    python cull.py faces   --output <output folder> [--sheets]   # face identities only
    python cull.py segments --output <output folder> [--sheets]  # day segments (segments.json)
    python cull.py report  --output <output folder>
    python cull.py label   --output <output folder> [--port 8765] [--no-browser]   # label boundaries in the browser
    python cull.py score   --output <output folder> [--groups groups.json groups.nofaces.json] [--labels FILE]
    python cull.py meeting --output <meeting folder> [--port 8765] [--no-browser]   # feedback or question page for the agency (meeting.json)
    python cull.py meeting-score --output <meeting folder>   # what the agency answered
    python cull.py judge   --output <output folder> [--dry-run] [--include-faces-decided] [--max-pairs N]
    python cull.py rank    --output <output folder> [--dry-run] [--max-requests N]   # best photo per group
    python cull.py pick    --output <output folder> [--port 8765] [--no-browser] [--review-model] [--sample FILE] [--picks-file NAME]   # mark the best photo(s) per group
    python cull.py pick-score --output <output folder> [--picks-file NAME] [--compare NAME]  # ranking.json vs picks.json
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
    from culling.ranking import ranking_for_report
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
                        segments_data=load_segments(args.output) if config["segments"]["enabled"] else None,
                        ranking=ranking_for_report(args.output, groups_data))
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


def cmd_pick(args, config):
    """Write picks.html (one multi-photo group per screen) and serve it; picks.json is
    written after every click."""
    from culling.grouping import load_groups
    from culling.labelserver import serve
    from culling.picks import build_items, write_page

    photos = _load_photos_or_exit(args)
    if not (args.output / "groups.json").exists():
        sys.exit(f"No groups.json in {args.output} - run 'group' first.")
    if args.review_model:
        # The model's choice on the screen: one ranked variant per screen, with its reason.
        import json

        from culling.picks import REVERSED_FILE, build_model_items
        from culling.ranking import load_ranking
        ranking = load_ranking(args.output)
        if not ranking or not ranking.get("answers"):
            sys.exit(f"No answers in {args.output / 'ranking.json'} - run 'rank' first.")
        reversed_file = args.output / REVERSED_FILE
        reversed_rows = json.loads(reversed_file.read_text(encoding="utf-8")) if reversed_file.exists() else None
        items = build_model_items(photos, ranking, reversed_rows)
        if not items:
            sys.exit("ranking.json has no ranked variant for these photos.")
        write_page(args.output, items, review=True)
        log.info("picks.html: %d variants ranked by %s%s", len(items), ranking.get("model"),
                 f", with the reversed-order check of {REVERSED_FILE}" if reversed_rows else "")
        serve(args.output, port=args.port, open_browser=not args.no_browser, page="picks.html",
              picks_file=args.picks_file)
        return
    sample = None
    if args.sample:
        # A chosen few groups for a meeting with the agency: short rules, usually their own picks file.
        from culling.picks import load_sample
        try:
            sample = load_sample(args.sample)
        except (OSError, ValueError) as e:
            sys.exit(str(e))
    try:
        items = build_items(photos, load_groups(args.output), sample)
    except ValueError as e:
        sys.exit(str(e))
    if not items:
        sys.exit("No group with two or more photos: nothing to pick.")
    write_page(args.output, items, meeting=sample is not None)
    log.info("picks.html: %d groups%s, picks in %s", len(items),
             " of the sample" if sample else " with two or more photos", args.picks_file)
    serve(args.output, port=args.port, open_browser=not args.no_browser, page="picks.html",
          picks_file=args.picks_file)


def cmd_pick_score(args, config):
    from culling.picks import (compare_picks, format_comparison, format_reasons, format_score,
                               load_picks, score_ranking)
    from culling.ranking import load_ranking

    photos = _load_photos_or_exit(args)
    picks = load_picks(args.output, args.picks_file)
    if not picks:
        sys.exit(f"No picks in {args.output / args.picks_file} - run 'pick' first.")
    ranking = load_ranking(args.output)
    if not ranking:
        sys.exit(f"No ranking.json in {args.output} - run 'rank' first.")
    result = score_ranking(picks, photos, ranking)
    names = {p["sha256"]: Path(p["primary_path"]).name for p in photos if p.get("sha256")}
    print(f"== {args.picks_file}")
    print(format_score(result, names))
    print(format_reasons(picks))
    if args.compare:
        print(format_comparison(compare_picks(picks, load_picks(args.output, args.compare)),
                                args.picks_file, args.compare))
    return result


def _meeting_data_or_exit(args):
    from culling.meeting import build_page_data, load_definition

    try:
        return build_page_data(load_definition(args.output))
    except (ValueError, OSError) as e:
        sys.exit(str(e))


def cmd_meeting(args, config):
    """Write meeting.html from meeting.json (disputed pairs + excerpts of the grouping),
    copy the previews it shows and serve it; meeting_answers.json is written on every click."""
    from culling.labelserver import serve
    from culling.meeting import copy_previews, write_page

    data = _meeting_data_or_exit(args)
    copied = copy_previews(args.output, data)
    write_page(args.output, data)
    log.info("meeting.html: %d disputed pairs, %d excerpts with %d groups, %d questions; %d previews copied",
             len(data["cases"]), len(data["excerpts"]), sum(len(x["groups"]) for x in data["excerpts"]),
             len(data["questions"]), copied)
    serve(args.output, port=args.port, open_browser=not args.no_browser, page="meeting.html")


def cmd_meeting_score(args, config):
    from culling.meeting import load_answers, summary

    answers = load_answers(args.output)
    if not answers["pairs"] and not answers["choices"]:
        sys.exit(f"No answers in {args.output / 'meeting_answers.json'} - run 'meeting' first.")
    print(summary(answers, _meeting_data_or_exit(args)))


def cmd_score(args, config):
    import json

    from culling.embed import load_cache
    from culling.labels import (attach_boundary_info, boundaries, errors_sheet_name,
                                format_comparison, format_report, load_labels, read_labels_file,
                                score, write_errors_sheet)

    if len(args.groups) > 2:
        sys.exit("--groups takes one or two files")
    photos = _load_photos_or_exit(args)
    if args.labels:
        if not args.labels.exists():
            sys.exit(f"No labels file {args.labels}")
        labels = read_labels_file(args.labels)
    else:
        labels = load_labels(args.output)
    if not labels:
        sys.exit(f"No labels in {args.labels or args.output / 'labels.json'} - run 'label' first.")
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


def cmd_rank(args, config):
    """Best photo per group: variants in code, the VLM orders each variant, ranking.json;
    then the report is rebuilt to show the decisions. Not part of `prepare`."""
    from culling.ranking import run_ranking
    from culling.vlm import VLMError

    try:
        run_ranking(args.output, config, dry_run=args.dry_run, max_requests=args.max_requests)
    except VLMError as e:
        sys.exit(_vlm_help(config["vlm"], e) + "\nProgress, if any, is saved in ranking.json; "
                 "rerun the command to resume.")
    cmd_report(args, config)


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
    # Serbian text (notes, question titles) must print when the output is piped or
    # redirected too: the Windows default code page has no č, ć or đ.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
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
    score.add_argument("--labels", type=Path, default=None, metavar="FILE",
                       help="labels file instead of labels.json in the output folder, e.g. the agency's "
                            "meeting_answers.json (pairs of other weddings are skipped)")
    meeting = add("meeting", "feedback page for the agency from meeting.json in the output folder "
                             "(disputed pairs, excerpts of the grouping, questions); writes meeting_answers.json", False)
    meeting.add_argument("--port", type=int, default=8765, help="local port (default 8765)")
    meeting.add_argument("--no-browser", action="store_true", help="do not open the browser")
    add("meeting-score", "summary of meeting_answers.json: answers, cuts, joins, differences from labels.json", False)
    judge = add("judge", "grey-zone pairs (similarity judge.sim_low..sim_high) judged by the VLM; writes "
                         "judge_pairs.json, judge_pairs.jpg, judge_pairs/ and judge_verdicts.json", False)
    judge.add_argument("--dry-run", action="store_true",
                       help="select the pairs and write the images, print the estimate, send nothing")
    judge.add_argument("--include-faces-decided", action="store_true",
                       help="also send pairs that face identities already decided (same/different)")
    judge.add_argument("--max-pairs", type=int, default=None, metavar="N",
                       help="judge at most N pairs (default: judge.max_pairs, 0 = all)")
    rank = add("rank", "best photo per group: variants in code, the VLM orders each variant (ranking.json)", False)
    rank.add_argument("--dry-run", action="store_true",
                      help="write the variants and the decisions so far, print the estimate, send nothing")
    rank.add_argument("--max-requests", type=int, default=None, metavar="N",
                      help="send at most N requests in this run (default: all open ones)")
    pick = add("pick", "mark the best photo(s) of every multi-photo group in the browser (picks.json)", False)
    pick.add_argument("--port", type=int, default=8765, help="local port (default 8765)")
    pick.add_argument("--no-browser", action="store_true", help="do not open the browser")
    pick.add_argument("--review-model", action="store_true",
                      help="show the model's choice and reason from ranking.json, one ranked variant per screen")
    pick.add_argument("--sample", type=Path, default=None, metavar="FILE",
                      help="show only the groups listed in this JSON file ([{photo, kind}]), in its order, "
                           "with the short rules for a meeting with the agency")
    pick.add_argument("--picks-file", default="picks.json", metavar="NAME",
                      help="file in the output folder that holds the picks (default picks.json), "
                           "e.g. picks.agency.json for the agency's own picks")
    pick_score = add("pick-score", "compare ranking.json with picks.json; reasons and notes given", False)
    pick_score.add_argument("--picks-file", default="picks.json", metavar="NAME",
                            help="picks file in the output folder (default picks.json)")
    pick_score.add_argument("--compare", default=None, metavar="NAME",
                            help="another picks file in the output folder: how often both chose the same")
    add("ping-vlm", "check that the VLM server (config vlm) answers and serves the model", False,
        needs_output=False)
    args = parser.parse_args()

    config = load_config(args.config)
    setup_logging(getattr(args, "output", None))
    log.info("Command: %s (config %s)", args.command, args.config)
    started = time.time()
    commands = {"prepare": cmd_prepare, "ingest": cmd_ingest, "group": cmd_group,
                "faces": cmd_faces, "segments": cmd_segments, "report": cmd_report, "label": cmd_label, "score": cmd_score,
                "judge": cmd_judge, "rank": cmd_rank, "pick": cmd_pick, "pick-score": cmd_pick_score, "ping-vlm": cmd_ping_vlm,
                "meeting": cmd_meeting, "meeting-score": cmd_meeting_score}
    commands[args.command](args, config)
    log.info("Finished in %.1f s", time.time() - started)


if __name__ == "__main__":
    main()
