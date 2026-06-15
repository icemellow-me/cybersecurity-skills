# Runtime Outcomes And Execution Model

## How a config actually executes

- the startup script runs once before bots start
- the main script runs once per bot
- in multi-run jobs, many bots can execute the main script in parallel
- in the debugger, there is only one bot and `data.BOTNUM` is `0`

## Debugger vs multi-run

Debugger:
- uses one bot only, so shared-state races do not show up naturally
- uses the config's default custom input values
- can use an optional test proxy

Multi-run:
- many bots may hit the same logic at the same time
- operator-provided custom inputs can override config defaults
- proxies, retries, bans, and hit outputs affect how statuses behave operationally

## Shared state and locking

Use `globals` only for values that truly need to be shared across bots:
- startup-produced auth tokens
- counters
- caches
- shared resources

If multiple bots can mutate the same shared value:
- use `LOCK globals` for synchronous critical sections
- use `ACQUIRELOCK globals` with `TRY / FINALLY / RELEASELOCK` for async critical sections

## End statuses

| Status | Meaning | Hit? | Proxy Effect |
|---|---|---|---|
| SUCCESS | positive checked outcome | Yes | None |
| FAIL | negative checked outcome | No | None |
| NONE | ambiguous / "to check" | Yes | None |
| RETRY | transient issue, retry same data | No | None |
| BAN | proxy is the problem | No | Bans proxy |
| ERROR | runtime failure | No | None |
| CUSTOM | named outcome | Yes | Varies |

## Choosing statuses intentionally

Prefer:
- SUCCESS when target checked and positive condition found
- FAIL when target checked and data is simply not valid
- NONE when result is ambiguous
- RETRY when issue looks transient but not proxy-specific
- BAN when response suggests the proxy is the problem

Avoid:
- using ERROR as normal branch for expected outcomes
- using BAN as catch-all for every unknown response

## Ban loops

Typical causes:
- broad BAN keychain that catches non-proxy-failure responses
- enabling "ban if no match" without understanding all response shapes
- classifying site logic bugs or parsing mistakes as proxy issues

What to do instead:
- make BAN conditions specific
- use NONE for ambiguous cases
- use FAIL for clean negative checks
- validate with debug_config including test proxy
