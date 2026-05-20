"""Sanitized MQTT payload decoder examples.

This module uses synthetic fixtures and generic payload shapes. It does not
contain broker endpoints, credentials, real device identifiers, or raw captures.
"""

from __future__ import annotations

import json
from collections.abc import Iterable
from typing import Any


SENSOR_MODEL_BYTES = {ord("w"), ord("W"), ord("i"), ord("I"), ord("t"), ord("T"), 0x14, 0x15}


def normalise_mac(mac: str) -> str:
    """Return an uppercase MAC-like identifier without separators."""
    return "".join(ch for ch in mac.upper() if ch in "0123456789ABCDEF")


def _mac_variants(mac: str) -> list[tuple[str, bytes]]:
    clean = normalise_mac(mac)
    if len(clean) != 12:
        return []
    raw = bytes.fromhex(clean)
    return [("forward", raw), ("reversed", raw[::-1])]


def _decode_temp_humidity(temp_data: bytes, battery: int | None) -> dict[str, Any] | None:
    if len(temp_data) < 3:
        return None

    sign = 1 if temp_data[1] & 0b10000000 else -1
    temperature = sign * ((temp_data[1] & 0b01111111) + ((temp_data[0] & 0b00001111) / 10))
    humidity = temp_data[2] & 0b01111111

    if not (-50 <= temperature <= 80 and 0 <= humidity <= 100):
        return None
    if temperature == 0 and humidity == 0 and battery == 0:
        return None

    decoded: dict[str, Any] = {
        "temperature": temperature,
        "humidity": humidity,
        "fahrenheit": bool(temp_data[2] & 0b10000000),
    }
    if battery is not None and 0 <= battery <= 100:
        decoded["battery"] = battery
    return decoded


def _parse_meter_service_data(service_data: bytes) -> dict[str, Any] | None:
    if len(service_data) < 6:
        return None

    model = service_data[0] & 0b01111111
    if model not in SENSOR_MODEL_BYTES:
        return None

    battery = service_data[2] & 0b01111111
    decoded = _decode_temp_humidity(service_data[3:6], battery)
    if not decoded:
        return None
    decoded["model_byte"] = model
    decoded["encrypted"] = bool(service_data[0] & 0b10000000)
    return decoded


def _find_known_mac(payload: bytes, known_macs: Iterable[str]) -> dict[str, Any] | None:
    for mac in known_macs:
        clean = normalise_mac(mac)
        for byte_order, needle in _mac_variants(clean):
            offset = payload.find(needle)
            if offset != -1:
                return {
                    "device_id": clean,
                    "mac_offset": offset,
                    "mac_byte_order": byte_order,
                }
    return None


def _candidate_service_offsets(payload: bytes, mac_offset: int | None) -> list[int]:
    offsets: list[int] = []
    if mac_offset is not None:
        offsets.extend([mac_offset + 6, mac_offset + 7, mac_offset + 8])
    offsets.extend(i for i, value in enumerate(payload) if value & 0b01111111 in SENSOR_MODEL_BYTES)

    result: list[int] = []
    seen: set[int] = set()
    for offset in offsets:
        if 0 <= offset <= len(payload) - 6 and offset not in seen:
            seen.add(offset)
            result.append(offset)
    return result


def _decode_sensor_payload(payload: bytes, known_macs: Iterable[str]) -> dict[str, Any]:
    mac_match = _find_known_mac(payload, known_macs)
    mac_offset = mac_match.get("mac_offset") if mac_match else None

    for offset in _candidate_service_offsets(payload, mac_offset):
        decoded = _parse_meter_service_data(payload[offset : offset + 6])
        if not decoded:
            continue
        event = {
            "event_type": "sensor_ble",
            "source": "mqtt",
            "data": decoded,
            "service_data_offset": offset,
            "raw_len": len(payload),
            "confidence": "high" if mac_match else "medium",
        }
        if mac_match:
            event.update(mac_match)
        return event

    event = {
        "event_type": "binary",
        "source": "mqtt",
        "raw_len": len(payload),
        "confidence": "low",
    }
    if mac_match:
        event.update(mac_match)
    return event


def _coerce_property_map(value: Any) -> dict[int, Any]:
    if not isinstance(value, dict):
        return {}

    props: dict[int, Any] = {}
    for key, item in value.items():
        try:
            prop_id = int(key)
        except (TypeError, ValueError):
            continue
        if isinstance(item, dict) and "value" in item:
            props[prop_id] = item.get("value")
        else:
            props[prop_id] = item
    return props


def _extract_shadow_events(obj: Any) -> list[dict[str, Any]]:
    if not isinstance(obj, dict):
        return []

    events: list[dict[str, Any]] = []
    changes = obj.get("changes")
    if isinstance(changes, list):
        by_device: dict[str, dict[int, Any]] = {}
        for change in changes:
            if not isinstance(change, dict):
                continue
            prop_id = change.get("propertyID") or change.get("propertyId")
            device_id = change.get("deviceID") or change.get("deviceId")
            if prop_id is None or device_id is None:
                continue
            try:
                prop_int = int(prop_id)
            except (TypeError, ValueError):
                continue
            by_device.setdefault(str(device_id), {})[prop_int] = change.get("propertyValue")
        for device_id, properties in by_device.items():
            events.append({
                "event_type": "shadow_update",
                "device_id": device_id,
                "properties": properties,
                "source": "mqtt_json_changes",
            })

    device_id = obj.get("deviceID") or obj.get("deviceId")
    for key in ("data", "properties", "property", "reported", "desired"):
        properties = _coerce_property_map(obj.get(key))
        if properties:
            events.append({
                "event_type": "shadow_update",
                "device_id": str(device_id) if device_id else None,
                "properties": properties,
                "source": f"mqtt_json_{key}",
            })

    for value in obj.values():
        if isinstance(value, dict):
            events.extend(_extract_shadow_events(value))
        elif isinstance(value, list):
            for item in value:
                events.extend(_extract_shadow_events(item))

    return events


def decode_payload(
    topic: str,
    payload: bytes,
    known_sensor_macs: Iterable[str] | None = None,
) -> list[dict[str, Any]]:
    """Decode one synthetic MQTT-like message into normalized events."""
    known_sensor_macs = known_sensor_macs or ()
    try:
        parsed = json.loads(payload)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return [_decode_sensor_payload(payload, known_sensor_macs)]

    events: list[dict[str, Any]] = [{
        "event_type": "json",
        "source": "mqtt",
        "topic": topic,
        "payload": parsed,
    }]
    events.extend(_extract_shadow_events(parsed))
    return events
