---
name: self-hosted-captcha-solvers
version: 2.0
description: Self-hosted captcha solving infrastructure — reCAPTCHA v2, Cloudflare Turnstile, image/OCR captchas, hCaptcha, coordinate captchas. 2captcha-compatible API servers on VPS.
triggers:
  - captcha solving
  - captcha solver
  - recaptcha solver
  - turnstile solver
  - hcaptcha solver
  - image captcha OCR
  - captcha API server
  - 2captcha compatible
  - anti-captcha
---

# Self-Hosted Captcha Solvers

Build and operate self-hosted captcha solving servers with 2captcha-compatible HTTP APIs.

## Architecture

```
                    ┌──────────────────────────┐
                    │  Universal Solver (:8855) │
                    │  ddddocr + Tesseract +    │
                    │  hcaptcha-challenger      │──► Image/OCR, hCaptcha, Coord
                    │  Upstream forwarder       │──► Turnstile (:8877)
                    │                           │──► reCAPTCHA v2 (:8866)
                    └──────────────────────────┘
```

Three servers, three ports:
- **Port 8855** — Universal solver (image OCR + hCaptcha + forwarding hub)
- **Port 8866** — reCAPTCHA v2 solver (Playwright + CaptchaPlugin extension)
- **Port 8877** — Turnstile solver (Playwright + headless Chromium)

## Server Details

### Universal Solver (port 8855)
- **Repo:** `icemellow-me/universal-captcha-solver`
- **Engines:** ddddocr (ONNX OCR+detection), Tesseract OCR, hcaptcha-challenger (ONNX + Gemini LLM)
- **API:** 2captcha-compatible (`POST /in.php`, `GET /res.php`) + direct JSON (`POST /solve`) + health (`GET /health`)
- **Methods:** `image`, `base64`, `userrecaptcha`, `turnstile`, `hcaptcha`, `coord`
- **Start:** `python3 solver-server.py --api-key KEY --port 8855 [--gemini-key GEMINI_KEY]`
- **Deps:** `ddddocr pytesseract aiohttp pillow hcaptcha-challenger tesseract-ocr`

### reCAPTCHA v2 Solver (port 8866)
- **Repo:** `icemellow-me/recaptcha-v2-solver`
- **Engine:** Playwright `launch_persistent_context()` with CaptchaPlugin extension loaded
- **API:** 2captcha-compatible
- **Start:** `DISPLAY=:99 python3 recaptcha-playwright-server.py --port 8866 --api-key KEY`
- **Key insight:** MV3 content scripts need Chrome's extension system to register match patterns BEFORE page load. `--load-extension` flag is unreliable for iframe injection. Use `launch_persistent_context` with extension pre-loaded.

### Turnstile Solver (port 8877)
- **Repo:** `icemellow-me/turnstile-solver`
- **Engine:** Playwright `launch_persistent_context()` with system Chromium
- **API:** 2captcha-compatible + FlareSolverr-compatible
- **Start:** `DISPLAY=:99 python3 solver-server.py --api-key KEY --port 8877 --no-headless`
- **Non-interactive Turnstile:** Works reliably (~730-char tokens)
- **Managed/interactive Turnstile:** Extension assistance needed (Cloudflare 400020 detection)

## Process Management — CRITICAL SAFETY RULE

**NEVER use `pkill -f solver-server.py`** — it kills ALL solver processes across all three servers.

### Safe kill commands (use exact path substrings)
```bash
pkill -f "universal-captcha-solver/solver-server"    # Universal only
pkill -f "turnstile-solver/solver-server"             # Turnstile only
pkill -f "recaptcha-v2-solver/recaptcha-playwright-server"  # reCAPTCHA only
```

### Or use specific PIDs
```bash
# Find PIDs
ps aux | grep -E "solver-server|recaptcha-playwright" | grep -v grep

# Kill by PID
kill <PID>
```

### Restart sequence
1. Kill the specific server process (using safe commands above)
2. Wait 2 seconds
3. Optionally clean stale browser profiles: `rm -rf /tmp/captcha-browser-profile/`
4. Start server: `docker exec -d hermes bash -c 'cd /path && DISPLAY=:99 python3 server.py --api-key KEY --port PORT >> /tmp/log 2>&1'`
5. Wait 10-15s for Playwright browser init
6. Health check: `curl -sf http://127.0.0.1:PORT/health`

## 2captcha-Compatible API

