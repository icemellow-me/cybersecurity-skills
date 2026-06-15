# Phone Number OSINT — Carrier OCN Lookup Table

Source: Local Calling Guide (localcallingguide.com) — NANPA-derived data, no CAPTCHA.

## Query URL Pattern

```
https://www.localcallingguide.com/lca_prefix.php?npa=XXX&nxx=YYY
```

Returns: rate centre, state, switch CLLI, OCN, LATA, thousands-block assignments, effective/disconnect dates.

## Major OCN → Carrier Mapping (US Wireless)

| OCN   | Carrier                                    | Line Type     |
|-------|-------------------------------------------|---------------|
| 6534  | New Cingular Wireless PCS, LLC - IL       | Wireless (AT&T) |
| 6508  | Cellco Partnership DBA Verizon Wireless   | Wireless (Verizon) |
| 6529  | T-Mobile USA, Inc.                        | Wireless (T-Mobile) |
| 6531  | New Cingular Wireless PCS, LLC - IL       | Wireless (AT&T) |
| 6532  | Sprint Spectrum L.P.                      | Wireless (legacy Sprint, now T-Mobile) |
| 6600  | T-Mobile License LLC                      | Wireless (T-Mobile) |

## Major OCN → Carrier Mapping (US Landline/VoIP)

| OCN   | Carrier                                    | Line Type     |
|-------|-------------------------------------------|---------------|
| 508J  | CenturyLink Communications, LLC           | Landline/VoIP |
| 5489  | Level 3 Communications, LLC               | VoIP/Carrier  |
| 544C  | Time Warner Cable Information Services    | VoIP/Cable    |
| 546C  | Comcast Phone of Michigan, LLC            | VoIP/Cable    |
| 022D  | Bandwidth.com CLEC, LLC                   | VoIP (Google Voice, etc.) |
| 621F  | Google Fiber Inc.                         | VoIP/Fiber    |

## Switch CLLI Prefix → City Mapping (Wisconsin examples)

| Prefix    | City        |
|-----------|-------------|
| MDSNWI    | Madison, WI |
| MKEWWI    | Milwaukee, WI |
| GRNBWI    | Green Bay, WI |
| LCRWWI    | La Crosse, WI |

## Cloudflare-gated OSINT sites to AVOID (no residential proxy)

- usphonebook.com
- 411.com
- truecaller.com (requires sign-in)
- phoneowner.com
- 800notes.com
- numverify.com (requires API key)
- spytox.com (timeout)
- callercomplaints.com (404s)
- telnyx.com API (Cloudflare blocked)

## Cloudflare-safe sources

- localcallingguide.com — prefix/block lookup (BEST)
- en.wikipedia.org — area code geography
- search.aol.com — web mentions (least aggressive bot detection)
