# Defensive Recommendations

These recommendations are written for anyone building or reviewing consumer IoT platforms. They do not depend on SwitchBot-specific payloads or private evidence.

## 1. Treat Cloud Shadow Writes As A Validation Boundary

Cloud shadows are convenient, but they should not become a bypass around device truth.

Recommended controls:

- enforce ownership on every write path,
- reject writes to device-owned or read-only properties,
- validate type and range server-side,
- separate app-originated updates from device-originated updates,
- log rejected writes with enough context for investigation.

## 2. Make Remediation Testable

The vendor and researcher should be able to agree what "fixed" means.

Good remediation criteria:

- the previously accepted write is rejected,
- the rejection is consistent across regions and accounts,
- readback confirms the shadow value did not change,
- related metadata has been rotated or removed,
- public artifact exposure has been narrowed.

## 3. Avoid Broad Public Artifact Inventory

Known firmware URLs may be necessary for device update flows. Broad public listing is a different issue. It turns delivery infrastructure into an inventory service.

Recommended controls:

- disable unauthenticated listing,
- publish only necessary objects by explicit URL,
- separate debug/internal artifacts from production delivery,
- avoid exposing unreleased or internal-looking paths,
- monitor public buckets or object stores for accidental inventory exposure.

## 4. Keep Production Metadata Clean

Production-facing metadata should not include test-looking certificate material or confusing environment signals. Even if the direct exploitability is low, it erodes trust and complicates incident analysis.

Recommended controls:

- rotate test-looking material out of production paths,
- use environment-specific signing and trust material,
- monitor public metadata for stale test artifacts,
- document expected certificate subjects and rotation windows.

## 5. Scope MQTT Credentials And Topics Tightly

MQTT and event systems are powerful because they sit close to real device behaviour. That also makes them sensitive.

Recommended controls:

- issue narrowly scoped credentials,
- rotate app-derived credentials,
- limit publish and subscribe rights by device, account, and topic class,
- log unexpected topic access,
- keep provisioning paths separate from ordinary app telemetry.

## 6. Design Integrations Around Source Labels

Home automation systems should know where a value came from. A value read from cloud shadow, a value observed locally, and a value reported directly by a device are not equivalent.

Recommended controls:

- keep source labels in integration state,
- prefer local observations where available,
- expose stale or uncertain values honestly,
- avoid overwriting local truth with cloud-shadow convenience fields.