### Submit: `POST /in.php`
| Param | Type | Description |
|-------|------|-------------|
| `key` | string | API key |
| `method` | string | `image`, `base64`, `userrecaptcha`, `turnstile`, `hcaptcha`, `coord` |
| `file` | file | Image file (for `image` method) |
| `body` | string | Base64 image (for `base64` method) |
| `sitekey` / `googlekey` | string | Site key for token captchas |
| `pageurl` | string | Page URL for token captchas |
| `version` | string | `v2` (default) or `v3` (reCAPTCHA) |

Response: `OK|<task_id>` or `ERROR|<message>`

### Poll: `GET /res.php?key=KEY&id=TASK_ID`
- `OK|<solution>` — solved
- `CAPCHA_NOT_READY` — still processing
- `ERROR|<message>` — failed

### Direct JSON: `POST /solve`
```json
{"type": "image", "image_base64": "<b64>"}
{"type": "turnstile", "sitekey": "...", "pageurl": "..."}
```
Returns: `{"status": "solved", "solution": "...", "solve_time": 1.33}`

## Captcha-Specific Notes

### Image/OCR Captchas
- ddddocr (primary): ONNX-based, ~0.02s, handles noise/warping well
- Tesseract (fallback): slower but handles different fonts
- For best results, images should be at least 200x80px with legible text
- Both engines fire in parallel and the better result wins

### hCaptcha
- Requires `--gemini-key` (Google Gemini API key) for LLM-based challenge solving
- Uses `hcaptcha-challenger` library with ONNX models (ResNet, YOLOv8)
- Pass `method=hcaptcha` with `sitekey` + `pageurl`
- Without Gemini key, engine loads but returns `GEMINI_API_KEY required`

### reCAPTCHA v2
- Uses CaptchaPlugin ONNX models via browser extension
- Takes ~60-100s per solve (browser interaction time)
- Browser sessions go stale after extended idle — restart if `Target page, context or browser has been closed` errors appear
- CaptchaPlugin API key: stored in user memory

### Turnstile
- Non-interactive (always-on) turnstile tokens solve in ~10s
- Managed/interactive turnstile may fail with Cloudflare 400020 detection
- Tokens are ~730 chars, start with version prefix like `1.`

### Coordinate/Click Captchas
- ddddocr detection mode finds object positions in images
- Returns coordinate string like `x1,y1;x2,y2`
- Use `method=coord`

## Forwarding Architecture

The universal solver can forward to dedicated solvers:
```bash
export RECAPTCHA_SOLVER_URL=http://127.0.0.1:8866
export TURNSTILE_SOLVER_URL=http://127.0.0.1:8877
```

When it receives `method=userrecaptcha` or `method=turnstile`, it HTTP-forwards the request to the respective upstream solver, polls the result, and returns it to the caller. This gives users a single API endpoint for all captcha types.

## Docker Container Notes

- Servers run inside `hermes` docker container (ID: `3ac017e1f59`)
- `docker exec hermes` from EC2 host, NOT from inside the container
- Python3 paths: `/opt/hermes/.venv/bin/python3` (venv), `/usr/bin/python3` (system)
- For pip inside venv: `/opt/hermes/.venv/bin/pip3 install ...`
- System pip: `pip install --break-system-packages ...`
- Display: `DISPLAY=:99` (Xvfb) needed for Playwright
- CaptchaPlugin API key: `8010000000ccojr5nrbg516w5jvw1wu9`

## Pitfalls

1. **pkill cross-contamination** — `pkill -f solver-server.py` kills ALL servers, not just one. Always use exact path substrings or specific PIDs.
2. **Stale browser contexts** — Playwright browser contexts crash after long idle periods. If you see `Target page, context or browser has been closed`, restart the affected server only.
3. **hcaptcha-challenger import changes** — The library's API changes between versions. `ZeroShotAgent` was removed in recent versions; only `AgentV` is stable. Always guard imports with try/except.
4. **aiohttp file upload** — `request.post()` returns `MultiDictProxy` where file fields are `FileField` objects. Use `file_field = post["file"]; data = file_field.read()` (not `open()` or `hasattr(file, "read")`).
5. **GET /in.php** — Never register GET and POST on the same handler for `/in.php`. GET can't parse multipart body and will crash if the handler calls `await request.post()`.
6. **Tesseract empty results** — Small/default PIL fonts produce tiny text that OCR can't read. Use TrueType fonts at 40+ pt for test captcha generation.
7. **Chrome `--load-extension` unreliability** — MV3 content scripts don't inject into iframes when loaded via CLI flag. Use Playwright `launch_persistent_context()` instead.

## See Also
- `references/captcha-research.md` — GitHub research notes on captcha solving tools and approaches
- `references/server-ports-and-repos.md` — Port assignments, repo URLs, and quick-start commands
