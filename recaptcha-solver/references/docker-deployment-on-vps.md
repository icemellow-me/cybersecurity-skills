---
name: docker-container-debugging
description: Debug Python/Docker setups on remote VPS (EC2) — probe paths before running commands, common failure patterns, solver deployment workflow for icemellow-me CAPTCHA solvers.
triggers:
  - docker exec failing path
  - No module named X in container
  - pip binary not found in container
  - installing python packages in docker container
  - setting up solvers on VPS
---

# Docker Container Debugging Workflow

## Core Rule
> **ALWAYS probe actual paths before running install/start commands inside a Docker container.**

When running `docker exec` commands on a remote container:
1. First probe what actually exists inside the container
2. Then use those discovered paths
3. Then verify the result

Never assume `/opt/some/.venv/bin/pip` or `/usr/bin/python3` without checking first.

---

## Standard Probe Sequence

Run these before ANY install or start command:

```bash
# Find Python and pip
docker exec <container> which python3 pip pip3 2>/dev/null

# Check Python version
docker exec <container> python3 --version

# List venv bins (if venv exists)
docker exec <container> ls /opt/hermes/.venv/bin/ 2>/dev/null | head -20

# List top-level app dir
docker exec <container> ls /opt/hermes/ 2>/dev/null
```

---

## Common Failure Patterns

### `No module named playwright` — wrong Python
**Symptom:** Package installed but `import playwright` fails.
**Cause:** `/opt/hermes/.venv/bin/pip` used but app runs with a different Python.
**Fix:**
```bash
# Probe first
docker exec hermes which python3 pip3
# Install using python3 -m pip (always works if python3 works)
docker exec hermes python3 -m pip install playwright
```

### `stat /opt/hermes/.venv/bin/pip: no such file`
**Symptom:** venv pip binary doesn't exist at expected path.
**Cause:** venv structure different from documentation; pip is pip3 inside venv.
**Fix:** Use `python3 -m pip` instead of direct pip path.

### `pip: command not found`
**Symptom:** pip not in PATH.
**Fix:** `python3 -m pip` — guaranteed to work with any Python install.

---

## Solver Deployment Workflow (icemellow-me solvers)

**Prerequisites:**
- EC2 host shell access (ubuntu user)
- Container name: `hermes`
- Repos (public): `icemellow-me/turnstile-solver`, `icemellow-me/recaptcha-v2-solver`

### Step 1 — Probe paths
```bash
docker exec hermes which python3 pip pip3
```

### Step 2 — Clone repos (if not present)
```bash
docker exec hermes bash -c "cd /opt && git clone -q https://github.com/icemellow-me/turnstile-solver.git 2>/dev/null || true"
docker exec hermes bash -c "cd /opt && git clone -q https://github.com/icemellow-me/recaptcha-v2-solver.git 2>/dev/null || true"
```

### Step 3 — Install Python deps
```bash
# Use python3 -m pip (not direct pip path)
docker exec hermes python3 -m pip install --break-system-packages fastapi uvicorn websockets pydantic httpx playwright 2>/dev/null
docker exec hermes python3 -m playwright install chromium 2>&1 | tail -3
```

### Step 4 — Start Xvfb + solvers
```bash
# Kill old instances
docker exec hermes bash -c 'pkill -f solver-server.py 2>/dev/null || true; pkill Xvfb 2>/dev/null || true; sleep 2'

# Start Xvfb
docker exec hermes bash -c 'Xvfb :99 -screen 0 1280x720x24 &'
sleep 2

# Start Turnstile (port 8877)
docker exec hermes bash -c 'export DISPLAY=:99; cd /opt/turnstile-solver && nohup python3 solver-server.py --api-key <KEY> --port 8877 >/tmp/turnstile.log 2>&1 &'

# Start reCAPTCHA (port 8866)
docker exec hermes bash -c 'export DISPLAY=:99; cd /opt/recaptcha-v2-solver && nohup python3 solver-server.py --api-key <KEY> --port 8866 >/tmp/recaptcha.log 2>&1 &'
```

### Step 5 — Verify
```bash
sleep 8
docker exec hermes curl -sf http://127.0.0.1:8866/health && echo " reCAPTCHA: OK"
docker exec hermes curl -sf http://127.0.0.1:8877/health && echo " Turnstile: OK"
```

### Step 6 — External test (from anywhere)
```bash
curl -X POST http://<EC2_IP>:8866/in.php \
  -d "key=<API_KEY>&method=userrecaptcha&googlekey=6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI&pageurl=https://www.google.com/recaptcha/api2/demo"

curl -X POST http://<EC2_IP>:8877/in.php \
  -d "key=<API_KEY>&method=turnstile&sitekey=0x4AAAAAAAD5LV2m1Xx1iA1N&pageurl=https://challenges.cloudflare.com/cdn-cgi/arena/enter"
```

---

## Quick Reference

| Item | Value |
|------|-------|
| EC2 IP | 23.22.196.74 |
| Container | hermes |
| reCAPTCHA port | 8866 |
| Turnstile port | 8877 |
| venv Python | `/opt/hermes/.venv/bin/python3` |
| playwright install | `python3 -m pip install playwright` |
| reCAPTCHA test key | `6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI` |
| Turnstile test key | `0x4AAAAAAAD5LV2m1Xx1iA1N` |

---

## When Stuck — Diagnostic Checklist

1. `docker ps` — is the container running?
2. `docker exec <c> which python3` — does Python exist?
3. `docker exec <c> python3 --version` — which Python version?
4. `docker exec <c> ls /opt/` — does the expected app dir exist?
5. `docker exec <c> python3 -m pip list` — is the package installed?
6. `docker exec <c> cat /tmp/turnstile.log` — any error output?