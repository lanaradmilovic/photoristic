"""HTML report for checking the grouping by eye.

A single static report.html in the output folder. It links to thumbs/ and
previews/ by relative path and loads nothing from the internet.
"""
import html
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

REPORT_FILE = "report.html"

CSS = """
:root { --bg:#f6f6f4; --card:#fff; --text:#1d1d1f; --muted:#6b6b70; --line:#e2e2e0;
        --accent:#2f6fde; --warn:#c2410c; --warnbg:#fff1e6;
        --ok:#15803d; --bad:#b91c1c; --unsure:#b45309; }
@media (prefers-color-scheme: dark) {
  :root { --bg:#161618; --card:#202024; --text:#ececee; --muted:#9a9aa2; --line:#33333a;
          --accent:#6ea0ff; --warn:#fb923c; --warnbg:#3a2516;
          --ok:#4ade80; --bad:#f87171; --unsure:#fbbf24; }
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
.seghead { display:flex; flex-wrap:wrap; gap:12px; align-items:baseline; margin:22px 0 6px; padding:6px 10px;
           border-left:4px solid var(--accent); background:var(--card); border-radius:0 8px 8px 0; }
.seghead .sid { font-weight:600; color:var(--accent); }
.badge { font-size:12px; padding:1px 7px; border-radius:10px; background:var(--warnbg); color:var(--warn); }
.thumbs { display:flex; flex-wrap:wrap; gap:6px; }
figure { margin:0; width:calc(var(--tw) + 4px); }
figure img { display:block; max-width:var(--tw); max-height:var(--tw); border-radius:4px; cursor:zoom-in; background:var(--line); }
.nothumb { width:var(--tw); height:calc(var(--tw) * .66); display:flex; align-items:center; justify-content:center;
           text-align:center; border:1px dashed var(--warn); border-radius:4px; color:var(--warn); font-size:12px; }
figcaption { font-size:11px; color:var(--muted); overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
figcaption .low { color:var(--warn); font-weight:600; }
figcaption .back { color:var(--accent); }
figcaption.faces { color:var(--text); }
#lightbox { position:fixed; inset:0; background:rgba(0,0,0,.88); display:none; z-index:10;
            align-items:center; justify-content:center; flex-direction:column; color:#eee; }
#lightbox img { max-width:94vw; max-height:88vh; }
#lightbox.open { display:flex; }
.problems td { padding:2px 12px 2px 0; vertical-align:top; }

/* ---- label mode */
#labelView { display:none; }
body.labeling #groupView, body.labeling .gctl, body.labeling .summary, body.labeling .panels,
body.labeling .intro { display:none; }
body.labeling #labelView { display:block; }
.lctl { display:none; align-items:center; gap:10px; flex-wrap:wrap; }
body.labeling .lctl { display:flex; }
.controls button { font:inherit; font-size:13px; padding:3px 10px; border:1px solid var(--line); border-radius:6px;
                   background:var(--card); color:var(--text); cursor:pointer; }
.controls button:disabled { opacity:.5; cursor:default; }
body.labeling #labelMode { background:var(--accent); color:#fff; border-color:transparent; }
#saveStatus.err { color:var(--bad); font-weight:600; }
.legend { margin:10px 0; }
.legend .ex { display:inline-block; width:18px; height:18px; line-height:16px; text-align:center; border-radius:4px;
              font-size:11px; font-weight:600; vertical-align:middle; border:1px solid var(--line); }
.strip { display:flex; flex-wrap:wrap; gap:6px 0; align-items:center; }
.strip figure { align-self:flex-start; }
.strip figcaption.time { color:var(--muted); }
.bnd { width:74px; display:flex; flex-direction:column; align-items:center; gap:3px; padding:4px 2px; margin:0 2px;
       border:1px solid transparent; border-radius:6px; cursor:pointer; font-size:11px; color:var(--muted); }
.bnd .link { width:100%; height:0; border-top:3px solid var(--line); }
.bnd[data-pipe=same] .link { border-top:3px solid var(--ok); }
.bnd[data-pipe=different] .link { border-top:3px dashed var(--bad); }
.bnd .pipe { font-size:10px; text-transform:uppercase; letter-spacing:.3px; }
.bnd[data-pipe=same] .pipe { color:var(--ok); } .bnd[data-pipe=different] .pipe { color:var(--bad); }
.bnd.labeled { border-color:var(--line); background:var(--card); }
.bnd.mismatch { border-left:3px solid var(--bad); }
.bnd.current { outline:2px solid var(--accent); outline-offset:1px; }
.bnd .btns { display:flex; gap:2px; }
.bnd button { width:22px; height:22px; border:1px solid var(--line); border-radius:4px; background:var(--card);
              color:var(--muted); font:600 11px system-ui, sans-serif; cursor:pointer; padding:0; }
.bnd button.suggested { border:2px dotted currentColor; }
.bnd button[data-l=same].suggested, .legend .ex.s-same { color:var(--ok); }
.bnd button[data-l=different].suggested, .legend .ex.s-diff { color:var(--bad); }
.bnd button.chosen, .legend .ex.chosen { color:#fff; border-color:transparent; }
.bnd button[data-l=same].chosen, .legend .ex.c-same { background:var(--ok); }
.bnd button[data-l=different].chosen, .legend .ex.c-diff { background:var(--bad); }
.bnd button[data-l=unsure].chosen, .legend .ex.c-unsure { background:var(--unsure); }
.legend .ex.s-same, .legend .ex.s-diff { border:2px dotted currentColor; }
.bnd .info { white-space:nowrap; }
.bnd .info.low { color:var(--warn); }
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
  document.querySelectorAll('.camhead, .seghead').forEach(h =>
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
  if (e.key === 'Escape') { lb.classList.remove('open'); e.stopImmediatePropagation(); return; }
  const step = e.key === 'ArrowRight' ? 'nextElementSibling'
             : e.key === 'ArrowLeft' ? 'previousElementSibling' : null;
  if (!step) return;
  let next = current[step];
  while (next && !next.dataset.preview) next = next[step];  // skip boundary widgets in label mode
  if (next) show(next);
});
applyFilters();

/* ---------------------------------------------------------------- label mode
   Boundaries between time-adjacent photos of one camera. The pipeline's decision is
   shown as a dotted suggestion; a label is stored only after S / D / U / Enter.
   Served over http (python cull.py label): every change is POSTed to /labels.
   Opened as a file: labels live in localStorage; use Export / Import. */
const labelEl = document.getElementById('labelData');
const LD = labelEl ? JSON.parse(labelEl.textContent) : null;
const serverMode = location.protocol.startsWith('http');
const labels = new Map();            // 'a_sha|b_sha' -> label entry
let bounds = [], bndEls = [], cur = 0, built = false, saveTimer = null, clearArmed = null;
const storageKey = 'labels:' + ((LD && LD.input_dir) || location.pathname);
const keyOf = b => b.a_sha + '|' + b.b_sha;
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const $ = id => document.getElementById(id);

function mergeLabels(list, newerWins) {
  for (const l of list || []) {
    if (!l || !l.a_sha || !l.b_sha || !['same', 'different', 'unsure'].includes(l.label)) continue;
    const k = l.a_sha + '|' + l.b_sha, old = labels.get(k);
    if (!old || !newerWins || (l.labeled_at || '') >= (old.labeled_at || '')) labels.set(k, l);
  }
}
async function loadLabels() {
  labels.clear();
  mergeLabels(LD.labels, false);                       // labels.json at report time
  if (serverMode) {
    try {
      const r = await fetch('/labels', {cache: 'no-store'});
      if (r.ok) { labels.clear(); mergeLabels(await r.json(), false); }   // the file on disk wins
    } catch (e) { setStatus('could not read /labels: ' + e.message, true); }
  } else {
    try { mergeLabels(JSON.parse(localStorage.getItem(storageKey) || '[]'), true); } catch (e) {}
  }
}
function serialise() {
  const seen = new Set(), out = [];
  for (const b of bounds) { const l = labels.get(keyOf(b)); if (l) { out.push(l); seen.add(keyOf(b)); } }
  for (const [k, l] of labels) if (!seen.has(k)) out.push(l);   // labels of pairs no longer adjacent
  return out;
}
function setStatus(text, isError) {
  const el = $('saveStatus'); el.textContent = text; el.classList.toggle('err', !!isError);
}
function scheduleSave() { clearTimeout(saveTimer); saveTimer = setTimeout(save, 300); }
let saving = null, saveAgain = false;   // one POST at a time, so labels.json never gets an older list last
async function save() {
  if (saving) { saveAgain = true; return; }
  saving = saveNow();
  try { await saving; } finally { saving = null; }
  if (saveAgain) { saveAgain = false; save(); }
}
async function saveNow() {
  const list = serialise(), body = JSON.stringify(list);
  if (serverMode) {
    try {
      const r = await fetch('/labels', {method: 'POST', headers: {'Content-Type': 'application/json'}, body});
      if (!r.ok) throw new Error('HTTP ' + r.status);
      setStatus('saved to labels.json (' + list.length + ')', false);
      return;
    } catch (e) { setStatus('save failed: ' + e.message + ' - kept in browser, use Export', true); }
  }
  try {
    localStorage.setItem(storageKey, body);
    if (!serverMode) setStatus('saved in browser only (' + list.length + ') - use Export labels.json', false);
  } catch (e) { setStatus('save failed: ' + e.message + ' - use Export now', true); }
}

function fig(b, side) {
  const thumb = b[side + '_thumb'], name = b[side + '_name'], t = b[side + '_time'].slice(11, 22);
  const img = thumb ? `<img loading="lazy" decoding="async" src="${esc(thumb)}" alt="${esc(name)}">`
                    : '<div class="nothumb">no preview</div>';
  return `<figure data-preview="${esc(b[side + '_preview'])}" data-caption="${esc(name + ' | ' + t)}">${img}` +
         `<figcaption>${esc(name)}</figcaption><figcaption class="time">${esc(t)}</figcaption></figure>`;
}
function build() {
  const parts = [], lowSim = LD.low_sim || 0.85;
  let lastCam = null;
  bounds.forEach((b, i) => {
    if (b.camera_id !== lastCam) {
      if (lastCam !== null) parts.push('</div>');
      parts.push(`<h2>Camera ${esc(b.camera_id)}</h2><div class="strip">`, fig(b, 'a'));
      lastCam = b.camera_id;
    }
    const sim = b.sim == null ? '?' : b.sim.toFixed(2), low = b.sim != null && b.sim < lowSim ? ' low' : '';
    const pipe = b.pipeline === 'same' ? 'pipe: same' : b.pipeline === 'different' ? 'pipe: diff' : 'pipe: ?';
    parts.push(`<div class="bnd" data-i="${i}" data-pipe="${b.pipeline || ''}"><div class="link"></div>` +
               `<div class="pipe">${pipe}</div><div class="btns">` +
               `<button data-l="same" title="same group (S)">S</button>` +
               `<button data-l="different" title="different group (D)">D</button>` +
               `<button data-l="unsure" title="unsure (U)">U</button></div>` +
               `<div class="info${low}" title="similarity · time gap">${sim} · +${b.gap}s</div></div>`, fig(b, 'b'));
  });
  if (lastCam !== null) parts.push('</div>');
  const view = $('labelView');
  view.querySelector('.strips').innerHTML = parts.join('');
  bndEls = [...view.querySelectorAll('.bnd')];
  bndEls.forEach(refresh);
}
function refresh(el) {
  const b = bounds[+el.dataset.i], lab = labels.get(keyOf(b));
  el.classList.toggle('labeled', !!lab);
  el.classList.toggle('mismatch', !!lab && lab.label !== 'unsure' && !!b.pipeline && lab.label !== b.pipeline);
  for (const btn of el.querySelectorAll('button')) {
    btn.classList.toggle('chosen', !!lab && lab.label === btn.dataset.l);
    btn.classList.toggle('suggested', !lab && b.pipeline === btn.dataset.l);
  }
}
function refreshAll() { bndEls.forEach(refresh); updateProgress(); }
function updateProgress() {
  const n = {same: 0, different: 0, unsure: 0};
  let done = 0;
  for (const b of bounds) { const l = labels.get(keyOf(b)); if (l) { done++; n[l.label]++; } }
  $('progress').textContent = `${done} / ${bounds.length} labelled · same ${n.same} · different ${n.different} · unsure ${n.unsure}`;
}
function setCurrent(i) {
  if (!bounds.length) return;
  i = Math.max(0, Math.min(bounds.length - 1, i));
  bndEls[cur].classList.remove('current');
  cur = i;
  bndEls[cur].classList.add('current');
  bndEls[cur].scrollIntoView({block: 'center'});
}
function setLabel(i, value) {
  const b = bounds[i];
  labels.set(keyOf(b), {a_sha: b.a_sha, b_sha: b.b_sha, a_name: b.a_name, b_name: b.b_name,
                        label: value, labeled_at: new Date().toISOString()});
  refresh(bndEls[i]); updateProgress(); scheduleSave();
  if (i === cur) setCurrent(cur + 1);
}
function removeLabel(i) {
  labels.delete(keyOf(bounds[i]));
  refresh(bndEls[i]); updateProgress(); scheduleSave();
}
function nextUnlabelled(includeCurrent) {
  for (let k = includeCurrent ? 0 : 1; k <= bounds.length; k++) {
    const i = (cur + k) % bounds.length;
    if (!labels.has(keyOf(bounds[i]))) { setCurrent(i); return; }
  }
  setStatus('all boundaries are labelled', false);
}
async function toggleLabelMode(on) {
  document.body.classList.toggle('labeling', on);
  if (on && !built) {
    bounds = LD.boundaries;
    await loadLabels();
    build(); built = true;
    updateProgress();
    if (bounds.length) { bndEls[0].classList.add('current'); nextUnlabelled(true); }
    setStatus(serverMode ? 'labels are saved to labels.json after every change'
                         : 'opened as a file: labels stay in this browser until you Export', false);
  }
}
function exportLabels() {
  const blob = new Blob([JSON.stringify(serialise(), null, 1)], {type: 'application/json'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob); a.download = 'labels.json'; a.click();
  setTimeout(() => URL.revokeObjectURL(a.href), 5000);
}
function importLabels(file) {
  const reader = new FileReader();
  reader.onload = () => {
    try {
      const list = JSON.parse(reader.result);
      if (!Array.isArray(list)) throw new Error('not a list');
      const before = labels.size;
      mergeLabels(list, false);                     // imported labels win
      refreshAll(); scheduleSave();
      setStatus(`imported ${list.length} labels (${labels.size - before} new)`, false);
    } catch (e) { setStatus('import failed: ' + e.message, true); }
  };
  reader.readAsText(file);
}

document.querySelectorAll('.controls button').forEach(b => b.addEventListener('click', () => b.blur()));
if (LD && LD.boundaries && LD.boundaries.length) {
  $('labelMode').disabled = false;
  $('labelMode').addEventListener('click', () => toggleLabelMode(!document.body.classList.contains('labeling')));
  $('nextUnlabelled').addEventListener('click', () => nextUnlabelled(false));
  $('exportLabels').addEventListener('click', exportLabels);
  $('importLabels').addEventListener('click', () => $('importFile').click());
  $('importFile').addEventListener('change', e => { if (e.target.files[0]) importLabels(e.target.files[0]); e.target.value = ''; });
  $('clearLabels').addEventListener('click', e => {
    if (clearArmed) { clearTimeout(clearArmed); clearArmed = null; labels.clear(); refreshAll(); scheduleSave();
                      e.target.textContent = 'Clear labels'; return; }
    e.target.textContent = 'Clear ALL labels? click again';
    clearArmed = setTimeout(() => { clearArmed = null; e.target.textContent = 'Clear labels'; }, 3000);
  });
  $('labelView').addEventListener('click', e => {
    const img = e.target.closest('figure img');
    if (img) { show(img.closest('figure')); return; }
    const bnd = e.target.closest('.bnd');
    if (!bnd) return;
    setCurrent(+bnd.dataset.i);
    const btn = e.target.closest('button');
    if (btn) {
      btn.blur();
      const b = bounds[cur], lab = labels.get(keyOf(b));
      if (lab && lab.label === btn.dataset.l) removeLabel(cur); else setLabel(cur, btn.dataset.l);
    }
  });
  document.addEventListener('keydown', e => {
    if (!document.body.classList.contains('labeling') || lb.classList.contains('open')) return;
    if ((e.target.matches && e.target.matches('input, select, textarea')) || e.ctrlKey || e.metaKey || e.altKey) return;
    const k = e.key;
    if (k === 'ArrowRight' || k === 'ArrowDown') setCurrent(cur + 1);
    else if (k === 'ArrowLeft' || k === 'ArrowUp') setCurrent(cur - 1);
    else if (k === 's' || k === 'S') setLabel(cur, 'same');
    else if (k === 'd' || k === 'D') setLabel(cur, 'different');
    else if (k === 'u' || k === 'U') setLabel(cur, 'unsure');
    else if (k === 'Enter') { if (bounds[cur].pipeline) setLabel(cur, bounds[cur].pipeline); }
    else if (k === 'n' || k === 'N') nextUnlabelled();
    else if (k === 'Backspace' || k === 'Delete') removeLabel(cur);
    else if (k === 'Escape') toggleLabelMode(false);
    else return;
    e.preventDefault();
  });
  if (location.hash === '#label') toggleLabelMode(true);   // cull.py label opens report.html#label
}
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


def _faces_caption(photo, identities):
    """'👤2 A,B' for a photo with two faces identified as A and B; '' without identities."""
    if not identities:
        return ""
    info = identities["photos"].get(photo.get("sha256"))
    if info is None:
        return ""
    min_faces = identities.get("min_identity_faces", 1)
    known = [l for l in info["ids"] if identities["identities"][l]["n_faces"] >= min_faces]
    unknown = len(info["faces"]) - sum(1 for l in info["faces"] if l in known)
    ids = ",".join(known) if known else "–"
    if unknown:
        ids += f" +{unknown}?"
    title = (f'{info["n_faces"]} face(s); known identities: {",".join(known) or "none"}; '
             f'{unknown} face(s) of people seen fewer than {min_faces} times')
    return f'<figcaption class="faces" title="{_e(title)}">👤{info["n_faces"]} {_e(ids)}</figcaption>'


def _figure(photo, gap, sim, low_sim, boundary=False, returned=False, moved=False, identities=None):
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
        f'<figcaption>{info or "&nbsp;"}</figcaption>{_faces_caption(photo, identities)}</figure>'
    )


def _group_html(group, photos_by_id, low_sim, identities=None):
    flags = list(group["flags"])
    if group["min_similarity"] is not None and group["min_similarity"] < low_sim:
        flags.append("low similarity")
    if group["split_part"]:
        i, n = group["split_part"]
        flags = [f for f in flags if f != "split"] + [f"split {i}/{n} of {group['split_from']}"]
    labels = {"lookback": "returned to scene", "moved": "boundary adjusted",
              "faces": "joined: same people", "faces_split": "kept apart: different people"}
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
                                   group["boundary_similarity"], low_sim, boundary=True,
                                   identities=identities))
        else:
            figures.append(_figure(photo, group["consecutive_gaps_seconds"][idx - 1],
                                   group["consecutive_similarities"][idx - 1], low_sim,
                                   returned=joined_by[idx - 1] == "lookback",
                                   moved=joined_by[idx - 1] == "moved", identities=identities))
    return (
        f'<div class="group{" flagged" if flags else ""}" data-size="{group["size"]}" '
        f'data-camera="{_e(group["camera_id"])}" data-flagged="{flagged}">'
        f'<div class="ghead"><span class="gid">{group["group_id"]}</span>'
        f'<span>{group["size"]} photo{"s" if group["size"] != 1 else ""}</span>'
        f'<span class="muted">{span}</span><span class="muted">{min_sim}</span>{badges}</div>'
        f'<div class="thumbs">{"".join(figures)}</div></div>'
    )


def _segment_bar(seg):
    """Header strip for a day segment (segments.json), shown before its first group."""
    st = seg.get("stats") or {}
    n_groups = st.get("n_groups")
    span = (f"{_clock(seg['start'])} – {_clock(seg['end'])}" if seg.get("start")
            else "no capture time")
    parts = [f'<span class="sid">{_e(seg["segment_id"])}</span>', f'<span class="muted">{span}</span>',
             f'<span>{seg["n_photos"]} photos</span>']
    if n_groups is not None:
        parts.append(f'<span>{n_groups} groups</span>')
    if st.get("no_people_share") is not None:
        parts.append(f'<span class="muted">{100 * st["no_people_share"]:.0f}% no people</span>')
    if st.get("identities"):
        ids = ", ".join(f"{label} {n}" for label, n in st["identities"][:5])
        parts.append(f'<span class="muted" title="known identities: photos in this segment">👤 {_e(ids)}</span>')
    parts += [f'<span class="badge">{_e(f)}</span>' for f in seg.get("flags", [])]
    if st.get("n_groups_crossing"):
        parts.append(f'<span class="badge">{st["n_groups_crossing"]} groups cross the boundary</span>')
    parts.append(f'<a href="segments_sheets/{_e(seg["segment_id"])}.jpg">sheet</a>')
    return (f'<div class="seghead" data-camera="{_e(seg.get("camera_id") or "")}">'
            f'{"".join(parts)}</div>')


def _label_block(label_data, input_dir, low_sim):
    """JSON for the label mode, embedded in the page; '' when there is nothing to label."""
    if not label_data or not label_data.get("boundaries"):
        return ""
    payload = {"boundaries": label_data["boundaries"], "labels": label_data.get("labels") or [],
               "input_dir": str(input_dir or ""), "low_sim": low_sim}
    text = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
    return f'<script id="labelData" type="application/json">{text}</script>'


def write_report(out_dir, photos, groups_data, input_dir=None, identities=None, label_data=None,
                 segments_data=None):
    """`identities` is the content of identities.json (faces.py) or None. `label_data` is
    {boundaries: labels.boundaries(...), labels: labels.load_labels(...)} for the label mode.
    `segments_data` is the content of segments.json (segments.py) or None; with it, a
    header strip is inserted before the first group of every day segment."""
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
    faces_note = ""
    if identities:
        n_faces = sum(v["n_faces"] for v in identities["photos"].values())
        min_faces = identities.get("min_identity_faces", 1)
        n_ids = sum(1 for v in identities["identities"].values() if v["n_faces"] >= min_faces)
        stats += [("faces", n_faces), (f"identities (≥{min_faces} faces)", n_ids)]
        faces_note = (f' <b>👤</b> shows the number of faces and their identity labels '
                      f'(A = most frequent person; identity threshold {identities["threshold"]}; '
                      f'"+2?" = two faces of people seen fewer than {min_faces} times, which '
                      f'neither join nor separate groups). '
                      f'Badge <i>joined: same people</i> marks a group that face identity merged, '
                      f'<i>kept apart: different people</i> one that it kept from merging.')
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

    seg_of_group = {gid: seg for seg in (segments_data or {}).get("segments", [])
                    for gid in seg.get("group_ids", [])}
    body, last_camera, last_segment = [], None, None
    for g in groups:
        if g["camera_id"] != last_camera:
            n_groups = sum(1 for x in groups if x["camera_id"] == g["camera_id"])
            body.append(f'<h2 class="camhead" data-camera="{_e(g["camera_id"])}">Camera {_e(g["camera_id"])} '
                        f'<span class="muted">· {n_groups} groups</span></h2>')
            last_camera = g["camera_id"]
        seg = seg_of_group.get(g["group_id"])
        if seg is not None and seg["segment_id"] != last_segment:
            body.append(_segment_bar(seg))
            last_segment = seg["segment_id"]
        body.append(_group_html(g, photos_by_id, low_sim, identities))

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
<p class="muted intro">Under each thumbnail: time gap and similarity to the previous photo of the same camera.
For the first photo of a group these refer to the previous group, i.e. why the group was cut there.
<span style="color:var(--accent)">↩</span> marks a photo that joined by look-back (the photographer returned to the scene):
time since the group's last photo and similarity to its best-matching photo.
<span style="color:var(--accent)">⇄</span> marks a photo moved here from the neighbouring group because it is more similar to this group.
Similarities below {low_sim} are highlighted.{faces_note} Click a thumbnail to open the preview (←/→ to move, Esc to close).</p>
<div class="controls">
  <button id="labelMode" disabled title="label the boundaries between neighbouring photos">Label mode</button>
  <label class="gctl"><input type="checkbox" id="hideSingles"> hide single photos</label>
  <label class="gctl"><input type="checkbox" id="onlyFlagged"> only flagged groups</label>
  <label class="gctl">camera <select id="camera"><option value="">all</option>{cam_options}</select></label>
  <label>thumb size <input type="range" id="size" min="80" max="320" value="160"></label>
  <span class="muted gctl"><span id="shown"></span> groups shown</span>
  <span class="lctl">
    <b id="progress"></b>
    <button id="nextUnlabelled" title="N">next unlabelled</button>
    <button id="exportLabels">Export labels.json</button>
    <button id="importLabels">Import</button><input type="file" id="importFile" accept=".json,application/json" hidden>
    <button id="clearLabels">Clear labels</button>
    <span class="muted" id="saveStatus"></span>
  </span>
</div>
<div id="groupView">
{"".join(body)}
{problems}
</div>
<div id="labelView">
<p class="legend">Each widget is the boundary between the two neighbouring photos of one camera.
The connector shows the pipeline's decision (<span style="color:var(--ok)">━━ same group</span>,
<span style="color:var(--bad)">┅┅ different</span>); a dotted button
<span class="ex s-same">S</span> / <span class="ex s-diff">D</span> is only the pipeline's <i>suggestion</i> and is not saved.
A filled button <span class="ex chosen c-same">S</span> <span class="ex chosen c-diff">D</span> <span class="ex chosen c-unsure">U</span>
is your label; a red left edge marks a label that disagrees with the pipeline.
Keys: <b>←/→</b> move, <b>S</b> same, <b>D</b> different, <b>U</b> unsure, <b>Enter</b> accept the suggestion,
<b>N</b> next unlabelled, <b>Backspace</b> remove, <b>Esc</b> leave. Click a thumbnail for the preview.</p>
<div class="strips"></div>
</div>
{_label_block(label_data, input_dir, low_sim)}
<div id="lightbox"><img alt=""><div></div></div>
<script>{JS}</script>
</body></html>"""
    path = out_dir / REPORT_FILE
    path.write_text(page, encoding="utf-8")
    return path
