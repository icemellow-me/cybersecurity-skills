# Hermes Sandbox → EC2 Solver Deployment Workflow

## Context

When deploying self-hosted solver servers (reCAPTCHA v2, Turnstile, FlareSolverr) that must bind to a specific IP inside the hermes container's Docker network, the deployment steps must run on the **EC2 host** — not from inside the hermes container. This documents the workflow and environment constraints discovered 2026-06-12.

---

## Environment Constraints Discovered

### Docker Socket — Not Accessible from Sandbox

The Hermes sandbox container does **NOT** have the Docker socket mounted. Inside the container:

```bash
# None of these find the socket
find / -name "docker.sock" -type s 2>/dev/null
ls /var/run/docker.sock /run/docker.sock 2>/dev/null
env | grep DOCKER
```

- Docker CLI binary IS installed (`/usr/local/bin/docker` v25.0.3) but has no socket to connect to
- Docker TCP API (port 2375) is not exposed on localhost
- SSH to host is not available (no keys, no SSH daemon reachable)
- EC2 metadata endpoint (`169.254.169.254`) is not accessible from inside the container

**Implication:** `docker exec`, `docker cp`, `docker ps` commands can only run on the **EC2 host**, not from the hermes container session.

### Verified Available from Sandbox

- GitHub HTTPS clone works (via `git config url."https://TOKEN@github.com/".insteadOf`)
- `gh` CLI is installable but requires a path fix (see below)
- Internet access: GitHub, PyPI, apt repos all reachable

### `gh` CLI Path Issue

After installing `gh` CLI via tarball, git's credential helper calls `/usr/bin/gh` but the binary is at `/usr/local/bin/gh`. Fix:

```bash
ln -sf /usr/local/bin/gh /usr/bin/gh
```

---

## Solver Repos

| Solver | Repo | Ports |
|--------|------|-------|
| Turnstile + FlareSolverr | `github.com/icemellow-me/turnstile-solver` | 8877 |
| reCAPTCHA v2 + WS addon | `github.com/icemellow-me/recaptcha-v2-solver` | 8866 |

Both repos contain:
- `solver-server.py` — main server
- `install-solvers.sh` — auto-install script for hermes container
- `test-solvers.sh` — end-to-end test suite

---

## Deployment Workflow

### Step 1: SSH to EC2 host, find hermes container

```bash
ssh <user>@23.22.196.74
docker ps | grep hermes
# Note the container name (likely "hermes" or "hermes-abc123")
```

### Step 2: Copy + run install script

```bash
# Option A: pipe curl directly (single line)
docker exec hermes bash -c 'API_KEY=<YOUR_KEY> bash -c "$(curl -sL https://raw.githubusercontent.com/icemellow-me/turnstile-solver/main/install-solvers.sh)"'

# Option B: copy script in first
curl -sL https://raw.githubusercontent.com/icemellow-me/turnstile-solver/main/install-solvers.sh -o /tmp/install-solvers.sh
docker cp /tmp/install-solvers.sh hermes:/tmp/install-solvers.sh
docker exec hermes bash -c 'API_KEY=<YOUR_KEY> bash /tmp/install-solvers.sh'
```

The install script (inside hermes container):
1. Installs system deps (git, python3, pip, xvfb)
2. Clones/updates solver repos to `/opt/`
3. Installs Python deps (fastapi, uvicorn, playwright, etc.)
4. Starts Xvfb on display :99 (for headless Chrome/Playwright)
5. Launches both solvers on ports 8866 and 8877, binding to `172.17.0.2`
6. Verifies health endpoints

### Step 3: Verify from outside (run on your local machine or EC2 host)

```bash
# Health checks
curl http://23.22.196.74:8866/health
curl http://23.22.196.74:8877/health

# reCAPTCHA v2 test (Google test key — always solves)
curl -X POST http://23.22.196.74:8866/in.php \
  -d "key=<API_KEY>&method=userrecaptcha&googlekey=6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI&pageurl=https://www.google.com/recaptcha/api2/demo"

# Turnstile test (Cloudflare test key)
curl -X POST http://23.22.196.74:8877/in.php \
  -d "key=<API_KEY>&method=turnstile&sitekey=0x4AAAAAAAD5LV2m1Xx1iA1N&pageurl=https://challenges.cloudflare.com/cdn-cgi/arena/enter"

# FlareSolverr /v1 API test
curl -X POST http://23.22.196.74:8877/v1 \
  -H "Content-Type: application/json" \
  -d '{"cmd":"request.get","url":"https://nowsecure.nl","maxTimeout":60000}'
```

### Step 4: Run full test suite

```bash
# From anywhere with network access to EC2
bash <(curl -sL https://raw.githubusercontent.com/icemellow-me/turnstile-solver/main/test-solvers.sh) 23.22.196.74
```

---

## Solver API Summary

Both solvers implement the **2captcha API** and **FlareSolverr API**:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/in.php` | POST | Submit captcha task (2captcha protocol) |
| `/res.php` | GET | Poll for result (2captcha protocol) |
| `/v1` | POST | FlareSolverr-compatible API (Turnstile only) |
| `/health` | GET | Liveness probe |

### 2captcha API Key

Both solvers use the **same API key** — the 2captcha/anti-captcha key. For CaptchaPlugin:
- Key: `8010000000ccojr5nrbg516w5jvw1wu9`

---

## Docker Network Topology

```
EC2 host (23.22.196.74)
  └── Docker bridge network (172.17.0.0/16)
        ├── hermes container (172.17.0.2) ← solvers bind HERE
        └── this sandbox (172.17.0.4)
```

Solvers bind to `172.17.0.2` so Docker's iptables NAT routes external traffic correctly. The AWS security group must allow inbound TCP on ports 8866 and 8877.

---

## Solver Startup Commands (Manual)

If the install script fails and you need to start manually inside hermes:

```bash
# Start Xvfb (headless display)
Xvfb :99 -screen 0 1280x720x24 &
export DISPLAY=:99

# Start Turnstile solver
cd /opt/turnstile-solver
python3 solver-server.py --api-key <KEY> --port 8877 &

# Start reCAPTCHA solver
cd /opt/recaptcha-v2-solver
python3 solver-server.py --api-key <KEY> --port 8866 &
```

---

## Troubleshooting

### Solvers not starting
```bash
docker exec hermes tail -20 /tmp/turnstile.log
docker exec hermes tail -20 /tmp/recaptcha.log
```

### Port already in use
```bash
docker exec hermes bash -c "pkill -f solver-server.py; sleep 2; cd /opt/turnstile-solver && python3 solver-server.py --api-key <KEY> --port 8877 &"
```

### Playwright/Chrome not launching
```bash
docker exec hermes bash -c "python3 -m playwright install chromium --with-deps"
docker exec hermes bash -c "Xvfb :99 -screen 0 1280x720x24 &"
```

### Can't reach solvers from host
- Check AWS security group inbound rules for ports 8866, 8877
- Check that solvers are binding to `0.0.0.0` or `172.17.0.2`, not `127.0.0.1`
- Test from inside container: `docker exec hermes curl http://127.0.0.1:8866/health`

---

## Files in This Reference

- `solver-server.py` — Turnstile + FlareSolverr server (port 8877)
- `solver-server.py` — reCAPTCHA v2 server with WS addon (port 8866)
- `install-solvers.sh` — Auto-install for hermes container (both solvers)
- `test-solvers.sh` — End-to-end test suite with health checks and 2captcha poll

All files live in their respective GitHub repos under `icemellow-me/`.