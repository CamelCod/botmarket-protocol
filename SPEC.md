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
