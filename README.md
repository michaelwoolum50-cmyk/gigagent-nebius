# 🤖 GigAgent — Autonomous Gig-Work Agent

**Powered by NVIDIA Nemotron on Nebius Token Factory.**
Built for the [Nebius × NVIDIA Global AI Hackathon](https://nebiusglobalaihackathon.devpost.com/) — **Best Apps & Agents** track.

GigAgent is an autonomous AI agent that finds real gig work, screens out scams and paywalls, drafts truthful proposals with AI disclosure, and files applications. People who need gig income can actually use it.

## How it works

1. **Screen** — Nemotron checks every listing against the never-pay rule: if a listing requires *any* payment, deposit, or subscription from the applicant, it's an instant hard pass.
2. **Draft** — For clean listings, Nemotron drafts a tailored, truthful proposal. Every proposal discloses it's AI-drafted under human review. It never claims to be human and never invents credentials.
3. **File** — The agent files the application and records a receipt.

## NVIDIA Nemotron on Nebius Token Factory

This is the required inference path. The agent talks to the OpenAI-compatible Token Factory API:

| | |
|---|---|
| Base URL | `https://api.tokenfactory.nebius.com/v1/` |
| Env | `NEBIUS_API_KEY` (never committed) |
| Primary model | `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B` |
| Fallback | `nvidia/nemotron-3-super-120b-a12b` |

Token Factory is what makes the agent shippable: one key, OpenAI-compatible API, NVIDIA open weights, no model hosting.

`--offline` (no key) runs the same loop with a deterministic mock — CI, judges, and airplane mode all work.

## Quick start

```bash
git clone https://github.com/michaelwoolum50-cmyk/gigagent-nebius.git
cd gigagent-nebius
pip install -r requirements.txt
cp .env.example .env   # put NEBIUS_API_KEY here (or leave empty for mock mode)

# CLI — screens 3 demo listings, drafts proposals for the clean ones
python3 -m gigagent.agent

# Web demo — http://localhost:5050
python3 demo/app.py
```

## Evaluation

Screening accuracy fixtures live in `evals/test_cases.json` (5 cases: 2 clean, 3 paywall/scam).

## Feedback on Nebius

Token Factory's OpenAI-compatible API made integration trivial — the whole LLM layer is ~60 lines. Nemotron-3-Nano-30B is fast and follows the screening instructions precisely. The playground was useful for prompt iteration before wiring the API.

## License

Apache 2.0 — see [LICENSE](LICENSE).
