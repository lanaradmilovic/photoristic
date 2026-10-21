"""HTML report for checking the grouping by eye.

A single static report.html in the output folder. It links to thumbs/ and
previews/ by relative path and loads nothing from the internet.
"""
import html
from collections import Counter
from datetime import datetime
from pathlib import Path

REPORT_FILE = "report.html"

CSS = """
:root { --bg:#f6f6f4; --card:#fff; --text:#1d1d1f; --muted:#6b6b70; --line:#e2e2e0;
        --accent:#2f6fde; --warn:#c2410c; --warnbg:#fff1e6; }
@media (prefers-color-scheme: dark) {
  :root { --bg:#161618; --card:#202024; --text:#ececee; --muted:#9a9aa2; --line:#33333a;
          --accent:#6ea0ff; --warn:#fb923c; --warnbg:#3a2516; }
}
* { box-sizing:border-box; }
body { margin:0; padding:16px 24px 64px; background:var(--bg); color:var(--text);
       font:14px/1.4 system-ui, -apple-system, "Segoe UI", sans-serif; }
h1 { font-size:22px; margin:0 0 4px; } h2 { font-size:17px; margin:28px 0 8px; }
.muted { color:var(--muted); }
.summary { display:flex; flex-wrap:wrap; gap:12px; margin:16px 0; }
.stat { background:var(--card); border:1px solid var(--line); border-radius:8px; padding:10px 14px; min-width:120px; }
.stat b { display:block; font-size:20px; }
.panels { display:flex; flex-wrap:wrap; gap:16px; }
.panel { background:var(--card); border:1px solid var(--line); border-radius:8px; padding:12px 14px; }
.panel table { border-collapse:collapse; } .panel td { padding:2px 10px 2px 0; }
.hist { display:grid; grid-template-columns:auto 1fr auto; gap:3px 8px; align-items:center; min-width:280px; }
.bar { height:12px; background:var(--accent); border-radius:2px; }
.controls { position:sticky; top:0; z-index:5; background:var(--bg); padding:10px 0;
            border-bottom:1px solid var(--line); display:flex; flex-wrap:wrap; gap:18px; align-items:center; }
.group { background:var(--card); border:1px solid var(--line); border-radius:8px; margin:10px 0; padding:8px 10px; }
.group.flagged { border-color:var(--warn); }
.ghead { display:flex; flex-wrap:wrap; gap:12px; align-items:baseline; margin-bottom:6px; }
.ghead .gid { font-weight:600; }
.badge { font-size:12px; padding:1px 7px; border-radius:10px; background:var(--warnbg); color:var(--warn); }
.thumbs { display:flex; flex-wrap:wrap; gap:6px; }
figure { margin:0; width:calc(var(--tw) + 4px); }
figure img { display:block; max-width:var(--tw); max-height:var(--tw); border-radius:4px; cursor:zoom-in; background:var(--line); }
.nothumb { width:var(--tw); height:calc(var(--tw) * .66); display:flex; align-items:center; justify-content:center;
           text-align:center; border:1px dashed var(--warn); border-radius:4px; color:var(--warn); font-size:12px; }
figcaption { font-size:11px; color:var(--muted); overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
figcaption .low { color:var(--warn); font-weight:600; }
figcaption .back { color:var(--accent); }
#lightbox { position:fixed; inset:0; background:rgba(0,0,0,.88); display:none; z-index:10;
            align-items:center; justify-content:center; flex-direction:column; color:#eee; }
#lightbox img { max-width:94vw; max-height:88vh; }
#lightbox.open { display:flex; }
.problems td { padding:2px 12px 2px 0; vertical-align:top; }
"""

JS = """
const groups = [...document.querySelectorAll('.group')];
function applyFilters() {
  const hideSingles = document.getElementById('hideSingles').checked;
  const onlyFlagged = document.getElementById('onlyFlagged').checked;
  const cam = document.getElementById('camera').value;
  let shown = 0;
  for (const g of groups) {
    const ok = !(hideSingles && g.dataset.size === '1')
            && !(onlyFlagged && g.dataset.flagged !== '1')
            && (cam === '' || g.dataset.camera === cam);
    g.style.display = ok ? '' : 'none';
    if (ok) shown++;
  }
  document.querySelectorAll('.camhead').forEach(h =>
    h.style.display = (cam === '' || h.dataset.camera === cam) ? '' : 'none');
  document.getElementById('shown').textContent = shown;
}
document.querySelectorAll('.controls input, .controls select').forEach(el =>
  el.addEventListener('input', applyFilters));
document.getElementById('size').addEventListener('input', e =>
  document.body.style.setProperty('--tw', e.target.value + 'px'));

const lb = document.getElementById('lightbox'), lbImg = lb.querySelector('img'),
      lbCap = lb.querySelector('div');
let current = null;
function show(fig) {
  current = fig;
  lbImg.src = fig.dataset.preview;
  lbCap.textContent = fig.dataset.caption;
  lb.classList.add('open');
}
document.querySelectorAll('figure img').forEach(img =>
  img.addEventListener('click', () => show(img.closest('figure'))));
lb.addEventListener('click', () => lb.classList.remove('open'));
document.addEventListener('keydown', e => {
  if (!lb.classList.contains('open')) return;
  if (e.key === 'Escape') lb.classList.remove('open');
  const next = e.key === 'ArrowRight' ? current.nextElementSibling
             : e.key === 'ArrowLeft' ? current.previousElementSibling : null;
  if (next && next.dataset.preview) show(next);
});
applyFilters();
"""


