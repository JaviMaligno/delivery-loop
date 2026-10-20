---
name: qa-execution
description: Use to execute a QA plan against a deployed non-production environment — walk each ID, capture evidence (screenshots, recordings, queries, logs), hunt bugs outside the spec that surface while verifying, clean up test data, and report per-ID status plus a separate bug list. Triggers: "run the QA plan", "verify the spec in the deployed env", "capture evidence per ID", or once a `qa-design` plan exists. Tool-agnostic.
---

# QA execution

in: QA plan (else run `qa-design`) · env URL from profile (never production — invariant) · auth method · cleanup owner = you.
out: plan doc with statuses + evidence pointers · bug list apart · cleanup confirmed.

## Capture tool per ID (first match)
1. async side effect (job ran, row created, status flipped) → data query on test env.
2. pipeline / queue / schedule timing or failure → logs of the closest surface.
3. hover, focus, tooltip text, animation, awkward multi-step flow → interactive browser driver.
4. visual/layout/text on reachable page → profile's `live-verification.ui` tool.
5. UI claim backed by data → both.
- profile or project skill pins a tool → use it; no ad-hoc wrapper scripts around it.
- none pinned and several available → pick by the list above; say which.

## Per ID
pre-condition (fixture with prefix `QA-<feature>-<ts>-`) → steps → capture at named path → compare → status + one-line note with evidence path.
honesty: can't capture → say so; never ✅ from code reading; capture ≠ expected → not verified, find why.
browser driver: confirm viewport non-zero and page visible before trusting interactions.

## Bug hunt (separate output)
| pattern | looks like |
|---|---|
| unresolved i18n placeholder | literal `{count}` in UI |
| hardcoded string in localised UI | one string in the wrong language |
| broken markup | literal comment/HTML markers in rendered output |
| stuck async pipeline | status stuck pending; stale queue messages |
| opaque indicator | colour/badge/value without explanation |
| producer/consumer mismatch | app writes to queue A, worker reads B |
| auto-apply gap | suggestion stored, target field never written |
| data leak to external party | internal names in outbound content |
| default tab hides results | default view empty after a fix |
each bug: where (file/route) · severity (blocks-merge · important · minor) · suggested fix.

## Regression smoke
run the plan's smoke sections; before/after compare in same env when baseline exists.

## Cleanup
delete every prefixed fixture, upload, draft; verify zero remain; reset toggles. Keep only what the user asked to keep.

## Report
coverage table first (`| ID | status | note |`), then bugs, then smoke. ✅ = PASS · ⚠️ = PASS + note · ❌/🔄 → escalate, never close silently.
