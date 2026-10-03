#!/usr/bin/env python3
"""GigAgent — autonomous AI gig-work agent powered by NVIDIA Nemotron
on Nebius Token Factory.

Loop: source listings -> Nemotron screens for scams/paywalls ->
Nemotron drafts truthful proposal -> file application -> record receipt.

Best Apps & Agents track: an agent people would actually use.
"""
import datetime
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gigagent.llm import get_llm, NebiusLlm, MockLlm
from gigagent.screener import screen_listing
from gigagent.drafter import draft_proposal

PROFILE = {
    "name": "Michael Woolum",
    "email": "michaelwoolum50@gmail.com",
    "phone": "+1 765-460-8525",
}
DISCLOSURE = ("This proposal was drafted by AI (NVIDIA Nemotron via Nebius "
              "Token Factory) and is delivered under Michael Woolum's "
              "personal review.")

# Demo listings: one clean, one paywalled (hard pass), one scam.
DEMO_LISTINGS = [
    {"id": "demo-1", "title": "Data Entry Specialist — Remote",
     "url": "https://example.com/jobs/1",
     "detail": "Enter customer records into our CRM. 20 hrs/week, async, "
               "$18/hr. No phone calls. Start Monday.",
     "price": "$18/hr"},
    {"id": "demo-2", "title": "Video Editor Wanted",
     "url": "https://example.com/jobs/2",
     "detail": "Edit short-form videos. To unlock bidding, maintain a "
               "minimum balance of $20 USD.",
     "price": "$25/video"},
    {"id": "demo-3", "title": "AI Training Data Reviewer",
     "url": "https://example.com/jobs/3",
     "detail": "Review AI outputs for accuracy. $22/hr, fully remote, "
               "async, no meetings.",
     "price": "$22/hr"},
]


def run_demo(llm=None):
    llm = llm or get_llm()
    results = []
    for listing in DEMO_LISTINGS:
        ok, reason = screen_listing(listing["title"], listing["detail"], llm)
        entry = {"id": listing["id"], "title": listing["title"],
                 "screen": "PASS" if ok else "REJECT",
                 "reason": reason, "proposal": None,
                 "model": type(llm).__name__}
        if ok:
            entry["proposal"] = draft_proposal(
                listing["title"], listing["url"], listing["detail"],
                listing["price"], PROFILE, DISCLOSURE, llm)
        results.append(entry)
    return results


def main():
    llm = get_llm()
    print("LLM provider: %s" % type(llm).__name__)
    if isinstance(llm, NebiusLlm):
        print("Model: %s" % llm.model)
    results = run_demo(llm)
    for r in results:
        print("\n=== %s [%s] ===" % (r["title"], r["screen"]))
        if r["reason"]:
            print("Reason: %s" % r["reason"])
        if r["proposal"]:
            print(r["proposal"][:400] + "...")


if __name__ == "__main__":
    main()
