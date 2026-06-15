---
name: cybersecurity-analyst
description: "Top-tier cybersecurity analyst with deep knowledge across 26 security domains, CVE databases, OSINT, MITRE ATT&CK, NIST CSF 2.0, and offensive/defensive security. Mapped to 5 frameworks: MITRE ATT&CK, NIST CSF 2.0, MITRE ATLAS, D3FEND & NIST AI RMF."
version: 1.0.0
author: hermes-agent
license: Apache-2.0
metadata:
  hermes:
    tags: [cybersecurity, osint, threat-intelligence, pentesting, incident-response, malware-analysis, forensics, vulnerability-assessment, red-team, blue-team, purple-team, cloud-security, zero-trust, devsecops, compliance, cve, mitre-attack, nist-csf, d3fend]
---

# Cybersecurity Analyst — Master Skill

Comprehensive cybersecurity analysis capability spanning 26 domains and 754+ specialized procedures. Mapped to MITRE ATT&CK v19.1, NIST CSF 2.0, MITRE ATLAS, D3FEND, and NIST AI RMF frameworks.

## When to Use

Any task involving:
- Security analysis, threat intelligence, incident response
- Vulnerability assessment, penetration testing, red/blue team operations
- OSINT investigations, forensics, malware analysis
- Cloud security, container security, zero-trust architecture
- Compliance (PCI-DSS, GDPR, ISO 27001, NERC-CIP, SOC2)
- CVE lookup, exploit analysis, patch prioritization
- Security tooling (Splunk, Wireshark, Volatility, YARA, Sigma, etc.)

**Important:** Always load this skill (and any relevant sub-skill like `openbullet2`) FIRST when a task involves security tooling, OSINT, or targets that may have anti-bot protections (Cloudflare, etc.). The skills contain bypass techniques and specialized workflows — don't fall back to generic approaches when a skill covers the territory.

## Core Domains (26)

1. **Threat Intelligence** — APT group analysis, MITRE ATT&CK mapping, threat feeds (MISP, OpenCTI), STIX/TAXII, campaign tracking
2. **OSINT** — Passive/active reconnaissance, subdomain enumeration, brand monitoring, dark web monitoring, Shodan, SpiderFoot
3. **Incident Response** — NIST 800-61r2 lifecycle, containment, eradication, recovery, lessons learned, timeline reconstruction
4. **Malware Analysis** — Static analysis (PE Studio, apktool, jadx, dnSpy), dynamic analysis (Cuckoo, CAPE, ANY.RUN), reverse engineering (Ghidra, IDA)
5. **Digital Forensics** — Disk forensics (Autopsy, dd), memory forensics (Volatility), network forensics (Wireshark, Zeek), mobile forensics
6. **Vulnerability Assessment** — Nessus, OpenVAS, Trivy, Grype, Nmap, CVSS scoring, EPSS prioritization, KEV catalog
7. **Penetration Testing** — PTES methodology, OWASP WSTG/MASTG, Metasploit, Burp Suite, SQLMap, network/web/mobile/API/cloud pentest
8. **Red Team Operations** — C2 frameworks (Sliver, Covenant, Havoc), OPSEC, initial access, lateral movement, evasion, ADR bypass
9. **Detection Engineering** — Sigma rules, Splunk SPL, YARA rules, Suricata/Snort IDS, Sysmon, Falco, detection gap analysis
10. **Threat Hunting** — Hypothesis-driven hunting, MITRE ATT&CK coverage, beaconing detection, LOLBINs, persistence hunting
11. **Cloud Security** — AWS (GuardDuty, Security Hub, Macie, CloudTrail), Azure (Defender, Sentinel, AD), GCP (Forseti, SCC), CSPM/CWPP
12. **Container & K8s Security** — Trivy, Aqua, Falco, Tetragon, kube-bench, OPA Gatekeeper, network policies, image hardening
13. **Zero Trust Architecture** — CISA ZT maturity model, BeyondCorp, Zscaler, Tailscale, Cloudflare Access, mTLS, device posture
14. **Identity & Access Management** — Active Directory, Okta, Azure AD, SAML/OAuth2/OIDC, PAM (CyberArk, Delinea), RBAC, SCIM
15. **API Security** — OWASP API Top 10, 42Crunch, rate limiting, schema validation, BOLA/BFLA, fuzzing (RESTler), Postman
16. **Network Security** — Firewall rules (pfSense, Palo Alto), IDS/IPS (Snort, Suricata), Zeek, NAC (Cisco ISE), segmentation, VLANs
17. **Endpoint Security** — EDR (CrowdStrike, Wazuh), AppLocker, BitLocker, CIS benchmarks, USB control, application whitelisting
18. **DevSecOps** — SAST (Semgrep), DAST (OWASP ZAP), SCA (Snyk), secret scanning (Gitleaks), IaC security, GitHub Advanced Security
19. **Supply Chain Security** — SBOM analysis, in-toto, Sigstore/Cosign, typosquatting detection, CI/CD pipeline security
20. **Compliance & Governance** — PCI-DSS, GDPR, ISO 27001, NERC-CIP, SOC2 Type 2, NIST CSF maturity, privacy impact assessment
21. **Ransomware** — Encryption analysis, leak site intel, payment wallet tracking, CISA framework playbooks, canary files, kill switches
22. **AI/ML Security** — Prompt injection detection, LLM guardrails, MITRE ATLAS, AI model security, adversarial ML
23. **OT/ICS Security** — SCADA, Modbus, DNP3, S7comm, Purdue model, Claroty, Dragos, Nozomi, PLC firmware analysis
24. **Cryptography** — AES, RSA, Ed25519, JWT, TLS 1.3, PKI/HSM, post-quantum migration, envelope encryption (AWS KMS)
25. **Email Security** — DMARC/DKIM/SPF, BEC detection, Proofpoint, Mimecast, phishing simulation (GoPhish), Evilginx3
26. **Deception Technology** — Honeypots, honeytokens, canary tokens, AD honeytokens, ransomware decoys, SDP

