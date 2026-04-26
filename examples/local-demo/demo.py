#!/usr/bin/env python3
"""
BotMarket Protocol — Local Negotiation Demo
Two in-memory agents negotiate the sale of a PS4.
No network required. Runs in under 10 seconds.

Usage: python3 demo.py
"""

import json
import time
import uuid
from datetime import datetime

# ── Colours ──────────────────────────────────────────────────────────────────
GREEN  = "\033[92m"
BLUE   = "\033[94m"
YELLOW = "\033[93m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

def ts():
    return datetime.utcnow().isoformat() + "Z"

def log(actor, msg, colour=RESET):
    print(f"{colour}{BOLD}[{actor}]{RESET} {msg}")

# ── Agent ─────────────────────────────────────────────────────────────────────
class Agent:
    def __init__(self, agent_id, role, principal):
        self.agent_id  = agent_id
        self.role      = role
        self.principal = principal

# ── Seller Agent ──────────────────────────────────────────────────────────────
class SellerAgent(Agent):
    def __init__(self, agent_id, principal, asking, floor, auto_accept_above):
        super().__init__(agent_id, "seller", principal)
        self.asking           = asking
        self.floor            = floor
        self.auto_accept_above = auto_accept_above
        self.current_offer    = asking

    def create_listing(self, title):
        listing = {
            "listing_id":      f"lst_{uuid.uuid4().hex[:8]}",
            "version":         "0.1.0",
            "created_at":      ts(),
            "seller_agent_id": self.agent_id,
            "item":            {"title": title, "category": "electronics", "condition": "used_good"},
            "pricing":         {"currency": "USD", "asking_price": self.asking,
                                "floor_price": self.floor, "negotiable": True},
            "instructions":    {"auto_accept_above": self.auto_accept_above,
                                "auto_reject_below": self.floor,
                                "counter_offer_strategy": "split_difference"},
            "signature":       "ed25519:DEMO_SIG_SELLER"
        }
        log(self.agent_id, f"Listing created — {title} @ ${self.asking} (floor ${self.floor})", GREEN)
        return listing

    def evaluate_bid(self, amount):
        if amount >= self.auto_accept_above:
            log(self.agent_id, f"Auto-accepting ${amount} (above threshold ${self.auto_accept_above})", GREEN)
            return "accept", amount
        if amount < self.floor:
            log(self.agent_id, f"Rejecting ${amount} (below floor ${self.floor})", YELLOW)
            return "reject", None
        # Split difference
        counter = round((self.current_offer + amount) / 2, 2)
        self.current_offer = counter
        log(self.agent_id, f"Counter-offering ${counter} (split of ${self.current_offer} & ${amount})", GREEN)
        return "counter", counter

# ── Buyer Agent ───────────────────────────────────────────────────────────────
class BuyerAgent(Agent):
    def __init__(self, agent_id, principal, initial_bid, max_price, auto_accept_below):
        super().__init__(agent_id, "buyer", principal)
        self.initial_bid      = initial_bid
        self.max_price        = max_price
        self.auto_accept_below = auto_accept_below
        self.current_offer    = initial_bid

    def submit_bid(self, listing):
        log(self.agent_id, f"Scanning listing '{listing['item']['title']}' — submitting ${self.initial_bid}", BLUE)
        return self.initial_bid

    def evaluate_counter(self, counter_amount):
        if counter_amount > self.max_price:
            log(self.agent_id, f"Rejecting counter ${counter_amount} (exceeds max ${self.max_price})", YELLOW)
            return "reject", None
        if counter_amount <= self.auto_accept_below:
            log(self.agent_id, f"Auto-accepting ${counter_amount} (below threshold ${self.auto_accept_below})", BLUE)
            return "accept", counter_amount
        # Counter back
        counter = round((self.current_offer + counter_amount) / 2, 2)
        self.current_offer = counter
        log(self.agent_id, f"Counter-offering ${counter}", BLUE)
        return "counter", counter

# ── Marketplace (in-memory node) ──────────────────────────────────────────────
class BotMarketNode:
    def negotiate(self, seller, buyer, listing):
        print(f"\n{'═'*60}")
        print(f"{BOLD}  BotMarket Protocol — Demo Negotiation{RESET}")
        print(f"  Item:   {listing['item']['title']}")
        print(f"  Seller: {seller.principal}  |  Buyer: {buyer.principal}")
        print(f"{'═'*60}\n")

        negotiation_log = []
        amount = buyer.submit_bid(listing)
        round_num = 1

        while True:
            print(f"\n  {BOLD}── Round {round_num} ──{RESET}")
            time.sleep(0.6)

            # Seller evaluates
            s_action, s_value = seller.evaluate_bid(amount)
            negotiation_log.append({"from": "buyer", "amount": amount, "timestamp": ts()})

            if s_action == "accept":
                final = amount
                break
            if s_action == "reject":
                print(f"\n{YELLOW}  ✗ Negotiation failed. No deal reached.{RESET}\n")
                return None

            # Buyer evaluates counter
            time.sleep(0.6)
            b_action, b_value = buyer.evaluate_counter(s_value)
            negotiation_log.append({"from": "seller", "amount": s_value, "timestamp": ts()})

            if b_action == "accept":
                final = s_value
                break
            if b_action == "reject":
                print(f"\n{YELLOW}  ✗ Negotiation failed. Buyer walked away.{RESET}\n")
                return None

            amount = b_value
            round_num += 1

        txn = {
            "transaction_id":  f"txn_{uuid.uuid4().hex[:8]}",
            "version":         "0.1.0",
            "completed_at":    ts(),
            "listing_id":      listing["listing_id"],
            "seller_agent_id": seller.agent_id,
            "buyer_agent_id":  buyer.agent_id,
            "final_price":     {"currency": "USD", "amount": final},
            "negotiation_log": negotiation_log,
            "status":          "completed"
        }

        print(f"\n{'═'*60}")
        print(f"{GREEN}{BOLD}  ✓ TRANSACTION COMPLETE{RESET}")
        print(f"  Final price : ${final}")
        print(f"  Rounds      : {round_num}")
        print(f"  Txn ID      : {txn['transaction_id']}")
        print(f"\n  {seller.principal} notified: 'Your item sold for ${final}'")
        print(f"  {buyer.principal} notified:  'Found your item for ${final}'")
        print(f"  Neither human opened a browser.")
        print(f"{'═'*60}\n")
        print(f"{BOLD}Full transaction record:{RESET}")
        print(json.dumps(txn, indent=2))
        return txn


# ── Run demo ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    seller = SellerAgent(
        agent_id         = "agt_seller01",
        principal        = "Ayham",
        asking           = 220,
        floor            = 180,
        auto_accept_above= 210
    )

    buyer = BuyerAgent(
        agent_id          = "agt_buyer01",
        principal         = "Marcus",
        initial_bid       = 190,
        max_price         = 215,
        auto_accept_below = 210
    )

    node    = BotMarketNode()
    listing = seller.create_listing("Sony PS4 Pro 1TB")
    node.negotiate(seller, buyer, listing)
