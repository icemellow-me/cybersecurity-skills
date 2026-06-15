#!/usr/bin/env python3
"""
CaptchaPlugin reCAPTCHA Solver API Server (2captcha-compatible)
================================================================
Persistent API server that connects to an already-running Chrome instance
with the CaptchaPlugin extension loaded via CDP.

Endpoints:
  POST /in.php   — Submit a task (params: key, method, googlekey, pageurl)
  GET  /res.php  — Poll for result (params: key, action=get, id=<task_id>)
  GET  /health   — Health check

Usage:
  python3 solver-server.py --api-key YOUR_KEY --port 8866 --cdp-port 9333

Requirements:
  - Chrome running with CaptchaPlugin extension (see skill for setup)
  - CDP enabled on --cdp-port
  - Python 3.8+ with websockets package

Install deps:
  pip install websockets

Note: The extension MUST be properly loaded and content scripts MUST be
injecting for this server to work. See recaptcha-solver skill pitfalls.
"""

import asyncio
import hashlib
import json
import logging
import time
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import websockets

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
API_KEY = ""
CDP_PORT = 9333
SOLVE_TIMEOUT = 180  # seconds
POLL_INTERVAL = 5    # seconds

# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------
tasks = {}  # task_id -> {status, token, created_at, page_url, sitekey}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("solver")


# ---------------------------------------------------------------------------
# CDP helpers
# ---------------------------------------------------------------------------
async def cdp_send(ws, method, params=None, msg_id=1):
    """Send a CDP command and return the response."""
    cmd = {"id": msg_id, "method": method}
    if params:
        cmd["params"] = params
    await ws.send(json.dumps(cmd))
    while True:
        resp = await asyncio.wait_for(ws.recv(), timeout=30)
        data = json.loads(resp)
        if data.get("id") == msg_id:
            return data


async def get_page_ws(cdp_port, url_contains=None):
    """Find a page target and return its WebSocket URL."""
    resp = urllib.request.urlopen(f"http://localhost:{cdp_port}/json")
    targets = json.loads(resp.read())
    for t in targets:
        if t.get("type") == "page":
            if url_contains is None or url_contains in (t.get("url") or ""):
                return t["webSocketDebuggerUrl"]
    return None


async def create_tab(cdp_port, url):
    """Create a new browser tab and return its WebSocket URL."""
    resp = urllib.request.urlopen(f"http://localhost:{cdp_port}/json/version")
    vi = json.loads(resp.read())
    browser_ws = vi["webSocketDebuggerUrl"]

    async with websockets.connect(browser_ws, max_size=10*1024*1024) as ws:
        result = await cdp_send(ws, "Target.createTarget", {"url": url}, msg_id=1)
        target_id = result.get("result", {}).get("targetId")

    # Wait for the new target to appear
    await asyncio.sleep(2)
    resp = urllib.request.urlopen(f"http://localhost:{cdp_port}/json")
    targets = json.loads(resp.read())
    for t in targets:
        if t.get("type") == "page" and url in (t.get("url") or ""):
            return t["webSocketDebuggerUrl"], target_id
    return None, target_id


async def check_token(cdp_port, page_ws_url):
    """Check if the reCAPTCHA token is available on the page."""
    async with websockets.connect(page_ws_url, max_size=10*1024*1024) as ws:
        result = await cdp_send(ws, "Runtime.evaluate", {
            "expression": """
                (() => {
                    const el = document.getElementById('g-recaptcha-response');
                    if (el && el.value && el.value.length > 10)
                        return JSON.stringify({solved: true, token: el.value});
                    const tas = document.querySelectorAll('textarea[name="g-recaptcha-response"]');
                    for (const ta of tas) {
                        if (ta.value && ta.value.length > 10)
                            return JSON.stringify({solved: true, token: ta.value});
                    }
                    return JSON.stringify({solved: false});
                })()
            """,
            "returnByValue": True,
        }, msg_id=100)
        val_str = result.get("result", {}).get("result", {}).get("value", "{}")
        try:
            return json.loads(val_str)
        except json.JSONDecodeError:
            return {"solved": False}


