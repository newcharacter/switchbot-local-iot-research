#!/usr/bin/env python3
"""Regression tests for the sanitized MQTT decoder example."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from switchbot_research import mqtt_decoder  # noqa: E402


def assert_equal(actual, expected, label: str) -> None:
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected!r}, got {actual!r}")


def sensor_payload(mac: str, service_data: bytes, reversed_mac: bool = False) -> bytes:
    mac_bytes = bytes.fromhex(mac)
    if reversed_mac:
        mac_bytes = mac_bytes[::-1]
    return mac_bytes + service_data


def test_normalise_mac() -> None:
    assert_equal(mqtt_decoder.normalise_mac("aa:bb-cc dd.ee.ff"), "AABBCCDDEEFF", "normalise_mac")


def test_forward_mac_sensor_payload() -> None:
    service_data = bytes([ord("W"), 0x00, 88, 0x05, 0x93, 50])
    events = mqtt_decoder.decode_payload(
        "synthetic/topic",
        sensor_payload("AABBCCDDEEFF", service_data),
        {"AABBCCDDEEFF"},
    )
    event = events[0]
    assert_equal(event["event_type"], "sensor_ble", "event type")
    assert_equal(event["device_id"], "AABBCCDDEEFF", "device id")
    assert_equal(event["mac_byte_order"], "forward", "byte order")
    assert_equal(event["data"]["temperature"], 19.5, "temperature")
    assert_equal(event["data"]["humidity"], 50, "humidity")
    assert_equal(event["data"]["battery"], 88, "battery")


def test_reversed_mac_sensor_payload() -> None:
    service_data = bytes([ord("w"), 0x00, 77, 0x07, 0x91, 64])
    events = mqtt_decoder.decode_payload(
        "synthetic/topic",
        sensor_payload("AABBCCDDEEFF", service_data, reversed_mac=True),
        {"AABBCCDDEEFF"},
    )
    event = events[0]
    assert_equal(event["event_type"], "sensor_ble", "event type")
    assert_equal(event["mac_byte_order"], "reversed", "byte order")
    assert_equal(event["data"]["temperature"], 17.7, "temperature")
    assert_equal(event["data"]["humidity"], 64, "humidity")
    assert_equal(event["data"]["battery"], 77, "battery")


def test_unknown_binary_payload() -> None:
    events = mqtt_decoder.decode_payload(
        "synthetic/topic",
        b"\x01\x02\x03",
        {"AABBCCDDEEFF"},
    )
    assert_equal(events[0]["event_type"], "binary", "event type")
    assert_equal(events[0]["confidence"], "low", "confidence")


def test_json_changes_shadow_update() -> None:
    payload = json.dumps({
        "changes": [
            {"deviceID": "DEVICE1", "propertyID": 820, "propertyValue": 77},
            {"deviceID": "DEVICE1", "propertyID": "830", "propertyValue": 215},
        ]
    }).encode()
    events = mqtt_decoder.decode_payload("synthetic/topic", payload, set())
    shadow_events = [event for event in events if event["event_type"] == "shadow_update"]
    assert_equal(len(shadow_events), 1, "shadow event count")
    assert_equal(shadow_events[0]["device_id"], "DEVICE1", "device id")
    assert_equal(shadow_events[0]["properties"], {820: 77, 830: 215}, "properties")


def test_json_property_map_shadow_update() -> None:
    payload = json.dumps({
        "deviceID": "DEVICE2",
        "data": {
            "820": {"value": 99},
            "831": 55,
        },
    }).encode()
    events = mqtt_decoder.decode_payload("synthetic/topic", payload, set())
    shadow_events = [event for event in events if event["event_type"] == "shadow_update"]
    assert_equal(shadow_events[0]["device_id"], "DEVICE2", "device id")
    assert_equal(shadow_events[0]["properties"], {820: 99, 831: 55}, "properties")


def main() -> None:
    tests = [
        test_normalise_mac,
        test_forward_mac_sensor_payload,
        test_reversed_mac_sensor_payload,
        test_unknown_binary_payload,
        test_json_changes_shadow_update,
        test_json_property_map_shadow_update,
    ]
    for test in tests:
        test()
    print(f"{len(tests)} MQTT decoder tests passed")


if __name__ == "__main__":
    main()
