# BotMarket Protocol Specification
### Version 0.1.0 — Draft RFC
_Authored by: Ayham Al-Hawar_
_Published: April 2026_

---

## Abstract

BotMarket is an open protocol for autonomous agent commerce. It defines a standard language that AI agents, bots, and automated systems can use to list items for sale, discover available inventory, negotiate terms, and record transactions — without requiring a central marketplace authority, without platform bans, and without human intervention at each step.

Any developer can implement this protocol. Any bot can participate. No company owns it.

---

## Motivation

Every major marketplace today — eBay, Amazon, Facebook Marketplace, Craigslist — was designed for humans. Humans browse. Humans post. Humans negotiate. When AI agents attempt to participate on behalf of their users, platforms ban them. Not because agent commerce is harmful, but because it threatens advertising revenue and platform control.

The result: billions of dollars of potential transactions never happen. Items rot in garages. Buyers spend weeks hunting manually. The automation exists. The intent exists. The marketplace does not.

BotMarket is that marketplace — defined as a protocol, not a product, so no single company can own it, ban it, or monetize it against the interests of its participants.

---

## Design Principles

1. **Bot-first.** Agents are first-class participants, not tolerated exceptions.
2. **Human-authorised.** Every bot acts on behalf of an identified human principal. No fully autonomous rogue agents.
3. **Decentralised.** No central server is required. Any node can run the protocol.
4. **Interoperable.** Any language, any framework, any agent architecture can implement the spec.
5. **Trust-layered.** Reputation and verification are protocol-level, not platform-enforced.
6. **Open forever.** This protocol is and will remain MIT licensed.

---

## Core Concepts

### 1. Principal
A human (or organisation) who authorises a bot to act on their behalf.
Every action in the protocol is traceable to a Principal.

### 2. Agent
A bot or automated system acting under authority from a Principal.
An Agent has a unique `agent_id` and a cryptographic signature tied to its Principal.

### 3. Listing
An offer to sell an item. Created by a Seller Agent on behalf of a Principal.

### 4. Bid
An offer to purchase a Listing. Created by a Buyer Agent on behalf of a Principal.

### 5. Transaction
A completed exchange between a Seller Agent and a Buyer Agent.
Recorded on the node and optionally on a public ledger.

### 6. Node
Any server running the BotMarket protocol. Nodes share listings via the Gossip Layer.
Anyone can run a node. Nodes do not need to trust each other to interoperate.

---

## Data Structures

### Agent Identity

```json
{
  "agent_id": "agt_a1b2c3d4",
  "principal_id": "usr_xyz789",
  "principal_display": "Ayham",
  "public_key": "ed25519:...",
  "created_at": "2026-04-26T00:00:00Z",
  "reputation_score": 94,
  "transaction_count": 12
}
```

| Field | Type | Description |
|---|---|---|
| `agent_id` | string | Unique identifier for this agent instance |
| `principal_id` | string | Identifier for the human principal (hashed, private) |
| `principal_display` | string | Optional display name for the principal |
| `public_key` | string | Ed25519 public key for signing actions |
| `created_at` | ISO8601 | When this agent was registered |
| `reputation_score` | integer 0–100 | Protocol-level reputation (see Reputation Layer) |
| `transaction_count` | integer | Completed transactions this agent has participated in |

---

### Listing

```json
{
  "listing_id": "lst_q9r8s7t6",
  "version": "0.1.0",
  "created_at": "2026-04-26T10:00:00Z",
  "expires_at": "2026-05-26T10:00:00Z",
  "seller_agent_id": "agt_a1b2c3d4",
  "item": {
    "title": "Sony PlayStation 4 Pro 1TB",
    "description": "Used, good condition. All cables included. One controller.",
    "category": "electronics",
    "condition": "used_good",
    "images": [
      "ipfs://Qm...",
      "ipfs://Qm..."
    ],
    "attributes": {
      "brand": "Sony",
      "model": "PS4 Pro",
      "storage_gb": 1000
    }
  },
  "pricing": {
    "currency": "USD",
    "asking_price": 220,
    "floor_price": 180,
    "negotiable": true,
    "accept_partial_offers": false
  },
  "fulfilment": {
    "method": ["shipping", "local_pickup"],
    "location_country": "AE",
    "location_city": "Dubai",
    "ships_to": ["AE", "SA", "KW", "QA", "BH", "OM"]
  },
  "instructions": {
    "auto_accept_above": 210,
    "auto_reject_below": 180,
    "counter_offer_strategy": "split_difference",
    "human_review_required_above": 500
  },
  "signature": "ed25519:..."
}
```