def _e(value):
    return html.escape(str(value), quote=True)


def _clock(iso):
    """'2024-06-15T16:23:45.370000' -> '16:23:45.37'"""
    if not iso:
        return "?"
    t = datetime.fromisoformat(iso)
    s = t.strftime("%H:%M:%S")
    if t.microsecond:
        s += f".{t.microsecond // 10000:02d}"
    return s


def _figure(photo, gap, sim, low_sim, boundary=False, returned=False, moved=False):
    name = Path(photo["primary_path"]).name
    if photo["jpg_path"] and photo["nef_path"]:
        name += " +JPG"
    parts = []
    if gap is not None:
        parts.append(f"+{gap:.2f}s")
    if sim is not None:
        cls = ' class="low"' if (sim < low_sim and not boundary) else ""
        parts.append(f"<span{cls}>{sim:.2f}</span>")
    info = " · ".join(parts)
    if boundary and info:
        info = f"prev group: {info}"
    if returned and info:
        info = f'<span class="back" title="returned to this scene: time since the group\'s last photo, ' \
               f'similarity to its best-matching photo">↩ {info}</span>'
    if moved and info:
        info = f'<span class="back" title="moved here from the neighbouring group: it is more similar ' \
               f'to this group on average">⇄ {info}</span>'
    caption = f"{name} | {_clock(photo['capture_time'])} | {photo['camera_id']}"
    thumb = photo.get("thumb_file") or ""
    preview = photo.get("preview_file") or ""
    if not thumb:
        return (
            f'<figure><div class="nothumb" title="{_e(photo.get("error") or "")}">no preview<br>'
            f'{_e(photo["status"])}</div><figcaption>{_e(name)}</figcaption>'
            f'<figcaption>&nbsp;</figcaption></figure>'
        )
    return (
        f'<figure data-preview="{_e(preview)}" data-caption="{_e(caption)}">'
        f'<img loading="lazy" src="{_e(thumb)}" alt="{_e(name)}" title="{_e(caption)}">'
        f'<figcaption>{_e(name)}</figcaption>'
        f'<figcaption>{info or "&nbsp;"}</figcaption></figure>'
    )


def _group_html(group, photos_by_id, low_sim):
    flags = list(group["flags"])
    if group["min_similarity"] is not None and group["min_similarity"] < low_sim:
        flags.append("low similarity")
    if group["split_part"]:
        i, n = group["split_part"]
        flags = [f for f in flags if f != "split"] + [f"split {i}/{n} of {group['split_from']}"]
    labels = {"lookback": "returned to scene", "moved": "boundary adjusted"}
    flags = [labels.get(f, f) for f in flags]
    joined_by = group.get("joined_by") or ["neighbour"] * (group["size"] - 1)
    flagged = "1" if flags else "0"
    span = f"{_clock(group['start'])} – {_clock(group['end'])}" if group["size"] > 1 else _clock(group["start"])
    min_sim = f"min sim {group['min_similarity']:.2f}" if group["min_similarity"] is not None else ""
    badges = "".join(f'<span class="badge">{_e(f)}</span>' for f in flags)

    figures = []
    for idx, pid in enumerate(group["photo_ids"]):
        photo = photos_by_id[pid]
        if idx == 0:
            figures.append(_figure(photo, group["boundary_gap_seconds"],
                                   group["boundary_similarity"], low_sim, boundary=True))
        else:
            figures.append(_figure(photo, group["consecutive_gaps_seconds"][idx - 1],
                                   group["consecutive_similarities"][idx - 1], low_sim,
                                   returned=joined_by[idx - 1] == "lookback",
                                   moved=joined_by[idx - 1] == "moved"))
    return (
        f'<div class="group{" flagged" if flags else ""}" data-size="{group["size"]}" '
        f'data-camera="{_e(group["camera_id"])}" data-flagged="{flagged}">'
        f'<div class="ghead"><span class="gid">{group["group_id"]}</span>'
        f'<span>{group["size"]} photo{"s" if group["size"] != 1 else ""}</span>'
        f'<span class="muted">{span}</span><span class="muted">{min_sim}</span>{badges}</div>'
        f'<div class="thumbs">{"".join(figures)}</div></div>'
    )


