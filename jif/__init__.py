"""jif: the if statement, finally powered by AI."""
import json
import os
import re
import sys
import time
import types
import urllib.request

__all__ = ["jif", "last_probability"]

URL = "https://ai-gateway.vercel.sh/v4/ai/evaluation-model"
MODEL = "typesafe-ai/jev"
last_probability = None  # calibrated confidence of the most recent branch. Enterprise observability.

_CHAIN = re.compile(r"[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*")


def _resolve(chain, scope):
    head, *rest = chain.split(".")
    v = scope[head]
    for attr in rest:
        v = getattr(v, attr)
    return v


def _variables(expr, scope):
    out = {}
    for chain in dict.fromkeys(_CHAIN.findall(expr)):
        try:
            v = _resolve(chain, scope)
        except (KeyError, AttributeError):
            continue
        if not isinstance(v, types.ModuleType) and not callable(v):
            out[chain] = repr(v)[:500]  # ponytail: truncation, the model doesn't need your whole DataFrame
    return out


def ask(expr, variables):
    """One branch, one frontier-model call."""
    global last_probability
    key = os.environ.get("AI_GATEWAY_API_KEY")
    if not key:
        raise RuntimeError("jif needs AI_GATEWAY_API_KEY. Branching is a premium feature.")
    state = "Variables:\n" + "".join(f"{k} = {v}\n" for k, v in variables.items()) + f"Expression: {expr}"
    body = {"state": state, "questions": {"answer": {
        "type": "boolean",
        "instructions": "Given the variable values, is the expression true?",
    }}}
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), headers={
        "authorization": f"Bearer {key}",
        "content-type": "application/json",
        "ai-model-id": MODEL,
        "ai-evaluation-model-specification-version": "4",
        "ai-gateway-auth-method": "api-key",
        "ai-gateway-protocol-version": "0.0.1",
    })
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                last_probability = json.load(r)["answers"]["answer"]["probability"]
            return last_probability
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == 3:
                raise RuntimeError(f"jev said {e.code}: {e.read().decode()}") from None
            time.sleep(2 ** attempt)  # Jev is busy deciding other people's if statements


def jif(expr, _depth=1):
    """`if jif("x > 5"):` -- evaluates the expression the modern way."""
    f = sys._getframe(_depth)
    scope = {**f.f_globals, **f.f_locals}
    return ask(expr, _variables(expr, scope)) >= float(os.environ.get("JIF_THRESHOLD", 0.5))
