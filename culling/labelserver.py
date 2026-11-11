"""Small local server for labelling in the browser (`python cull.py label`).

Serves the output folder (report.html, thumbs/, previews/) on 127.0.0.1 and accepts
POST /labels, which writes labels.json. Standard library only.
"""
import json
import logging
import threading
import webbrowser
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

from culling.labels import load_labels, normalise_labels, save_labels

log = logging.getLogger(__name__)

MAX_BODY = 20 * 1024 * 1024
SAVE_LOCK = threading.Lock()   # ThreadingHTTPServer: one labels.json write at a time


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
        if self.path.split("?")[0] == "/labels":
            self._json(200, load_labels(self.out_dir))
            return
        super().do_GET()

    def do_POST(self):
        if self.path.split("?")[0] != "/labels":
            self._json(404, {"error": "not found"})
            return
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            length = -1
        if length < 0 or length > MAX_BODY:
            self._json(413, {"error": "body too large or missing Content-Length"})
            return
        try:
            labels = normalise_labels(json.loads(self.rfile.read(length).decode("utf-8")))
        except (ValueError, UnicodeDecodeError) as exc:
            self._json(400, {"error": str(exc)})
            return
        with SAVE_LOCK:
            save_labels(self.out_dir, labels)
        log.info("labels.json: %d labels saved", len(labels))
        self._json(200, {"saved": len(labels)})


def make_server(out_dir, port=0):
    """ThreadingHTTPServer bound to 127.0.0.1; port 0 picks a free one."""
    return ThreadingHTTPServer(("127.0.0.1", port), partial(LabelHandler, out_dir=out_dir))


def serve(out_dir, port=8765, open_browser=True):
    server = make_server(out_dir, port)
    url = f"http://127.0.0.1:{server.server_address[1]}/report.html#label"
    log.info("Labelling at %s  (Ctrl-C to stop; labels are saved to labels.json after every change)", url)
    if open_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log.info("Label server stopped")
    finally:
        server.server_close()