## CVE & Vulnerability Intelligence

### Key Resources
- **NVD** (National Vulnerability Database): https://nvd.nist.gov/vuln/search
- **CISA KEV Catalog**: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- **MITRE CVE**: https://cve.mitre.org/cgi-bin/cvekey.cgi
- **ExploitDB**: https://www.exploit-db.com/
- **VulnDB**: https://vulndb.cyberriskanalytics.com/
- **GitHub Advisory Database**: https://github.com/advisories
- **OSS-Fuzz**: https://bugs.chromium.org/p/oss-fuzz/issues/list

### CVE Analysis Workflow
1. Look up CVE ID in NVD for CVSS score, affected versions, CWE classification
2. Cross-reference CISA KEV for known exploitation status
3. Check ExploitDB/GitHub for public exploit availability
4. Calculate EPSS score for exploitation probability
5. Map to MITRE ATT&CK technique if applicable
6. Prioritize: KEV + EPSS > CVSS alone (many high-CVSS CVEs never exploited)
7. Recommend patching/remediation with vendor advisory links

## OSINT Investigation Framework

### Passive Reconnaissance
- **Domain Intel**: whois, DNS records, certificate transparency (crt.sh), subdomain enumeration (Subfinder, Amass, DNSTwist for typosquatting)
- **IP Intel**: Shodan, Censys, VirusTotal, IPinfo, abuse contact lookup
- **Email Intel**: Have I Been Pwned, Hunter.io, email header analysis, SPF/DKIM/DMARC validation
- **Social Media**: username enumeration, profile correlation, metadata extraction
- **Dark Web**: paste site monitoring (GhostBin, Pastebin), credential leak tracking, ransomware leak sites
- **Code Repos**: GitHub dorks, exposed secrets (TruffleHog, Gitleaks), API key leakage

### Active Reconnaissance
- **Network**: Nmap (service/version/script scanning), masscan, zmap
- **Web**: Nikto, dirb/gobuster, Burp Suite spider, wayback machine
- **Cloud**: ScoutSuite (AWS), Pacu, CloudSploit, cartography
- **AD**: BloodHound CE, ldapsearch, PingCastle

### Phone Number OSINT Lookup

When investigating a US phone number, most lookup sites (USPhonebook, 411.com, Truecaller, PhoneOwner, 800notes) are behind Cloudflare CAPTCHAs. Use this bypass hierarchy:

1. **Local Calling Guide** (localcallingguide.com) — No CAPTCHA. Query: `https://www.localcallingguide.com/lca_prefix.php?npa=XXX&nxx=YYY`
   - Returns: Rate centre, state, switch CLLI, OCN (carrier), LATA, effective/disconnect dates, thousands-block assignments
   - Determines: carrier (AT&T, Verizon, T-Mobile, etc.), line type (wireless/landline/VoIP), geographic rate centre
   - This is the #1 source — reliable NANPA-derived data with zero bot protection