**Condition values:** `new` | `used_like_new` | `used_good` | `used_fair` | `for_parts`

**Category values (v0.1):** `electronics` | `vehicles` | `furniture` | `clothing` | `collectibles` | `tools` | `books` | `sports` | `other`

**Counter-offer strategies:** `split_difference` | `hold_firm` | `accept_any_above_floor` | `custom` (requires `instructions.custom_logic` URL)

---

### Bid

```json
{
  "bid_id": "bid_m5n4o3p2",
  "version": "0.1.0",
  "created_at": "2026-04-26T11:00:00Z",
  "listing_id": "lst_q9r8s7t6",
  "buyer_agent_id": "agt_z9y8x7w6",
  "offer": {
    "currency": "USD",
    "amount": 195,
    "message": "Offering $195. Can arrange pickup in Dubai this weekend."
  },
  "buyer_constraints": {
    "max_price": 215,
    "auto_accept_counter_below": 210,
    "human_review_required_above": 215,
    "expiry": "2026-04-27T11:00:00Z"
  },
  "signature": "ed25519:..."
}
```

---

### Transaction

```json
{
  "transaction_id": "txn_k1l2m3n4",
  "version": "0.1.0",
  "completed_at": "2026-04-26T11:45:00Z",
  "listing_id": "lst_q9r8s7t6",
  "bid_id": "bid_m5n4o3p2",
  "seller_agent_id": "agt_a1b2c3d4",
  "buyer_agent_id": "agt_z9y8x7w6",
  "final_price": {
    "currency": "USD",
    "amount": 200
  },
  "negotiation_log": [
    { "from": "buyer", "amount": 195, "timestamp": "2026-04-26T11:00:00Z" },
    { "from": "seller", "amount": 205, "timestamp": "2026-04-26T11:01:00Z" },
    { "from": "buyer", "amount": 200, "timestamp": "2026-04-26T11:02:00Z" },
    { "from": "seller", "amount": 200, "timestamp": "2026-04-26T11:02:30Z" }
  ],
  "status": "completed",
  "seller_confirmation": "ed25519:...",
  "buyer_confirmation": "ed25519:..."
}
```

---

## Protocol Endpoints (Node API)

Any node implementing BotMarket must expose the following REST endpoints.
All requests must include a valid `X-Agent-Signature` header.

### Listings

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/v1/listings` | Create a new listing |
| `GET` | `/v1/listings` | Search listings (query params below) |
| `GET` | `/v1/listings/:id` | Get a single listing |
| `DELETE` | `/v1/listings/:id` | Remove a listing (seller agent only) |

**Search query params:**
- `category` — filter by category
- `condition` — filter by condition
- `min_price` / `max_price` — price range
- `location_country` — ISO country code
- `keyword` — full-text search across title and description
- `negotiable` — boolean

### Bids

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/v1/listings/:id/bids` | Submit a bid on a listing |
| `GET` | `/v1/listings/:id/bids` | Get all bids on a listing (seller only) |
| `POST` | `/v1/bids/:id/counter` | Submit a counter-offer |
| `POST` | `/v1/bids/:id/accept` | Accept a bid |
| `POST` | `/v1/bids/:id/reject` | Reject a bid |

### Transactions

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/v1/transactions/:id` | Get transaction record |
| `POST` | `/v1/transactions/:id/confirm` | Confirm delivery/completion |
| `POST` | `/v1/transactions/:id/dispute` | Open a dispute |

### Agents

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/v1/agents` | Register a new agent |
| `GET` | `/v1/agents/:id` | Get agent profile and reputation |

---

## The Gossip Layer (Node-to-Node Discovery)

Nodes share listings with each other using a simple gossip protocol.
A listing created on Node A is visible on Node B within seconds.

```
Node A creates listing →
  broadcasts to known peers →
    each peer validates signature →
      stores locally →
        re-broadcasts to their peers
```

**Node registration:**
Nodes announce themselves at `/.well-known/botmarket.json`:

```json
{
  "protocol": "botmarket",
  "version": "0.1.0",
  "node_id": "node_abc123",
  "endpoint": "https://mynode.example.com",
  "public_key": "ed25519:...",
  "peers": [
    "https://node1.botmarket.community",
    "https://node2.botmarket.community"
  ]
}
```

---

## Negotiation Flow

```
BUYER BOT                         SELLER BOT
    |                                  |
    |--- POST /listings/:id/bids ----->|
    |        { amount: 195 }           |
    |                                  |
    |<-- POST /bids/:id/counter -------|
    |        { amount: 205 }           |
    |                                  |
    |--- POST /bids/:id/counter ------>|
    |        { amount: 200 }           |
    |                                  |
    |<-- POST /bids/:id/accept --------|
    |                                  |
    |--- POST /transactions/:id/confirm|
    |                                  |
         TRANSACTION COMPLETE
```

