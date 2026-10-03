#!/usr/bin/env python3
"""GigAgent web demo — shows the Nemotron-powered agent screening listings
and drafting proposals live. For the hackathon demo video and judge testing.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, jsonify
from gigagent.llm import get_llm, NebiusLlm
from gigagent.agent import run_demo, DEMO_LISTINGS, PROFILE, DISCLOSURE
from gigagent.screener import screen_listing
from gigagent.drafter import draft_proposal

app = Flask(__name__)


@app.route("/")
def index():
    llm = get_llm()
    provider = type(llm).__name__
    model = getattr(llm, "model", "mock") if isinstance(llm, NebiusLlm) else "mock"
    return render_template("index.html", provider=provider, model=model,
                           listings=DEMO_LISTINGS)


@app.route("/api/run", methods=["POST"])
def api_run():
    llm = get_llm()
    results = run_demo(llm)
    return jsonify({"provider": type(llm).__name__, "results": results})


@app.route("/api/screen", methods=["POST"])
def api_screen():
    data = request.json
    llm = get_llm()
    ok, reason = screen_listing(data.get("title", ""), data.get("detail", ""), llm)
    return jsonify({"ok": ok, "reason": reason,
                    "provider": type(llm).__name__})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=False)
