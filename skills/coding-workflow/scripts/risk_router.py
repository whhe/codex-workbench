#!/usr/bin/env python3
"""Route impact-qualified signals using the canonical risk policy."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def classify(data: dict, policy: dict) -> dict:
    signals = data.get("signals", data)
    rules = policy["rules"]
    deep = [key for key in rules["deep_engineering"] if signals.get(key)]
    standard = [key for key in rules["standard_engineering"] if signals.get(key)]
    product_deep = [key for key in rules["deep_product"] if signals.get(key)]
    product_standard = [key for key in rules["standard_product"] if signals.get(key)]
    mode = "deep" if deep or product_deep else "standard" if standard or product_standard else "light"
    reasons = deep + ["product:" + key for key in product_deep] if mode == "deep" else standard + ["product:" + key for key in product_standard]
    adapters = set()
    if any(signals.get(key) for key in ("multi_step_interaction", "cross_view_state")):
        adapters.update(("state", "browser"))
    if any(signals.get(key) for key in ("persistent_state", "retry_semantics", "concurrency")):
        adapters.add("state")
    if int(signals.get("failed_fix_count", 0) or 0) >= rules["recovery_threshold"]:
        adapters.update(("debug", "recovery"))
    return {
        "schema_version": 2,
        "mode": mode,
        "dimensions": {
            "engineering": "high" if deep else "medium" if standard else "low",
            "product": "high" if product_deep else "medium" if product_standard else "low",
            "authority": "high" if signals.get("authorization_boundary") or signals.get("external_write") else "low",
        },
        "reasons": sorted(set(reasons)) or ["no_standard_or_deep_signal"],
        "required_adapters": sorted(adapters),
        "signals": signals,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--policy", default=str(ROOT / "references/risk-policy.json"))
    parser.add_argument("--output")
    args = parser.parse_args()
    result = classify(json.loads(Path(args.input).read_text()), json.loads(Path(args.policy).read_text()))
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(text)
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