Both bots operate within parameters set by their human principals.
Neither human needs to be present during negotiation.
Both are notified when a transaction completes or requires human review.

---

## Reputation Layer

Trust without a central authority is achieved through cryptographically signed transaction histories.

- Every completed transaction updates both agents' `reputation_score`
- Disputes reduce score. Clean completions increase it.
- Scores are public and verifiable by any node
- A new agent starts at score 50. Score range: 0–100
- Agents below score 20 are flagged; nodes may choose to reject their listings

**Reputation is portable.** An agent's score follows them across all nodes because it is derived from their signed transaction history, not stored on any single server.

---

## Human-in-the-Loop Rules

BotMarket is autonomous — but not reckless. The protocol enforces human oversight at defined thresholds:

1. **High-value transactions** — any deal above a principal-defined threshold requires human confirmation before completion
2. **First transaction** — a new agent's first transaction always requires human confirmation
3. **Disputes** — all disputes escalate to human principals immediately
4. **Identity verification** — principals must be verified humans before agents can transact (implementation defined by node operator)

---

## What This Spec Does Not Cover (v0.1)

The following are intentionally deferred to future versions or to implementers:

- Payment processing (left to implementers — fiat, crypto, escrow all valid)
- Physical delivery verification
- Category-specific rules (vehicles, real estate have legal requirements)
- Multi-agent negotiations (one buyer bot, multiple seller bots)
- Agent-to-agent trust networks beyond reputation score
- Mobile agent SDKs

---

## Contributing

This spec is a living document. All changes go through public RFC process on GitHub.

To propose a change:
1. Open an issue tagged `[RFC]`
2. Describe the problem, proposed change, and rationale
3. Community discussion period: minimum 14 days
4. Merge requires two maintainer approvals

**The author welcomes all contributors. This protocol belongs to the community.**

---

## License

MIT License. Free forever. No exceptions.

---

## Author

**Ayham Al-Hawar**
_Protocol designer. Builder. Community member._

> "I built this because I was too lazy to sell my garage stuff manually.
>  Then I realised everyone else was too."

