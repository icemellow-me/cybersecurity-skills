# Captcha Solving Research Notes

## Key GitHub Projects

### ddddocr (⭐14k+)
- **Repo:** sml2h3/ddddocr
- **PyPI:** `pip install ddddocr`
- ONNX-based OCR engine, handles warped/noisy text captchas
- Two modes: OCR (text recognition) and detection (object position finding)
- ~0.02s per solve on CPU
- Use `show_ad=False` to disable ad banner on init

### hcaptcha-challenger
- **Repo:** QIN2DIM/hcaptcha-challenger
- **PyPI:** `pip install hcaptcha-challenger`
- ONNX models: ResNet (classification), YOLOv8 (detection)
- LLM agent: Gemini for zero-shot challenge understanding
- Import changes between versions — `ZeroShotAgent` removed, `AgentV` is current stable API
- Requires `GEMINI_API_KEY` for actual solving (ONNX models alone aren't sufficient for all challenge types)

### Tesseract OCR
- System package: `apt install tesseract-ocr`
- Python wrapper: `pip install pytesseract`
- Good fallback for clean text, struggles with heavy noise/warping
- Use together with ddddocr (parallel engine approach)

### CaptchaPlugin
- Browser extension with ONNX models for reCAPTCHA v2
- API key format: numeric prefix + alphanumeric
- 2captcha-compatible API built into the extension
- Chrome MV3 extension — content scripts require proper registration before page load
- Cannot simply `--load-extension` into an existing browser — need persistent context

## Architecture Patterns

### Parallel OCR Engines
Run ddddocr + Tesseract simultaneously, pick the better result:
- If ddddocr returns non-empty → use it (usually better)
- If ddddocr empty but Tesseract returns result → fallback
- If both empty → report unsolvable

### Forwarding Hub Pattern
Single universal server on a well-known port that:
1. Handles local solving (image OCR, hCaptcha) directly
2. Forwards token-type captchas (reCAPTCHA, Turnstile) to dedicated servers
3. Polls upstream results and returns them transparently
4. Gives users a single API endpoint for all types

### Playwright Persistent Context
For captcha types needing browser extensions:
```python
browser = await playwright.chromium.launch_persistent_context(
    user_data_dir="/tmp/captcha-profile",
    headless=False,  # some captchas detect headless
    args=["--disable-blink-features=AutomationControlled"],
    extensions=[ext_path]
)
```
- `--load-extension` CLI flag is unreliable for MV3 content script injection into iframes
- Persistent context ensures extension is registered before any page loads
- Browser contexts go stale after extended idle — implement restart logic

## Captcha Types Taxonomy

| Type | Solving Approach | Speed | Self-hostable |
|------|-----------------|-------|---------------|
| Text OCR | ddddocr/Tesseract | ~1s | ✅ |
| reCAPTCHA v2 | Browser + extension | ~60s | ✅ |
| reCAPTCHA v3 | Score simulation (harder) | ~10s | Partial |
| hCaptcha | ONNX + LLM | ~30s | ✅ (needs Gemini) |
| Turnstile non-interactive | Browser JS execution | ~10s | ✅ |
| Turnstile managed/interactive | Browser + extension | ~15s | Partial |
| FunCaptcha | AI classification | ~30s | Needs model |
| KeyCaptcha | ML classification | ~20s | Needs model |
| Coordinate/Click | ddddocr detection | ~2s | ✅ |
| GeeTest | ML + behavioral | ~15s | Complex |
