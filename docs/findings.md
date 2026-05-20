# Findings

This page summarizes the public findings without payloads, identifiers, raw captures, connection details, or reproduction steps.

## Summary Matrix

| Finding | Evidence level | Public status | Main limit |
|---|---|---|---|
| Cloud-shadow validation failure | Cloud-side write/readback on owned account | Still reproduced after vendor target | Cross-account impact untested, not disproven |
| Public artifact inventory exposure | Public unauthenticated observation | Still observable after retest | No personal-data claim |
| Production metadata hygiene | Public metadata observation | Still observable after retest | No standalone exploitability claim |
| MQTT authentication result | Private retest evidence | Kept private | Topic permissions not publicly assessed |

## 1. Cloud-Shadow Validation Failure

The core issue was a cloud validation failure. Tested shadow properties accepted modified values, persisted those values, and returned them on readback after SwitchBot's remediation target. The retest harness restored the original values immediately, and a later read-only check confirmed the restoration.

Active mutation stayed inside my own account and devices. That is the ethical line of the test, not a conclusion that the bug class was only meaningful there. The security question is whether the shared cloud-shadow write path enforces ownership, source, type, range, and device-owned/read-only constraints before accepting updates.

Public conclusion:

> After SwitchBot's remediation target, the cloud-shadow write path still accepted and returned unexpected values for tested device-owned/read-only shadow properties.

Boundary:

- Cross-account impact was not tested with a second owned account.
- Writes to non-owned devices were not attempted.
- Physical device mutation is not the claim; cloud-shadow acceptance and readback are.

## 2. Public Artifact Inventory Exposure

The retest found that public artifact listing behaviour remained observable. The issue is not merely that firmware can be downloaded by known URL. The stronger concern is inventory exposure: public listing turns delivery infrastructure into a map of vendor artifacts and internal-looking material.

Public conclusion:

> Public artifact delivery remained broader than necessary for a narrow firmware distribution path.

Boundary:

- Personal user-data leakage is not claimed.
- Complete current enumeration of all objects is not claimed.

## 3. Production Metadata Hygiene

After the vendor's expected remediation window, public certificate metadata still included test-looking material that had been reported earlier.

Public conclusion:

> Production-facing metadata still contained test-looking certificate material after the remediation target.

Boundary:

- Direct exploitability from that metadata alone is not claimed.
- A complete assessment of the signing or trust chain is not claimed.

## 4. MQTT Authentication Result

The private retest also showed that app-derived MQTT authentication material could still authenticate. This is intentionally not expanded in the public repo because connection details, certificate material, and topic names would move too close to operational guidance.

Public conclusion:

> MQTT/local-control work remained relevant and was kept in the private disclosure lane.

Boundary:

- Effective topic-permission breadth is not publicly claimed.
- Access to other users' topics is not claimed.
- A complete public MQTT security analysis is not claimed.

## Overall Status

The 2026-04-30 retest indicated that remediation was not complete for the cloud-shadow validation finding. The public repo presents the research and engineering story; the raw evidence remains reserved for coordinated vendor follow-up.

## Why The Cloud Finding Is Strong

- It tested the cloud path after a vendor remediation target.
- It used readback rather than assuming a write succeeded.
- It restored the changed values.
- It confirmed restoration later with a read-only check.
- It separates ethical test scope from platform impact analysis.
- It does not need physical device mutation to matter: apps and automations consume cloud-shadow state.
