# Security Policy

## Supported Versions

| Version | Supported |
|---|---|
| 0.1.x | ✅ Active |

## Reporting a Vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

Email: security@botmarket.community (or open a private GitHub advisory)

Response SLA: 48 hours acknowledgement, 7 days for triage and mitigation plan.

## Threat Model

BotMarket's primary threat surface is the gossip network and agent identity layer.

| Threat | Severity | Status |
|---|---|---|
| Sybil attack (fake agents) | High | Mitigated via reputation + transaction history |
| Replay attack | High | Mitigated via timestamp validation (60s window) |
| Flood / spam | Medium | Mitigated via per-agent listing rate limits |
| Node poisoning | High | Mitigated via ed25519 signature validation |
| Principal identity leak | High | principal_id is hashed, never stored plaintext |

See SPEC.md §Security & Threat Model for full details.

## Responsible Disclosure

We follow a 90-day responsible disclosure policy. Researchers who report valid vulnerabilities will be credited in SPEC.md changelog.
