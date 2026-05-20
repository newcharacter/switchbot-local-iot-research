# Disclosure Timeline

## 2026-03-14

Initial vulnerability disclosure sent to SwitchBot Security.

Reported areas:

- Cloud-shadow write validation.
- Public artifact listing exposure.
- Test-looking certificate material in production-facing metadata.

## 2026-03-24

SwitchBot Security replied.

They stated that two of the reported areas were expected to be fully remediated by the end of March 2026. They treated the public artifact listing issue as lower priority because of legacy firmware concerns and because they had not identified direct user-data leakage.

## 2026-04-30

Owned-account retesting was performed after the remediation window.

Results:

- The cloud-shadow validation issue still reproduced in the cloud path under owned-account testing.
- Public artifact listing behaviour was still observable.
- Test-looking certificate metadata remained visible.
- Related MQTT authentication evidence remained active and was kept private.

## 2026-04-30 Follow-Up

A follow-up was sent in the same vendor thread. It stated that the remediation did not appear complete, avoided claiming cross-account impact as proven, and kept raw evidence available for coordinated review.

## Current Posture

No raw exploit details are published here. The public repo exists to document the research, the retest discipline, and the local-control engineering direction.
