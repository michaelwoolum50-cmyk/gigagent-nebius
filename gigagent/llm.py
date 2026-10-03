#!/usr/bin/env python3
"""LLM provider with Nebius Token Factory + offline mock fallback.

The winning pattern: every external capability is an interface with two
implementations. With NEBIUS_API_KEY set, uses NVIDIA Nemotron on Nebius
Token Factory. Without it, MockLlm runs deterministically offline so judges
and CI can exercise the full loop with no key.
"""
import json
import os
import urllib.request
import urllib.error

NEBIUS_BASE_URL = os.environ.get(
    "NEBIUS_BASE_URL", "https://api.tokenfactory.nebius.com/v1")
NEBIUS_API_KEY = os.environ.get("NEBIUS_API_KEY", "")

# Primary: fast MoE specialist. Fallback: larger reasoning model.
PRIMARY_MODEL = "nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B"
FALLBACK_MODEL = "nvidia/nemotron-3-super-120b-a12b"


class NebiusLlm:
    """NVIDIA Nemotron via Nebius Token Factory (OpenAI-compatible)."""

    def __init__(self, model=PRIMARY_MODEL, api_key=None, base_url=None):
        self.model = model
        self.api_key = api_key or NEBIUS_API_KEY
        self.base_url = (base_url or NEBIUS_BASE_URL).rstrip("/")
        if not self.api_key:
            raise RuntimeError("NEBIUS_API_KEY not set")

    def chat(self, messages, max_tokens=1200, temperature=0.7):
        payload = json.dumps({
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }).encode("utf-8")
        req = urllib.request.Request(
            self.base_url + "/chat/completions", data=payload,
            headers={"Content-Type": "application/json",
                     "Authorization": "Bearer " + self.api_key})
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            # Fallback model on primary failure
            if self.model == PRIMARY_MODEL:
                fb = NebiusLlm(FALLBACK_MODEL, self.api_key, self.base_url)
                return fb.chat(messages, max_tokens, temperature)
            raise RuntimeError("Nebius API HTTP %s: %s" % (e.code, e.read()[:200]))
        except urllib.error.URLError as e:
            raise RuntimeError("Nebius unreachable: %s" % e)
        choices = data.get("choices") or []
        if not choices:
            raise RuntimeError("No choices: %s" % str(data)[:200])
        return choices[0]["message"]["content"]


class MockLlm:
    """Deterministic offline stand-in. Same interface, no network."""

    def chat(self, messages, max_tokens=1200, temperature=0.7):
        last = messages[-1]["content"] if messages else ""
        if "Reply with exactly one line" in last and "OK" in last:
            # Screening prompt: check only the LISTING/DETAIL portion
            # (the prompt template itself mentions "payment" — ignore that)
            marker = "LISTING:"
            listing_part = last.split(marker, 1)[-1].lower() if marker in last else ""
            if any(w in listing_part for w in ("deposit", "minimum balance",
                                               "subscription", "paywall",
                                               "premium", "unlock bidding",
                                               "pay to apply", "registration fee")):
                return "REJECT: requires payment to apply"
            return "OK"
        # Drafting prompt: return a templated truthful proposal
        return (
            "Hello — I'm Michael Woolum's automated bidding assistant. "
            "This proposal was drafted by AI and is delivered under his "
            "personal review.\n\n"
            "I can complete this work as described. I work asynchronously, "
            "deliver on deadline, and communicate clearly in writing.\n\n"
            "Rate and timeline are negotiable — tell me what you need and "
            "I'll confirm I can deliver it before we start.\n\n"
            "Thank you for your consideration.\n"
            "— Michael Woolum (via AI assistant)"
        )


def get_llm():
    """Factory: Nebius when keyed, mock otherwise."""
    if NEBIUS_API_KEY:
        return NebiusLlm()
    return MockLlm()


if __name__ == "__main__":
    llm = get_llm()
    print(type(llm).__name__)
    print(llm.chat([{"role": "user", "content": "Reply with exactly: READY"}],
                   max_tokens=10))