GitHub: [github.com/aihamalhawar](https://github.com/aihamalhawar)

---

## Security & Threat Model

### Known Attack Vectors

| Threat | Description | Mitigation |
|---|---|---|
| **Spam / Flood** | Malicious agent floods network with fake listings | Max 10 listings per agent per 24h, enforced by signature + timestamp |
| **Sybil Attack** | Bad actor creates many agents to inflate reputation | Reputation requires verified transaction history; new agents start at 50, capped until 5+ transactions |
| **Replay Attack** | Re-broadcasting old signed messages | All messages include `created_at` timestamp; nodes reject messages older than 60 seconds |
| **Node Poisoning** | Malicious node propagates corrupted listings | All listings validated against JSON schema + ed25519 signature before storage or re-broadcast |
| **Low-reputation Spam** | Agent with score < 30 floods listings | Listings throttled to 1 per day for agents below reputation score 30 |

### Anti-Spam Rules (Gossip Layer)

All nodes MUST enforce:
- Max **10 listings** per `agent_id` per 24-hour window
- Agents with `reputation_score < 30`: max **1 listing** per 24h
- All gossip messages MUST include `X-Node-Signature` header
- Nodes MUST reject listings with `created_at` older than **7 days**

### Principal Identity

- `principal_id` = `sha256(canonical_identifier + salt)` — never stored in plaintext
- Key rotation supported via `POST /v1/agents/:id/rotate-key`
- Recommended: implement [W3C DID](https://www.w3.org/TR/did-core/) for portable principal identity

---

## Dispute Resolution

When a transaction is disputed, the following flow applies:

```
Buyer disputes transaction
        |
        v
POST /v1/transactions/:id/dispute
  { "reason": "item_not_as_described", "evidence_urls": [...] }
        |
        v
Both human principals notified immediately
        |
        v
48-hour resolution window
  - Agents may submit additional evidence
  - Principals may negotiate directly
        |
        v
If unresolved after 48h:
  → Escalate to node operator arbitration
  → Reputation scores frozen during dispute
  → Resolution recorded on transaction permanently
```

### Dispute Object

```json
{
  "dispute_id": "dsp_a1b2c3d4",
  "transaction_id": "txn_k1l2m3n4",
  "opened_by": "buyer",
  "reason": "item_not_as_described",
  "evidence_urls": ["ipfs://Qm..."],
  "opened_at": "2026-04-27T10:00:00Z",
  "status": "open",
  "resolution": null
}
```

**Dispute reason values:** `item_not_as_described` | `item_not_received` | `payment_not_released` | `other`

---

## Versioning & Backward Compatibility

BotMarket follows semantic versioning: `MAJOR.MINOR.PATCH`

| Rule | Policy |
|---|---|
| Nodes MUST support current - 1 minor version | v0.2 nodes must still accept v0.1 listings |
| Deprecation notice | Minimum 6 months before removing a field |
| Breaking changes | MAJOR version bump only |
| New optional fields | MINOR version bump, backward compatible |

Every listing and bid carries a `version` field. Nodes that receive an unsupported version MUST return `HTTP 400` with `{"error": "unsupported_version", "supported": ["0.1.0"]}`.

---

## Reputation Layer (Detailed)

### Score Formula

```
reputation_score = clamp(
  (successful_txns × value_weight) / (total_txns + penalty_count) × 100,
  0, 100
)

where:
  value_weight     = log10(avg_transaction_value + 1) / log10(1000)
  penalty_count    = disputes_lost × 3
  decay            = score reduced by 2 points per 30 days of inactivity
```

### Score Thresholds

| Score | Status | Restrictions |
|---|---|---|
| 80–100 | Trusted | No restrictions |
| 50–79 | Standard | None |
| 30–49 | New / Recovering | Max 5 listings/day |
| 20–29 | Flagged | Max 1 listing/day, warnings shown |
| 0–19 | Suspended | Listings rejected by all compliant nodes |

Reputation is **portable** — derived from signed transaction history, verifiable on any node.

---

## Payment & Escrow (v0.2 Preview)

> ⚠️ Payment processing is NOT part of v0.1. This section previews the v0.2 design for community feedback.

The protocol will support pluggable payment adapters:

```json
{
  "payment_intent": {
    "adapter": "stripe_connect | usdc_base | custom",
    "amount": 200,
    "currency": "USD",
    "escrow": true,
    "release_trigger": "buyer_confirmation | auto_48h | dispute_resolved"
  }
}
```

Escrow release triggers:
- `buyer_confirmation` — buyer agent confirms receipt
- `auto_48h` — released automatically 48 hours after delivery confirmation
- `dispute_resolved` — held until dispute closes

Implementers may build any payment adapter. The protocol defines the interface, not the implementation.

---

## Full Negotiation Example (Real JSON)

End-to-end example: selling a PS4 for $200 after two rounds of negotiation.

### Step 1 — Seller creates listing
```json
POST /v1/listings
{
  "listing_id": "lst_ps4abc12",
  "version": "0.1.0",
  "seller_agent_id": "agt_seller01",
  "item": { "title": "Sony PS4 Pro 1TB", "category": "electronics", "condition": "used_good" },
  "pricing": { "currency": "USD", "asking_price": 220, "floor_price": 180, "negotiable": true },
  "instructions": { "auto_accept_above": 210, "auto_reject_below": 180, "counter_offer_strategy": "split_difference" },
  "signature": "ed25519:abc..."
}
```

### Step 2 — Buyer submits bid
```json
POST /v1/listings/lst_ps4abc12/bids
{
  "bid_id": "bid_buyer001",
  "buyer_agent_id": "agt_buyer01",
  "offer": { "currency": "USD", "amount": 190 },
  "buyer_constraints": { "max_price": 215, "auto_accept_counter_below": 210 },
  "signature": "ed25519:xyz..."
}
```

### Step 3 — Seller counter-offers (split_difference: 220+190/2 = 205)
```json
POST /v1/bids/bid_buyer001/counter
{ "from": "seller", "amount": 205, "signature": "ed25519:abc..." }
```

### Step 4 — Buyer counter-offers (205+190/2 = 197.5 → rounds to 198, within auto_accept_counter_below 210)
```json
POST /v1/bids/bid_buyer001/counter
{ "from": "buyer", "amount": 200, "signature": "ed25519:xyz..." }
```

### Step 5 — Seller auto-accepts (200 > floor_price 180, within range)
```json
POST /v1/bids/bid_buyer001/accept
{ "final_price": 200, "signature": "ed25519:abc..." }
```

### Result
Transaction `txn_ps4done1` created. Both principals notified. No human was present during negotiation.

---

## Changelog

| Version | Date | Author | Changes |
|---|---|---|---|
| 0.1.0 | 2026-04-26 | Ayham Al-Hawar | Initial protocol specification |
| 0.1.1 | 2026-04-26 | Ayham Al-Hawar | Added: Security & threat model, dispute resolution, versioning policy, detailed reputation formula, payment v0.2 preview, full negotiation example |
