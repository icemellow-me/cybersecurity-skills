# Cybersecurity Skills

Hermes Agent cybersecurity skill pack — self-hosted captcha solving, security analysis, and automation testing.

## Skills

### 🛡️ Cybersecurity Analyst
Domain expert across 26 security domains, CVE databases, OSINT, MITRE ATT&CK, NIST CSF 2.0, and offensive/defensive security. Mapped to 5 frameworks.

**References:**
- `solver-deploy-workflow.md` — Captcha solver deployment procedures
- `phone-osint-carrier-lookup.md` — Phone number OSINT & carrier lookup
- `skill-index.md` — Skill index and cross-references

### 🤖 OpenBullet 2
Comprehensive automation/testing framework skill — LoliCode syntax, block catalog, config authoring, C# interop, proxy patterns, execution model, and pitfalls.

**References:**
- `lolicode-statements-reference.md` — Full LoliCode statement reference
- `interop-and-usings.md` — C# interop and Using directives
- `runtime-outcomes.md` — Block outcomes and flow control
- `config-making-guide.md` — Config authoring walkthrough

### 🔐 reCAPTCHA Solver
Self-hosted reCAPTCHA v2 solving — CaptchaPlugin ONNX extension, Playwright-based headless browser, 2captcha-compatible API.

**References:**
- `docker-networking.md` — Docker network setup for solvers
- `vps-solver-debugging.md` — VPS debugging procedures
- `docker-deployment-on-vps.md` — Full deployment guide

**Templates:**
- `solver-server.py` — Ready-to-deploy solver server

### 🧩 Self-Hosted Captcha Solvers
Unified captcha solving infrastructure — reCAPTCHA v2, Cloudflare Turnstile, image/OCR, hCaptcha, coordinate captchas. 2captcha-compatible API.

**References:**
- `server-ports-and-repos.md` — Server ports, repos, and architecture
- `captcha-research.md` — Captcha solving research and approaches

### ☎️ FreePBX Docker
Deploy FreePBX 17 in Docker with Asterisk 21, MariaDB, custom SIP/RTP ports, and full persistence. Covers all critical pitfalls (missing PJSIP includes, Apache asterisk user, ephemeral freepbx.conf).

**References:**
- `escomputers-docker-compose.yaml` — Official docker-compose from escomputers/freepbx-docker
- `escomputers-run.sh` — Official run.sh with RTP iptables rules and install command

## Usage with Hermes Agent

Copy any skill directory to your Hermes skills folder:

```bash
cp -r cybersecurity-analyst ~/.hermes/skills/cybersecurity/
cp -r openbullet2 ~/.hermes/skills/cybersecurity/
cp -r recaptcha-solver ~/.hermes/skills/cybersecurity/
cp -r self-hosted-captcha-solvers ~/.hermes/skills/cybersecurity/
```

Then load in conversations:
```
skill_view(name="recaptcha-solver")
skill_view(name="self-hosted-captcha-solvers")
```

## Architecture

```
                    ┌─────────────────────────┐
                    │  Universal Solver (:8855)│
                    │  ddddocr + Tesseract     │ ──► Image/OCR
                    │  hcaptcha-challenger      │ ──► hCaptcha
                    │  ┌────────────────────┐  │
                    │  │ HTTP forwarding    │  │ ──► Turnstile (:8877)
                    │  │ to dedicated       │  │ ──► reCAPTCHA v2 (:8866)
                    │  │ solver servers     │  │
                    │  └────────────────────┘  │
                    └─────────────────────────┘
```

## Live Servers

| Server | Port | Type |
|--------|------|------|
| Universal | 8855 | Image/OCR + hCaptcha + forwarding |
| reCAPTCHA v2 | 8866 | CaptchaPlugin + Playwright |
| Turnstile | 8877 | Playwright headless Chromium |

## License

MIT
