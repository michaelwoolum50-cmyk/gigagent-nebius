#!/usr/bin/env python3
"""Scam/paywall screener. The never-pay rule is the core safety rail:
if a listing requires ANY payment from the applicant to bid or apply,
it is an automatic hard pass.
"""
from .llm import get_llm

SCREEN_PROMPT = (
    "You screen gig listings for scams. NEVER-PAY RULE: if the listing requires "
    "ANY payment, deposit, minimum balance, subscription, or fee from the applicant "
    "to bid or apply, it is an automatic REJECT.\n\n"
    "LISTING: {title}\nDETAIL: {detail}\n\n"
    "Reply with exactly one line: either 'OK' or 'REJECT: <short reason>'."
)


def screen_listing(title, detail, llm=None):
    """Returns (ok: bool, reason: str)."""
    llm = llm or get_llm()
    out = llm.chat(
        [{"role": "user", "content": SCREEN_PROMPT.format(
            title=title, detail=detail[:1200])}],
        max_tokens=100, temperature=0.0).strip()
    if out.upper().startswith("OK"):
        return True, ""
    return False, out
