# VPS Solver Debugging Log (2026-06-11)

## Environment

- Chrome: 149.0.7827.102 (installed via `google-chrome-stable`)
- OS: Linux (Docker container, headless via Xvfb)
- Xvfb: `:100 -screen 0 1920x1080x24 -ac`
- Extension: CaptchaPlugin with WS addon (git cloned to `/opt/captchaplugin/extension/`)
- Extension ID via CDP: `mgpkeembckgdmcpnklehponnjkenjnfg`
- CDP port: 9333
- Solver API port: 8866

## Confirmed Findings

### 1. `--load-extension` Does NOT Work in Chrome 149

Started Chrome multiple times with:
```
--load-extension=/opt/captchaplugin/extension
--disable-extensions-except=/opt/captchaplugin/extension
```

Result: Extension does NOT appear in Preferences file. Only 4 built-in extensions appear (Web Store, Network Speech, PDF Viewer, Hangouts). Content scripts never inject.

Chrome stderr shows "Created TensorFlow Lite XNNPACK delegate for CPU" which means the ONNX runtime loads, but this is misleading — the extension's content scripts still don't function.

### 2. CDP `Extensions.loadUnpacked` — Partial Success

```python
await ws.send({
    "id": 1,
    "method": "Extensions.loadUnpacked",
    "params": {"path": "/opt/captchaplugin/extension"}
})
# Returns: {"result": {"id": "mgpkeembckgdmcpnklehponnjkenjnfg"}}
```

The extension registers successfully. However:
- Content scripts do NOT inject into existing pages
- Content scripts do NOT inject after `Page.reload` (with or without `ignoreCache: True`)
- Content scripts do NOT inject into new tabs created via `Target.createTarget`
- Opening the extension's popup page (`chrome-extension://{ext_id}/popup.html`) forces the SW to start, but still no content script injection on subsequent page reloads

Tested by polling `document.getElementById('g-recaptcha-response').value` for 120+ seconds — always empty. Iframes (anchor + bframe) are present but the checkbox is never auto-clicked.

### 3. One Success Case (Not Reproducible)

Early in the session, Chrome was started with `--load-extension` AND the reCAPTCHA demo URL as the initial page. After waiting ~20 seconds, the token appeared (length > 0). However, this could NOT be reproduced on subsequent Chrome restarts with identical flags. This may have been a race condition or the extension may have loaded via a different path.

### 4. `chrome.runtime.reload()` Destroys the Extension

After calling `chrome.runtime.reload()` from the extension's service worker:
- The SW target disappears from CDP targets
- It does NOT restart on its own
- Content scripts stop working entirely
- Only a full Chrome restart recovers the extension

### 5. Content Script Architecture

The extension uses two content script groups (from manifest.json):

**Group 0** (runs at `document_start`, all frames):
- `eventhook/loader.js` — Hooks native DOM APIs to intercept reCAPTCHA internals

**Group 1** (runs at `document_start`, all frames):
- `eventhook.js` — Posts messages via `postMessage({source: "captcharaptor", ...})`
- `captcha/recaptcha.js` — Main solving logic (clicks checkbox, processes image challenge)

Both match: `*://*.google.com/recaptcha/*` and `*://*.recaptcha.net/recaptcha/*`

The scripts reference `chrome.runtime.sendMessage` and `chrome.runtime.id`, so they CANNOT be injected manually via `Page.addScriptToEvaluateOnNewDocument` — they need the extension's isolated world context.

### 6. Service Worker Behavior (MV3)

The extension's SW (`background.js`) uses `importScripts()`:
- `background_sqlite.js` — SQLite WASM for hash cache
- `uploader.js` — Solve data upload
- `ws/background_ws.js` — WebSocket + CDP for remote solving

The SW only starts on-demand (MV3 spec). It does NOT appear as a CDP target until triggered (e.g., by opening the popup page). Even when the SW starts, content scripts still don't inject — the registration timing is the issue.

## Approaches NOT Yet Tested

1. **Playwright `launch_persistent_context`** — Most promising. Playwright manages Chrome startup differently and may register extensions before the first page load. Script at `/tmp/solver_playwright.py` was started but results not yet verified.

2. **Chrome Web Store install** — Installing the published extension (`hdiblbpgjngidefamjemomebmkdpddjl`) via CWS may trigger proper content script registration since Chrome treats CWS extensions as first-class.

3. **Direct WS cloud service** — Skip local extension entirely. Send solve tasks to `wss://ws.captcharaptor.com` with API key. The CaptchaPlugin cloud handles everything.

4. **Selenium ChromeDriver** — `add_extension()` method may handle the extension lifecycle differently.

## Solver Server Architecture

The solver server at `/opt/captchaplugin/solver-server.py` implements:
- 2captcha-compatible API (`/in.php`, `/res.php`)
- Connects to Chrome via CDP (port configurable)
- Creates new tabs for each solve request
- Polls for token completion
- Returns token in standard format (`OK|token_string`)

The server works end-to-end IF the extension is actually functioning in Chrome. The blocking issue is purely the extension content script injection, not the server logic.

## CDP Commands Reference

```python
# Load extension
{"method": "Extensions.loadUnpacked", "params": {"path": "/path/to/extension"}}

# List all targets (including extension workers)
{"method": "Target.getTargets"}

# Create new tab
{"method": "Target.createTarget", "params": {"url": "https://..."}}

# Navigate and wait
{"method": "Page.enable"}
{"method": "Page.navigate", "params": {"url": "https://..."}}
# Listen for Page.loadEventFired

# Reload with cache bypass
{"method": "Page.reload", "params": {"ignoreCache": True}}

# Evaluate JS in page
{"method": "Runtime.evaluate", "params": {"expression": "...", "returnByValue": True}}

# Check reCAPTCHA token
"document.getElementById('g-recaptcha-response').value.length"
```
