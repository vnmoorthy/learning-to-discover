"""Tiny HTTP front for the referee so a server running elsewhere (the GPU box) can use the Claude CLI on this laptop.

  python3 -m ltd.referee_service            # listens on 127.0.0.1:8899
  ssh -R 8899:127.0.0.1:8899 <box>          # the box then sets LTD_REFEREE_URL=http://127.0.0.1:8899/review
Only localhost binds; the reverse tunnel is the only way in.
"""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from . import referee


class H(BaseHTTPRequestHandler):
    def do_POST(self):  # noqa: N802
        if self.path != "/review":
            self.send_error(404); return
        n = int(self.headers.get("Content-Length") or 0)
        try:
            body = json.loads(self.rfile.read(n) or b"{}")
            out = referee.review(body.get("state") or {}, body.get("decisions") or [])
            data = json.dumps(out).encode()
            self.send_response(200)
        except Exception as e:  # noqa: BLE001
            data = json.dumps({"error": f"{type(e).__name__}: {e}"}).encode()
            self.send_response(500)
        self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(data)))
        self.end_headers(); self.wfile.write(data)

    def log_message(self, *a):  # quiet
        pass


if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", 8899), H).serve_forever()