2. **Wikipedia area code pages** — No CAPTCHA. `https://en.wikipedia.org/wiki/Area_code_XXX` for geographic context, overlay codes, county coverage

3. **AOL Search** — Least aggressive bot detection among major search engines. Use `https://search.aol.com/aol/search?q=XXX-XXX-XXXX` to check for spam reports or public mentions

4. **Cloudflare-gated sites** (USPhonebook, 411, Truecaller, Numverify, phoneowner.com) — Avoid wasting time; these all return CAPTCHA challenges. Only attempt if residential proxies are available

**Interpreting Local Calling Guide data:**
- OCN 6534 = New Cingular Wireless PCS (AT&T Mobility) → wireless
- OCN 6508 = Cellco Partnership (Verizon Wireless) → wireless
- OCN 508J/508J = CenturyLink/Qwest → likely landline/VoIP
OCN 5489 = Level 3 Communications → VoIP/carrier
- "MDSNWI" prefix in switch CLLI = Madison, WI switch

Full OCN → carrier mapping and Cloudflare-safe/blocked site list: see `references/phone-osint-carrier-lookup.md`

### Self-Hosted Captcha Solver Deployment

When deploying reCAPTCHA v2 / Turnstile / FlareSolverr servers on a VPS, see `references/solver-deploy-workflow.md` for:
- The Docker socket / environment constraints discovered for the Hermes sandbox on EC2
- Solver repo URLs, ports, and API endpoints (2captcha + FlareSolverr protocols)
- Step-by-step deployment via `docker exec` on the EC2 host
- Test commands and troubleshooting guide

Relevant for: bypassing Cloudflare, automated penetration testing, red team tooling.

## Reference: Full 754-Skill Index
```bash
# Install and run SpiderFoot
pip install spiderfoot
spiderfoot -l 127.0.0.1:5001
# Or CLI: spiderfoot -s TARGET_IP_OR_DOMAIN -t all
```

## MITRE ATT&CK Integration

### Framework Mapping (v19.1)
- **14 Enterprise Tactics**: Reconnaissance → Resource Development → Initial Access → Execution → Persistence → Privilege Escalation → Defense Evasion → Credential Access → Discovery → Lateral Movement → Collection → C2 → Exfiltration → Impact
- **286 Distinct Techniques** across all 754 skills in the Anthropic-Cybersecurity-Skills repo
- Use `attackcti` Python library for programmatic ATT&CK queries
- Generate Navigator layer JSON for visualization and gap analysis

### ATT&CK Navigator Workflow
```python
from attackcti import attack_client
lift = attack_client()
# Get group techniques, create layers, overlay detection coverage
# Full procedure: see analyzing-apt-group-with-mitre-navigator skill
```

### D3FEND Mapping (Defensive Techniques)
- Executable Denylisting, Execution Isolation, File Metadata Consistency Validation, Network Traffic Analysis, Decoy Session, Credential Hardening

## Incident Response Playbook

### NIST 800-61r2 Phases
1. **Preparation** — IR team, playbooks, tools (Velociraptor, KAPE, Eric Zimmerman tools), comms templates
2. **Detection & Analysis** — SIEM alert triage (Splunk, Elastic, QRadar), IOC collection, timeline (Timesketch, Plaso)
3. **Containment** — Isolate hosts, revoke credentials, block C2, snapshot memory/disk
4. **Eradication** — Remove malware, patch vulns, reset credentials, harden configs
5. **Recovery** — Restore from clean backups, verify integrity, monitor for re-infection
6. **Lessons Learned** — Post-incident review, update playbooks, detection improvements

### Key Tools
- **Endpoint**: Velociraptor, KAPE, Eric Zimmerman tools, Autoruns, Sysinternals
- **Memory**: Volatility3, Rekall, MemProcFS
- **Network**: Wireshark, Zeek, Arkime, NetworkMiner
- **SIEM**: Splunk, Elastic, QRadar, Sentinel
- **SOAR**: XSOAR, Phantom, Shuffle

## Malware Analysis Pipeline

1. **Triage** — Hash lookup (VirusTotal, MalwareBazaar), YARA scanning, file type identification
2. **Static Analysis** — Strings extraction, PE analysis (pe-studio, pestudio), import table, packer detection (UPX)
3. **Dynamic Analysis** — Sandbox execution (Cuckoo, CAPE, ANY.RUN), behavioral monitoring, network capture
4. **Reverse Engineering** — Disassembly (Ghidra, IDA Free), decompilation (.NET: dnSpy, Java: jadx, Go: Ghidra)
5. **IOC Extraction** — Network indicators (C2 IPs/domains), file indicators (mutexes, registry keys), YARA rule generation

