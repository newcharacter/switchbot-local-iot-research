# Research Map

The private SwitchBot workspace is larger than the public vulnerability note. This page maps the workstream at a public level so the repo shows the breadth of the project without exposing raw evidence.

## 1. App And Cloud API Mapping

The project began by comparing the official developer API with the app-facing API surface. The official API exposed only a small set of commands for the K10+ Pro vacuum. The app-facing layer exposed a much richer state model: device state, writable settings, action dispatch, rooms, scenes, firmware metadata, home context, and shadow properties.

Public value:

- shows ability to map a real mobile/cloud system,
- explains why the public API did not represent the whole platform,
- gives context for the cloud-shadow validation finding.

Private material kept out:

- exact endpoints,
- request bodies,
- live identifiers,
- authentication material.

## 2. K10+ Pro Control Surface

The K10+ Pro work mapped settings, commands, consumables, schedules, and status fields beyond the public API. It showed that the device has a broader programmable surface than the public integration suggests.

Public value:

- demonstrates protocol and state-model reconstruction,
- supports the Home Assistant/local-control thread,
- explains why remediation validation needed a harness rather than manual app testing.

Private material kept out:

- full property tables,
- live device identifiers,
- account and group context.

## 3. Cloud Shadow Property Sweep

The project scanned property ranges across the vacuum, Hub Mini, and temperature/humidity sensors to identify which numeric properties actually returned data. That work connected cloud-shadow IDs to real concepts such as battery, temperature, humidity, dewpoint, absolute humidity, VPD, device metadata, and vacuum state.

Public value:

- explains why the cloud-shadow validation issue matters,
- shows that the finding came from systematic mapping rather than guessing,
- motivates source-labeled state in the local-control prototype.

Private material kept out:

- exact sensitive property payloads,
- raw scans,
- private room/device/account metadata.

## 4. Disclosure And Retest Harness

The disclosure work produced the strongest public story: report, vendor acknowledgement, remediation target, owned-account retest, restoration, read-only confirmation, and follow-up.

Public value:

- demonstrates responsible disclosure,
- demonstrates remediation validation rather than one-off bug finding,
- keeps proven impact separate from untested risk.

Private material kept out:

- raw proof artifacts,
- vendor thread contents,
- exact reproduction payloads.

## 5. Public Artifact And Metadata Review

The project also reviewed public-facing artifact delivery and certificate metadata. Those findings were kept at a high level publicly because the raw evidence can become an enumeration guide if published carelessly.

Public value:

- shows broader platform hygiene review,
- produces defensive recommendations for artifact distribution and metadata rotation,
- supports the case that remediation should cover more than one code path.

Private material kept out:

- object listings,
- exact paths,
- certificate bodies,
- raw firmware artifacts.

## 6. Firmware And IR Database Archaeology

The private workspace includes firmware diffing, debug-artifact review, and IR database format analysis. That work is not necessary to reproduce the security findings, but it shows the wider reverse-engineering depth behind the local-control direction.

Public value:

- demonstrates binary/artifact analysis,
- explains the Hub Mini and IR control context,
- supports the claim that the project was broader than a single HTTP finding.

Private material kept out:

- vendor firmware files,
- APK/database extracts,
- raw object inventories.

## 7. Home Assistant Integration Work

The private integration work created a custom Home Assistant direction for vacuum state, sensor metrics, consumables, switches, numbers, remote/IR control, and realtime MQTT/BLE update merging. The public repo keeps only a synthetic decoder example and architecture notes.

Public value:

- turns the research into practical engineering,
- shows how local observations can be merged with cloud state,
- demonstrates why source labels matter in home automation.

Private material kept out:

- credential prompts and real configuration,
- real device IDs,
- live MQTT topics,
- raw captures.

## 8. Remaining Unknowns

The project still has open questions, and the public repo should be honest about them:

- cross-account impact was not tested with a second owned account,
- physical device mutation was not claimed,
- MQTT topic permission breadth was not publicly assessed,
- some schedule/map/camera paths sit behind signing layers not covered in the public example,
- live Hub BLE relay capture still needs more data.

That honesty is part of the project quality. The repo is direct about what was found, but it does not inflate uncertainty into proof.
