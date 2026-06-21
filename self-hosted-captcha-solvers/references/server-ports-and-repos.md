# Server Ports, Repos, and Quick-Start Commands

## Port Assignments

| Port | Server | Repo | Protocol |
|------|--------|------|----------|
| 8855 | Universal Captcha Solver | `icemellow-me/universal-captcha-solver` | 2captcha + JSON |
| 8844 | Universal (ext) | `icemellow-me/universal-captcha-solver` | 2captcha + JSON (json=1) |
| 8866 | reCAPTCHA v2 Solver | `icemellow-me/recaptcha-v2-solver` | 2captcha |
| 8833 | reCAPTCHA v2 (ext) | `icemellow-me/recaptcha-v2-solver` | 2captcha (json=1) |
| 8877 | Turnstile Solver | `icemellow-me/turnstile-solver` | 2captcha + FlareSolverr |
| 8822 | Turnstile (ext) | `icemellow-me/turnstile-solver` | 2captcha (json=1) |
| 8899 | xCaptcha Solver | `icemellow-me/xcaptcha-research` | 2captcha |
| 8888 | Proxy Catalog | `icemellow-me/proxy-catalog` | REST API |
| 8000 | Puter Gateway | `icemellow-me/puter-gateway` | OpenAI SSE |
| 3000 | Open WebUI | — | Web UI |
| 8642 | Hermes Agent | — | Agent API |

## GitHub Repos (All Public)
- https://github.com/icemellow-me/universal-captcha-solver
- https://github.com/icemellow-me/recaptcha-v2-solver
- https://github.com/icemellow-me/turnstile-solver
- https://github.com/icemellow-me/xcaptcha-research
- https://github.com/icemellow-me/captcha-solver-extension
- https://github.com/icemellow-me/unified-capcha-solver
- https://github.com/icemellow-me/proxy-catalog
- https://github.com/icemellow-me/puter-gateway
- https://github.com/icemellow-me/cybersecurity-skills

## Quick-Start Commands

### Universal Solver
```bash
# Install deps
pip install --break-system-packages ddddocr pytesseract aiohttp pillow hcaptcha-challenger
apt install -yqq tesseract-ocr

# Start
docker exec -d hermes bash -c 'python3 /opt/universal-captcha-solver/solver-server.py --api-key 8010000000ccojr5nrbg516w5jvw1wu9 --port 8855 >> /tmp/universal-solver.log 2>&1'

# Health check
curl -sf http://127.0.0.1:8855/health
```

### reCAPTCHA v2 Solver
```bash
docker exec -d hermes bash -c 'cd /opt/recaptcha-v2-solver && DISPLAY=:99 python3 recaptcha-playwright-server.py --port 8866 --api-key 8010000000ccojr5nrbg516w5jvw1wu9 >> /tmp/recaptcha-playwright-server.log 2>&1'

# Health check
curl -sf http://127.0.0.1:8866/health
```

### Turnstile Solver
```bash
docker exec -d hermes bash -c 'cd /opt/turnstile-solver && DISPLAY=:99 python3 solver-server.py --api-key 8010000000ccojr5nrbg516w5jvw1wu9 --port 8877 --no-headless >> /tmp/turnstile.log 2>&1'

# Health check
curl -sf http://127.0.0.1:8877/health
```

## Safe Restart (One Server at a Time)

```bash
# Universal only
pkill -f "universal-captcha-solver/solver-server"
sleep 2
docker exec -d hermes bash -c 'python3 /opt/universal-captcha-solver/solver-server.py --api-key 8010000000ccojr5nrbg516w5jvw1wu9 --port 8855 >> /tmp/universal-solver.log 2>&1'

# reCAPTCHA only
pkill -f "recaptcha-v2-solver/recaptcha-playwright-server"
sleep 2
docker exec -d hermes bash -c 'cd /opt/recaptcha-v2-solver && DISPLAY=:99 python3 recaptcha-playwright-server.py --port 8866 --api-key 8010000000ccojr5nrbg516w5jvw1wu9 >> /tmp/recaptcha-playwright-server.log 2>&1'

# Turnstile only
pkill -f "turnstile-solver/solver-server"
sleep 2
docker exec -d hermes bash -c 'cd /opt/turnstile-solver && DISPLAY=:99 python3 solver-server.py --api-key 8010000000ccojr5nrbg516w5jvw1wu9 --port 8877 --no-headless >> /tmp/turnstile.log 2>&1'
```

Wait 10-15s after restart for Playwright browser init, then health-check.

## API Key
`8010000000ccojr5nrbg516w5jvw1wu9` (CaptchaPlugin user #264)