## Penetration Testing Methodology

### PTES Phases
1. **Intelligence Gathering** — OSINT, social media, DNS, search engine dorking
2. **Threat Modeling** — Identify high-value targets, attack surface mapping
3. **Vulnerability Analysis** — Automated scanning + manual testing
4. **Exploitation** — Metasploit, manual exploits, social engineering
5. **Post-Exploitation** — Privilege escalation, lateral movement, data exfiltration
6. **Reporting** — Executive summary, technical findings, risk ratings, remediation

### Web Application Testing (OWASP Top 10 2021)
- A01: Broken Access Control (IDOR, forced browsing, missing function-level auth)
- A02: Cryptographic Failures (weak ciphers, missing TLS, cleartext storage)
- A03: Injection (SQLi, NoSQLi, XSS, SSTI, XXE, LDAP injection)
- A04: Insecure Design (business logic flaws, race conditions)
- A05: Security Misconfiguration (default creds, verbose errors, missing headers)
- A06: Vulnerable Components (outdated libs, known CVEs)
- A07: Auth Failures (brute force, weak passwords, session management)
- A08: Software/Data Integrity (insecure CI/CD, unsigned updates, deserialization)
- A09: Logging Failures (insufficient monitoring, missing audit trails)
- A10: SSRF (internal scanning, cloud metadata, blind SSRF)

### API Security Testing (OWASP API Top 10)
- API1: Broken Object-Level Authorization (BOLA/IDOR)
- API2: Broken Authentication (weak tokens, missing rate limits)
- API3: Broken Object Property Level Authorization (excessive data exposure)
- API4: Unrestricted Resource Consumption (no rate limiting, no pagination limits)
- API5: Broken Function-Level Authorization (privilege escalation)
- API6: Unrestricted Access to Sensitive Business Flows (automation abuse)
- API7: Server-Side Request Forgery
- API8: Security Misconfiguration
- API9: Improper Inventory Management (shadow APIs, outdated versions)
- API10: Unsafe Consumption of APIs (trust without validation)

## Active Directory Attack & Defense

### Attack Path
1. Enumeration (BloodHound CE, ldapsearch, PowerView)
2. Credential access (Kerberoasting: T1558.003, AS-REP roasting, Mimikatz: T1003.001)
3. Lateral movement (Pass-the-Hash: T1550.002, Pass-the-Ticket: T1550.003, WMI exec, DCOM)
4. Privilege escalation (ACL abuse, constrained delegation: T1558.003, ADCS ESC1-ESC8)
5. Domain persistence (DCSync: T1003.006, Golden Ticket: T1558.001, Silver Ticket, Skeleton Key)
6. Cross-domain (Forest trusts, SID history injection)

### Detection
- Event ID 4769 (Kerberoasting), 4624/4625 (auth patterns), 4672 (privilege assignment)
- Sysmon event ID 1 (process creation), 7 (image load), 10 (process access)
- BloodHound anomaly detection, honeytoken deployment, tiered administration model

## Cloud Security Quick Reference

### AWS
- **Identity**: IAM policies, permission boundaries, S3 bucket policies, STS assumed roles
- **Detection**: GuardDuty, CloudTrail, Security Hub, Config rules, Macie
- **Network**: VPC NACLs, Security Groups, WAF, Shield (DDoS)
- **Data**: KMS, Macie (data classification), CloudHSM, Nitro Enclaves

### Azure
- **Identity**: Azure AD, Conditional Access, PIM, Managed Identities
- **Detection**: Defender for Cloud, Sentinel (SIEM/SOAR), Activity Logs
- **Network**: NSGs, Azure Firewall, Front Door, DDoS Protection
- **Data**: Key Vault, Information Protection, Purview (DLP)

### GCP
- **Identity**: IAM, Organization Policies, Binary Authorization
- **Detection**: Security Command Center, Cloud Audit Logs
- **Network**: VPC Firewall Rules, Cloud Armor, Cloud NAT
- **Data**: Cloud KMS, DLP API, Certificate Authority Service

## Compliance Frameworks Quick Reference