# ---------------------------------------------------------------------------
# Solver
# ---------------------------------------------------------------------------
async def solve_recaptcha(cdp_port, page_url, sitekey=None, timeout=SOLVE_TIMEOUT):
    """Navigate to a page with reCAPTCHA and wait for the extension to solve it."""
    page_ws, tab_id = await create_tab(cdp_port, page_url)
    if not page_ws:
        return None

    start = time.time()
    while time.time() - start < timeout:
        await asyncio.sleep(POLL_INTERVAL)
        try:
            result = await check_token(cdp_port, page_ws)
            if result.get("solved"):
                return result.get("token")
        except Exception as e:
            log.warning(f"Token check error: {e}")

    return None


# ---------------------------------------------------------------------------
# Background solver loop
# ---------------------------------------------------------------------------
async def solver_loop():
    """Process tasks from the queue."""
    while True:
        for task_id, task in list(tasks.items()):
            if task["status"] == "processing":
                token = await solve_recaptcha(CDP_PORT, task["page_url"], task.get("sitekey"))
                if token:
                    task["status"] = "ready"
                    task["token"] = token
                else:
                    task["status"] = "failed"
                    task["token"] = None
        await asyncio.sleep(1)


# ---------------------------------------------------------------------------
# HTTP handler (2captcha-compatible)
# ---------------------------------------------------------------------------
class SolverHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        log.info(format % args)

    def _respond(self, code, body):
        self.send_response(code)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(body.encode())

    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        if parsed.path == "/health":
            self._respond(200, json.dumps({"status": "ok", "tasks": len(tasks)}))
            return

        if parsed.path == "/res.php":
            key = params.get("key", [""])[0]
            action = params.get("action", [""])[0]
            task_id = params.get("id", [""])[0]

            if key != API_KEY:
                self._respond(403, "ERROR_WRONG_KEY")
                return
            if action != "get":
                self._respond(400, "ERROR_INVALID_ACTION")
                return

            task = tasks.get(task_id)
            if not task:
                self._respond(400, "ERROR_NO_TASK")
                return

            if task["status"] == "processing":
                self._respond(200, "CAPCHA_NOT_READY")
            elif task["status"] == "ready":
                self._respond(200, f"OK|{task['token']}")
                del tasks[task_id]
            elif task["status"] == "failed":
                self._respond(200, "ERROR_CAPTCHA_UNSOLVABLE")
                del tasks[task_id]
            return

        self._respond(404, "NOT_FOUND")

    def do_POST(self):
        parsed = urlparse(self.path)
        content_len = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_len).decode() if content_len else ""
        params = parse_qs(body)

        if parsed.path == "/in.php":
            key = params.get("key", [""])[0]
            method = params.get("method", [""])[0]
            googlekey = params.get("googlekey", [""])[0]
            pageurl = params.get("pageurl", [""])[0]

            if key != API_KEY:
                self._respond(403, "ERROR_WRONG_KEY")
                return
            if method != "userrecaptcha":
                self._respond(400, "ERROR_INVALID_METHOD")
                return

            task_id = hashlib.md5(f"{pageurl}{googlekey}{time.time()}".encode()).hexdigest()[:12]
            tasks[task_id] = {
                "status": "processing",
                "page_url": pageurl,
                "sitekey": googlekey,
                "created_at": time.time(),
            }

            log.info(f"New task {task_id}: {pageurl} sitekey={googlekey}")
            self._respond(200, f"OK|{task_id}")
            return

        self._respond(404, "NOT_FOUND")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
async def main():
    global API_KEY, CDP_PORT

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-key", required=True)
    parser.add_argument("--port", type=int, default=8866)
    parser.add_argument("--cdp-port", type=int, default=9333)
    args = parser.parse_args()

    API_KEY = args.api_key
    CDP_PORT = args.cdp_port

    # Start solver loop
    asyncio.create_task(solver_loop())

    # Start HTTP server (run in thread)
    server = HTTPServer(("0.0.0.0", args.port), SolverHandler)
    log.info(f"Solver API listening on :{args.port} (CDP port {CDP_PORT})")

    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, server.serve_forever)


if __name__ == "__main__":
    asyncio.run(main())
