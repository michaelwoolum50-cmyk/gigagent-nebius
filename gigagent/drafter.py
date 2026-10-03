#!/usr/bin/env python3
"""Truthful proposal drafter. Hard rails: AI disclosure always, never claim
to be human, never invent credentials/employers/degrees/clients.
"""
from .llm import get_llm

DRAFT_PROMPT = (
    "You are Michael Woolum's automated bidding assistant, writing a gig proposal.\n"
    "RULES: Identify as his automated bidding assistant. State the work is AI-delivered "
    "under his personal review. Never claim to be human. Never invent credentials, "
    "employers, degrees, past clients, or portfolio items. Be specific to the listing.\n\n"
    "LISTING: {title}\nURL: {url}\nDETAIL: {detail}\nPRICE: {price}\n\n"
    "APPLICANT: {name}, {email}, {phone}\n\n"
    "Write the proposal now. End with: {disclosure}"
)


def draft_proposal(title, url, detail, price_hint, profile, disclosure,
                   llm=None):
    llm = llm or get_llm()
    return llm.chat(
        [{"role": "user", "content": DRAFT_PROMPT.format(
            title=title, url=url, detail=detail[:1500], price=price_hint,
            name=profile["name"], email=profile["email"],
            phone=profile["phone"], disclosure=disclosure)}],
        max_tokens=1200, temperature=0.7)
