# Phase 1 — spec

in: full source — ticket per `tracker.read-rule` (default: description + comments + attachments + linked docs) | whole document | request.
out: inventory (skill `spec`, written in the delivery dir): stable IDs, verbatim quotes, surface, status.
done-when: every source point has an ID or an exclusion reason.

behaviours:
- read the source entire; never a summary. Ticket already fixing scope/split → respect it.

capabilities: tracker, live-verification (current behaviour, large only).
absent: tracker none → source is the document or request.
size-variants: large → baseline inventory of current behaviour first (each capability with an ID → regression contract); parallel readers with different lenses + completeness critic.
skip-when: trivial (mini-inventory from phase 0).
