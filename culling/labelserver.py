"""Small local server for labelling in the browser (`python cull.py label`).

Serves the output folder (report.html, picks.html, thumbs/, previews/) on 127.0.0.1 and
accepts POST /labels (writes labels.json) and POST /picks (writes picks.json, the "best
photo" ground truth of `python cull.py pick`). Standard library only.
"""
import json
import logging
import threading
import webbrowser
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

from culling.labels import load_labels, normalise_labels, save_labels
from culling.picks import load_picks, normalise_picks, save_picks

log = logging.getLogger(__name__)

MAX_BODY = 20 * 1024 * 1024
SAVE_LOCK = threading.Lock()   # ThreadingHTTPServer: one file write at a time
# path -> (load, normalise, save, file name)
STORES = {"/labels": (load_labels, normalise_labels, save_labels, "labels.json"),
          "/picks": (load_picks, normalise_picks, save_picks, "picks.json")}


class LabelHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, out_dir, **kwargs):
        self.out_dir = out_dir
        super().__init__(*args, directory=str(out_dir), **kwargs)

    def log_message(self, fmt, *args):
        log.debug("%s " + fmt, self.address_string(), *args)

    def _json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        store = STORES.get(self.path.split("?")[0])
        if store:
            self._json(200, store[0](self.out_dir))
            return
        super().do_GET()

    def do_POST(self):
        store = STORES.get(self.path.split("?")[0])
        if store is None:
            self._json(404, {"error": "not found"})
            return
        _, normalise, save, name = store
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            length = -1
        if length < 0 or length > MAX_BODY:
            self._json(413, {"error": "body too large or missing Content-Length"})
            return
        try:
            data = normalise(json.loads(self.rfile.read(length).decode("utf-8")))
        except (ValueError, UnicodeDecodeError) as exc:
            self._json(400, {"error": str(exc)})
            return
        with SAVE_LOCK:
            save(self.out_dir, data)
        log.info("%s: %d entries saved", name, len(data))
        self._json(200, {"saved": len(data)})


def make_server(out_dir, port=0):
    """ThreadingHTTPServer bound to 127.0.0.1; port 0 picks a free one."""
    return ThreadingHTTPServer(("127.0.0.1", port), partial(LabelHandler, out_dir=out_dir))


def serve(out_dir, port=8765, open_browser=True, page="report.html#label"):
    server = make_server(out_dir, port)
    url = f"http://127.0.0.1:{server.server_address[1]}/{page}"
    log.info("Open %s  (Ctrl-C to stop; every change is saved at once)", url)
    if open_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log.info("Label server stopped")
    finally:
        server.server_close()