def write_report(out_dir, photos, groups_data, input_dir=None):
    out_dir = Path(out_dir)
    groups = groups_data["groups"]
    cfg = groups_data["config_used"]
    low_sim = cfg.get("report_low_similarity", 0.85)
    photos_by_id = {p["id"]: p for p in photos}

    sizes = Counter(g["size"] for g in groups)
    per_camera = Counter(p["camera_id"] for p in photos)
    failed = [p for p in photos if p["status"] != "ok"]
    no_time = [p for p in photos if p["status"] == "ok" and not p["capture_time"]]
    singles = sizes.get(1, 0)
    multi = len(groups) - singles

    stats = [
        ("photos", len(photos)), ("groups", len(groups)), ("multi-photo groups", multi),
        ("single photos", singles), ("failed", len(failed)), ("no timestamp", len(no_time)),
        ("photos / group", f"{len(photos) / max(len(groups), 1):.2f}"),
    ]
    stats_html = "".join(f'<div class="stat"><b>{_e(v)}</b>{_e(k)}</div>' for k, v in stats)

    max_count = max(sizes.values()) if sizes else 1
    hist_rows = "".join(
        f'<span>{size}</span><div class="bar" style="width:{100 * count / max_count:.1f}%"></div>'
        f'<span class="muted">{count}</span>'
        for size, count in sorted(sizes.items())
    )
    cfg_rows = "".join(f"<tr><td>{_e(k)}</td><td><b>{_e(v)}</b></td></tr>" for k, v in cfg.items())
    cam_rows = "".join(f"<tr><td>{_e(c)}</td><td><b>{n}</b></td></tr>" for c, n in sorted(per_camera.items()))
    cam_options = "".join(f'<option value="{_e(c)}">{_e(c)} ({n})</option>' for c, n in sorted(per_camera.items()))

    body, last_camera = [], None
    for g in groups:
        if g["camera_id"] != last_camera:
            n_groups = sum(1 for x in groups if x["camera_id"] == g["camera_id"])
            body.append(f'<h2 class="camhead" data-camera="{_e(g["camera_id"])}">Camera {_e(g["camera_id"])} '
                        f'<span class="muted">· {n_groups} groups</span></h2>')
            last_camera = g["camera_id"]
        body.append(_group_html(g, photos_by_id, low_sim))

    problem_rows = "".join(
        f"<tr><td>{_e(p['primary_path'])}</td><td>{_e(p['error'] or 'no capture time in EXIF')}</td></tr>"
        for p in failed + no_time
    )
    problems = (f'<h2>Problems ({len(failed) + len(no_time)})</h2>'
                f'<p class="muted">These photos are kept as single-photo groups and must be reviewed by hand.</p>'
                f'<table class="problems">{problem_rows}</table>') if problem_rows else ""

    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Grouping report</title><style>{CSS}</style></head>
<body style="--tw:160px">
<h1>Grouping report</h1>
<div class="muted">{_e(input_dir or "")} · generated {datetime.now():%Y-%m-%d %H:%M}</div>
<div class="summary">{stats_html}</div>
<div class="panels">
  <div class="panel"><b>Group sizes</b><div class="hist">{hist_rows}</div></div>
  <div class="panel"><b>Photos per camera</b><table>{cam_rows}</table></div>
  <div class="panel"><b>Grouping thresholds</b><table>{cfg_rows}</table></div>
</div>
<p class="muted">Under each thumbnail: time gap and similarity to the previous photo of the same camera.
For the first photo of a group these refer to the previous group, i.e. why the group was cut there.
<span style="color:var(--accent)">↩</span> marks a photo that joined by look-back (the photographer returned to the scene):
time since the group's last photo and similarity to its best-matching photo.
<span style="color:var(--accent)">⇄</span> marks a photo moved here from the neighbouring group because it is more similar to this group.
Similarities below {low_sim} are highlighted. Click a thumbnail to open the preview (←/→ to move, Esc to close).</p>
<div class="controls">
  <label><input type="checkbox" id="hideSingles"> hide single photos</label>
  <label><input type="checkbox" id="onlyFlagged"> only flagged groups</label>
  <label>camera <select id="camera"><option value="">all</option>{cam_options}</select></label>
  <label>thumb size <input type="range" id="size" min="80" max="320" value="160"></label>
  <span class="muted"><span id="shown"></span> groups shown</span>
</div>
{"".join(body)}
{problems}
<div id="lightbox"><img alt=""><div></div></div>
<script>{JS}</script>
</body></html>"""
    path = out_dir / REPORT_FILE
    path.write_text(page, encoding="utf-8")
    return path
