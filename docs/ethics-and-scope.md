# Ethics And Scope

Active testing was constrained to my own SwitchBot account and devices. I kept the raw evidence private and reported findings to the vendor through responsible disclosure.

That testing boundary matters. It is also easy to misread. It means I did not touch anyone else's devices or accounts. It does not mean the cloud-shadow validation issue is only interesting on my account; the observed acceptance happened in the cloud path.

## Scope

- Testing was limited to devices and accounts I controlled.
- Cross-account impact was not tested.
- Raw captures, identifiers, credentials, and vendor correspondence stayed out of this public repo.
- Claims are phrased around observed behaviour, not worst-case speculation.

## Disclosure

The findings were reported to SwitchBot Security. After the vendor gave a remediation window, I retested the affected areas on owned devices and followed up when the retest did not match the expected outcome.

That remediation-validation loop matters: not just finding a bug, but keeping evidence clean enough to check whether it was actually fixed.

## Local-Control Thread

The same investigation also pointed toward a practical Home Assistant direction. Cloud APIs can be useful, but local observability and local automation reduce reliance on opaque vendor state. The decoder example in this repo is a small, sanitized slice of that local-control work.

## What This Repo Leaves Out

The private workspace contains the material needed for vendor follow-up. This public repo leaves out raw requests, raw MQTT payloads, reusable authentication material, firmware dumps, private identifiers, vendor correspondence, and reproduction steps.
