# Ironwood Parking Team Dashboard — Spec (v2.0)

## Status
- v1.0 shipped as a working prototype (CCB monthly-export based, in-browser edit mode). Superseded by this v2.0 direction before real rollout — not carrying the old edit UI forward.
- The CCB group itself is being renamed **Parking Team** (from Parking Lot) as Campus Greeters get migrated off, within the week of Jul 28, 2026.
- Design direction (palette, layout, flags) approved 2026-07-28 against an interactive mockup built with sample data.

## Scope
- Primary focus: the **Parking Team roster** — the post-purge list from the July 2026 CCB audit — not the general Campus Team.
- People who also serve Campus Greeter stay visible (Brad Hall, Justus Norgord, Daniel Stewart, Jamie Weems per the July 2026 audit), tracked through the general **Also Serves** field below rather than a special "dual" case.
- Known reassignment: **Scott Marsh** — Parking Lot/Team leadership (Shift 2 lead), not a one-time Greeter fill-in. Already reflected in the July 2026 audit.

## Data source & refresh model
- Primary source going forward: each person's CCB profile → **Involvement → Serving** tab
  (`https://ironwoodchurch.ccbchurch.com/goto/individuals/{ID}`) — gives real per-Sunday
  shift history (date, position, shift, accepted/declined), far more precise than the old
  monthly Yes/blank export.
- No CCB API for now — CCB is slated to be replaced, so it's not worth pursuing API access.
  All pulls happen via Claude driving Mark's signed-in Chrome, on request.
- **One-time legacy pull**: visit every current Parking Team member's profile once to backfill
  full serving history.
- **Ongoing refresh**: ask Claude to re-pull (everyone, or specific people) whenever an update
  is needed — no live/automatic sync.
- **Roster audit**: a repeatable workflow (built as a project skill) that compares the live CCB
  group member list against our data, to catch anyone added or removed that we missed.
- **Manual corrections** (e.g. Jacob, who serves but doesn't sign up in CCB) live in a small
  `data/corrections.json`, edited by Claude from plain-language prompts — "Jacob served every
  week this month," "add Bob Smith" — not a live in-browser edit feature.
- **No-shows** are the mirror case: CCB records a signup as served even when the person didn't
  actually show up. Also handled in `data/corrections.json`, as a `removedServedDates` entry
  that cancels out the matching date/position/shift once it shows up in a pull, from a
  plain-language prompt — "Jonathan no-showed his Aug 9 shift."

## Fields (per person)
- Name, CCB System ID
- **Shift**: 1, 2, or 3 — a person can hold more than one (e.g. Jacob: 2/3)
- **Status**: Active / Inactive / New (CCB's own designation)
- **Also Serves**: every other role/ministry a person serves, inside Campus Team (e.g. Campus
  Greeter) or elsewhere (e.g. Communion Prep, BUILD Leadership) — a list/count, not capped at 2
- **Serving Rotation**: Weekly / Bi-Weekly / Seasonal — not in the CCB data, set manually per
  person. Describes *frequency*, separate from Dedicated Shift Team below.
- **Dedicated Shift Team**: Shift 1 / Shift 2 / Shift 3, or none — set manually by Mark
  (`DEDICATED_TEAM` in `scripts/build_seed_data.py`), not inferred from serving history. This is
  someone's actual team assignment; covering a different shift one week doesn't change it.
  Drives the Shift 1/2/3 tabs on the dashboard (added 2026-09-14, replacing the old behavior of
  grouping by whichever shift a person most recently served).
- Per-Sunday serving history (from the Involvement > Serving pull)
- Joined date

## Attendance & flags
- **Needs Review**: a Dedicated Shift Team member who hasn't served their last ~3 expected
  Sundays, with no correction on file. Only applies to people with a Dedicated Shift Team --
  Irregular people are expected to have gaps, so they're never flagged (changed 2026-09-14;
  previously applied to anyone Active).
- **Multi-Shift Sunday**: flagged when someone serves more than one position/shift the same
  Sunday.
- **Served Once / Never Served**: merged into a single bucket, not tracked separately.

### Burnout Warning
- **Only applies to Weekly rotation.** Bi-Weekly and Seasonal are excluded entirely, not just
  slower to trigger — a known non-Weekly pattern already tells us what to expect, so gaps there
  aren't a burnout signal.
- Trigger: served every expected turn with **zero weeks off for ~12 consecutive weeks (3
  months)**.
- Faster trigger for higher load: Weekly volunteers also flagged Multi-Shift Sunday or with 2+
  Also-Serves roles drop to a **~6 consecutive week** no-break threshold.
- A single Sunday off resets the streak to zero — flags *no break*, not raw frequency.
- Mirror image of Needs Review (too little vs. too much, with no rest) — the two should never
  fire on the same person at once.
- Thresholds (12 / 6 weeks) are a starting point, tune once seen against real streaks.

## UI
- Filter by **Shift 1 / Shift 2 / Shift 3 / Irregular / New** — Shift 1/2/3 show each shift's
  Dedicated Shift Team; everyone without one (occasional help, long-dormant, not yet assigned)
  falls into Irregular. Renamed from "Seasonal" 2026-09-14 to avoid clashing with the Serving
  Rotation value of the same name.
- Sort by name, frequency, or last served.
- Click a person to expand: per-week served history, join date, Also Serves, Burnout Warning
  detail when it applies.
- At-a-glance status pill on every row (Active / Needs Review / Inactive / New).
- **No in-browser editing.** Read-only dashboard — every correction or addition happens by
  telling Claude, which edits the committed data and republishes. No passcode, no edit mode.
- Audience: primary is Mark's own working view; secondary is clean enough to share with
  leadership.

## Visual identity
- Ironwood green (`#6e9277`) as the single brand accent — chrome, navigation, role badges
  (e.g. Shift Lead) — never used as a status color.
- Status colors kept deliberately separate from the brand accent: steel blue = Active,
  terracotta = Needs Review / Burnout Warning, gold/tan = New, gray = Inactive.
- Ironwood tree mark in the header, cropped from the church's own parking-lot map PDF.
- Monospace for data/dates/shift tags (manifest/duty-roster feel); bold sans for names, since
  those need to stay the most scannable thing on the page.

## Access & sharing
- Host as a static page (e.g. GitHub Pages) — accessible anywhere, no more iPhone-shortcut
  dependency.
- Public repo/page is fine — there's no edit surface left to protect, so no passcode needed.

## Future (not this build)
- Cowork-based auto-update: reduce the manual "hand Claude a CSV / ask for a refresh" step
  further.
- CCB API access, if it ever becomes worth pursuing (deprioritized — CCB is being replaced).

## Background context
- Co-leaders (volunteer side): Ali, Tim, Heidi (Campus Team + small group).
- Broader vision: fuller church health dashboard (serving, giving, attendance, groups) pulling
  from CCB + Pushpay APIs.