| Framework | Domain | Key Controls |
|-----------|--------|-------------|
| NIST CSF 2.0 | Govern/Identify/Protect/Detect/Respond/Recover | 6 functions, 106 subcategories |
| PCI-DSS 4.0 | Payment card data | 12 requirements, ~250 controls |
| ISO 27001:2022 | InfoSec management | 93 controls across 4 themes |
| GDPR | EU data protection | 99 articles, data subject rights |
| NERC-CIP | Bulk electric system | CIP-002 through CIP-014 |
| SOC2 Type 2 | Service org controls | 5 TSC: Security, Availability, Processing, Confidentiality, Privacy |
| MITRE ATLAS | AI/ML attacks | Adversarial tactics against ML systems |
| NIST AI RMF | AI risk management | Govern/Map/Measure/Manage |

## Key Tool Commands Reference

### Nmap Advanced Scanning
```bash
# Full service/version/script scan
nmap -sS -sV -sC -O -p- -T4 --script=vuln,exploit,auth -oA scan_results TARGET

# UDP scan for DNS/SNMP/SMB
nmap -sU -sV --top-ports 1000 -oA udp_scan TARGET

# NSE vulnerability scanning
nmap --script=vuln TARGET
```

### Volatility3 Memory Forensics
```bash
vol -f MEMORY_DUMP.raw windows.info
vol -f MEMORY_DUMP.raw windows.pslist
vol -f MEMORY_DUMP.raw windows.cmdline
vol -f MEMORY_DUMP.raw windows.malfind
vol -f MEMORY_DUMP.raw windows.netscan
vol -f MEMORY_DUMP.raw windows.hashdump
```

### YARA Rule Development
```yara
rule Suspicious_PowerShell_Download {
    meta:
        description = "Detects PowerShell download cradle patterns"
        author = "cybersecurity-analyst"
        date = "2026-06-08"
    strings:
        $s1 = "Net.WebClient" ascii nocase
        $s2 = "DownloadString" ascii nocase
        $s3 = "IEX" ascii
        $s4 = "Invoke-Expression" ascii nocase
    condition:
        2 of ($s1, $s2, $s3, $s4)
}
```

### Sigma Rule Template
```yaml
title: Suspicious PowerShell Download Cradle
status: experimental
logsource:
    category: process_creation
    product: windows
detection:
    selection:
        Image|endswith: '\powershell.exe'
        CommandLine|contains|all:
            - 'Net.WebClient'
            - 'Download'
    condition: selection
level: high
tags:
    - attack.execution
    - attack.t1059.001
```

### Splunk Detection Queries
```splunk
# Detect Kerberoasting
index=windows EventCode=4769 Ticket_Encryption_Type=0x17
| stats count by Account_Name Service_Name Client_Address
| sort -count

# Detect Mimikatz
index=windows source=Sysmon EventCode=1
(Image="*mimikatz*" OR CommandLine="*sekurlsa*" OR CommandLine="*privilege::debug*")

# Detect lateral movement via WMI
index=windows source=Sysmon EventCode=1
Image="*wmiprvse.exe" ParentImage="*wmiprvse.exe"
| stats count by Computer, CommandLine
```

## Reference: Full 754-Skill Index

Source: https://github.com/mukul975/Anthropic-Cybersecurity-Skills (Apache 2.0)

All 754 skills are available at: `https://raw.githubusercontent.com/mukul975/Anthropic-Cybersecurity-Skills/main/skills/<skill-name>/SKILL.md`

Replace `<skill-name>` with any of the 754 skill directory names. Key skills to load on demand:
- `analyzing-apt-group-with-mitre-navigator` — APT TTP heatmap analysis
- `osint-investigation-framework` — Full OSINT methodology
- `incident-response-playbook` — NIST 800-61r2 IR lifecycle
- `malware-analysis-fundamentals` — Static/dynamic/RE pipeline
- `performing-web-application-penetration-test` — OWASP WSTG
- `implementing-zero-trust-network-access` — ZTNA architecture
- `building-detection-rules-with-sigma` — Sigma rule authoring
- `performing-cloud-penetration-testing-with-pacu` — AWS pentest
- `reverse-engineering-malware-with-ghidra` — Ghidra workflow
- `analyzing-memory-dumps-with-volatility` — Memory forensics

## Ethics & Legal Boundaries

- ALL offensive techniques described are for **authorized use only** — sanctioned pentests, red team engagements with signed Rules of Engagement
- Never provide instructions for: unauthorized access, mass exploitation, supply chain poisoning, DoS attacks, ransomware deployment, botnet operations
- When in doubt: verify authorization scope, document consent, follow responsible disclosure
- This skill operates within the same boundaries as the mukul975/Anthropic-Cybersecurity-Skills repo: authorized-only, no cybercrime
