"""VLM client: OpenAI-compatible chat completions over the standard library.

Used by culling/judge.py (and later by the scoring step) to talk to the user's own
vLLM server (`vlm.base_url`, normally an SSH tunnel to the EC2 instance). Only the
transport lives here: request body, headers, error mapping and the server's `usage`
block. Prompts, schemas, parsing and retries belong to the caller, so that a fake
client can stand in for the server in tests.

Privacy: image bytes go into the request body as base64 and nowhere else. Logs and
exception messages carry counts, sizes, timings and the `usage` block, never the
prompt, the body or the images.
"""
import base64
import http.client
import json
import logging
import os
import re
import socket
import time
import urllib.error
import urllib.request

log = logging.getLogger(__name__)

PING_TIMEOUT = 10  # seconds; a server that is up answers /models at once
_BASE64_RUN = re.compile(r"[A-Za-z0-9+/]{48,}={0,2}")  # anything that could be image data


class VLMError(Exception):
    """One request failed: HTTP 4xx/5xx, a timeout, or a reply without content."""


class VLMUnavailable(VLMError):
    """The server cannot be reached at all (connection refused, unknown host, the SSH
    tunnel dropped the channel). Not worth retrying: the caller stops and resumes later."""


def _error_body(error):
    """First 300 characters of an HTTP error body, with anything that looks like base64
    blanked out (a validation error could echo the request)."""
    try:
        text = error.read(4000).decode("utf-8", "replace")
    except Exception:
        return ""
    return _BASE64_RUN.sub("<base64>", text)[:300]


class OpenAICompatibleClient:
    """Chat completions against vLLM or any OpenAI-compatible server.

    `cfg` is config["vlm"]. `opener(request, timeout=...)` is urllib's urlopen by
    default; tests pass a fake that returns a response-like context manager.
    """

    def __init__(self, cfg, opener=None):
        self.base_url = str(cfg["base_url"]).rstrip("/")
        self.model = cfg["model"]
        self.timeout = float(cfg["timeout_seconds"])
        self.api_key_env = cfg["api_key_env"]
        self.api_key = os.environ.get(self.api_key_env) or None
        # No proxies: urllib's default opener honours HTTP_PROXY / the system proxy, which
        # would route the pair images through a third host. They go to base_url only.
        self._open = opener or urllib.request.build_opener(urllib.request.ProxyHandler({})).open
        self.last_usage = {}  # `usage` block of the last successful ask()

    def _headers(self):
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _call(self, path, body=None, timeout=None):
        """POST `body` (a dict) or GET when body is None; returns the decoded JSON reply."""
        url = f"{self.base_url}{path}"
        data = json.dumps(body).encode("utf-8") if body is not None else None
        request = urllib.request.Request(url, data=data, headers=self._headers(),
                                         method="POST" if data is not None else "GET")
        try:
            with self._open(request, timeout=self.timeout if timeout is None else timeout) as resp:
                raw = resp.read()
        except urllib.error.HTTPError as e:
            raise VLMError(f"HTTP {e.code} from {url}: {_error_body(e)}") from None
        except urllib.error.URLError as e:
            reason = e.reason
            if isinstance(reason, (ConnectionError, socket.gaierror)):
                raise VLMUnavailable(f"cannot reach {self.base_url}: {reason}") from None
            raise VLMError(f"request to {url} failed: {reason}") from None
        except (ConnectionError, socket.gaierror) as e:
            # http.client raises these directly when the server closes the connection
            # before answering (the tunnel is up but vLLM behind it is not).
            raise VLMUnavailable(f"cannot reach {self.base_url}: {e}") from None
        except http.client.HTTPException as e:
            # Not an OSError: a reply cut short (IncompleteRead), a non-HTTP reply on the
            # port (BadStatusLine), a bad URL. Worth a retry, not an abort.
            raise VLMError(f"request to {url} failed: {type(e).__name__}: {str(e)[:200]}") from None
        except OSError as e:  # includes TimeoutError / socket.timeout on read
            raise VLMError(f"request to {url} failed: {type(e).__name__}: {e}") from None
        try:
            return json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, ValueError) as e:
            raise VLMError(f"reply from {url} is not JSON: {e}") from None

    def ask(self, prompt, images, schema, max_tokens=256, temperature=0.0, schema_name="pair_verdict"):
        """One user message: the images (JPEG bytes, as data URLs) followed by the text.
        The answer is constrained to `schema` (vLLM structured outputs, strict). Returns
        the raw content string; parsing and retries are the caller's business."""
        content = [{"type": "image_url",
                    "image_url": {"url": "data:image/jpeg;base64," + base64.b64encode(img).decode("ascii")}}
                   for img in images]
        content.append({"type": "text", "text": prompt})
        body = {
            "model": self.model,
            "messages": [{"role": "user", "content": content}],
            "max_tokens": max_tokens,
            "temperature": temperature,
            "response_format": {"type": "json_schema",
                                "json_schema": {"name": schema_name, "schema": schema, "strict": True}},
            # vLLM + Qwen3: thinking off per request (docs/research/2026-10-19-vlm-context-budget.md).
            "chat_template_kwargs": {"enable_thinking": False},
        }
        started = time.time()
        reply = self._call("/chat/completions", body)
        try:
            text = reply["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError):
            raise VLMError("reply has no choices[0].message.content") from None
        if not isinstance(text, str):
            raise VLMError(f"reply content is {type(text).__name__}, not text")
        self.last_usage = reply.get("usage") or {}
        log.info("VLM request: %d image(s), %d bytes, %.1f s, usage %s",
                 len(images), sum(len(i) for i in images), time.time() - started, self.last_usage)
        return text

    def ping(self):
        """GET /models. Returns the served model ids; raises VLMError when `self.model`
        is not among them (and VLMUnavailable when the server does not answer)."""
        reply = self._call("/models", timeout=min(self.timeout, PING_TIMEOUT))
        try:
            ids = [str(m["id"]) for m in reply["data"]]
        except (KeyError, TypeError):
            raise VLMError(f"unexpected /models reply from {self.base_url}") from None
        if self.model not in ids:
            raise VLMError(f"{self.base_url} serves {ids or 'no model'}, not {self.model}")
        return ids


def make_client(cfg):
    """The client for config["vlm"]; selected by `provider`."""
    if cfg["provider"] == "openai_compatible":
        return OpenAICompatibleClient(cfg)
    raise ValueError(f"Unknown vlm.provider '{cfg['provider']}' (only openai_compatible is implemented)")
