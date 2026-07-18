from __future__ import annotations

import json
import random
from datetime import UTC, datetime, timedelta
from pathlib import Path

ROOTS = {
    "deadlock": {
        "message": "checkout worker timed out acquiring inventory_lock",
        "stack": ["cart.reserve", "inventory.lock_stock", "db.wait_for_lock"],
    },
    "schema_drift": {
        "message": "payment payload missing required field customer_tier",
        "stack": ["payments.decode", "schemas.validate_order", "api.checkout"],
    },
    "cache_poison": {
        "message": "profile cache returned mismatched tenant scope",
        "stack": ["profiles.load", "cache.deserialize", "tenant.guard"],
    },
    "rate_limit": {
        "message": "webhook delivery exhausted provider retry budget",
        "stack": ["webhooks.deliver", "providers.post_event", "retry.backoff"],
    },
    "timezone": {
        "message": "billing window closed before local midnight conversion",
        "stack": ["billing.close_window", "timezones.to_customer_day", "invoices.emit"],
    },
}


def synthetic_jsonl(count: int = 500, seed: int = 42) -> str:
    rng = random.Random(seed)
    start = datetime(2026, 7, 1, tzinfo=UTC)
    lines: list[str] = []
    root_names = list(ROOTS)
    for index in range(count):
        root = root_names[index % len(root_names)]
        spec = ROOTS[root]
        request_id = f"req_{rng.randrange(10**8, 10**10)}"
        user_id = rng.randrange(1000, 9999)
        timestamp = start + timedelta(minutes=index * 3 + rng.randrange(0, 3))
        frame_path = f"/srv/app/releases/{rng.randrange(100, 999)}/{root}.py"
        stack = "\n".join(
            f'  File "{frame_path}", line {20 + pos}, in {frame}'
            for pos, frame in enumerate(spec["stack"])
        )
        noisy_suffix = rng.choice(
            [
                f" request_id={request_id}",
                f" user={user_id}",
                f" trace={request_id} duration_ms={rng.randrange(20, 700)}",
            ]
        )
        payload = {
            "timestamp": timestamp.isoformat().replace("+00:00", "Z"),
            "level": "ERROR",
            "service": rng.choice(["api", "worker", "scheduler"]),
            "message": f"{spec['message']}{noisy_suffix}",
            "stack": stack,
            "root_cause": root,
        }
        lines.append(json.dumps(payload, sort_keys=True))
    return "\n".join(lines) + "\n"


def write_synthetic(path: Path, count: int = 500, seed: int = 42) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(synthetic_jsonl(count=count, seed=seed), encoding="utf-8")
