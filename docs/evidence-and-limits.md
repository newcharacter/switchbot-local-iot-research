# Evidence, Scope, And Impact

This page separates three things that are easy to collapse into each other: what was directly proven, where active testing stopped, and what the result implies for platform validation.

## Directly Proven

- On 2026-04-30, tested cloud-shadow properties accepted modified values, persisted them, and returned them on readback after the vendor's remediation target.
- The modified values were restored immediately.
- A later read-only check confirmed the tested values were readable after restoration.
- Public artifact listing behaviour remained observable.
- Production-facing certificate metadata still contained test-looking material.
- App-derived MQTT authentication evidence remained live in the private retest lane.

## Testing Scope

Active write testing was constrained to accounts and devices I controlled. That was the right ethical boundary.

It should not be misread as proof that the issue was harmless outside that boundary. The observed behaviour belongs to a cloud validation path. The unresolved platform question is how that path enforces ownership, source, type, range, and read-only/device-owned constraints across accounts and device classes.

## Still Open

- Cross-account impact was not tested with a second owned account.
- Writes to non-owned device identifiers were not attempted.
- Physical device state change is not claimed.
- MQTT topic-permission breadth is not publicly assessed.
- Personal user-data exposure is not claimed for the artifact-listing issue.

## Testing Principle

If ownership-isolation impact needs testing, it should be tested only with two accounts and devices controlled by the researcher.

## Conclusion

After vendor acknowledgement and a promised remediation window, retesting showed that at least one server-side cloud-shadow validation issue remained reproducible. Related public artifact, certificate metadata, and MQTT-authentication concerns stayed in the coordinated disclosure lane.

## Public Evidence Table

| Question | Public answer |
|---|---|
| Did the cloud shadow accept unexpected writes during owned-account retesting? | Yes. |
| Were those values returned on readback? | Yes. |
| Were changed values restored? | Yes. |
| Does this prove cross-account impact? | No. It leaves that question open. |
| Does this require physical device mutation to matter? | No. Cloud-shadow state is consumed by apps, dashboards, support tooling, and automations. |
| Are raw reproduction details public here? | No. |
