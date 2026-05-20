#!/usr/bin/env python3
"""Decode synthetic SwitchBot-like messages.

This demo intentionally uses synthetic fixtures. It does not connect to
SwitchBot, load credentials, or read private captures.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from switchbot_research.mqtt_decoder import decode_payload  # noqa: E402


def load_payload(message: dict[str, Any]) -> bytes:
    encoding = message.get("encoding")
    payload = message.get("payload")

    if encoding == "hex" and isinstance(payload, str):
        return bytes.fromhex(payload)
    if encoding == "json":
        return json.dumps(payload).encode()

    raise ValueError(f"Unsupported synthetic message encoding: {encoding!r}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Path to synthetic message JSON file")
    args = parser.parse_args()

    messages = json.loads(args.path.read_text())
    decoded: list[dict[str, Any]] = []

    for message in messages:
        events = decode_payload(
            topic=message["topic"],
            payload=load_payload(message),
            known_sensor_macs=message.get("known_sensor_macs", ()),
        )
        decoded.append({
            "name": message["name"],
            "events": events,
        })

    print(json.dumps(decoded, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
