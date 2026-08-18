You're helping me update the Ironwood Campus Team dashboard with this
past week's serving data. Work in the Ember/Ironwood/ repo.

1. Load `data/seed-data.json` and note its `generatedAt` date — that's
   the last time the dashboard was refreshed from CCB.

2. Do a live CCB pull for the full current roster (everyone listed in
   `PEOPLE` in `scripts/build_seed_data.py`). For each person, drive my
   signed-in Chrome to their CCB profile
   (`https://ironwoodchurch.ccbchurch.com/goto/individuals/{ID}`) →
   Involvement → Serving, and read off any per-Sunday entries (date,
   position, shift, accepted/declined) newer than `generatedAt`. Also
   note any new "Also Serves" activity.

3. Add whatever CCB shows into each person's `served` list in
   `scripts/build_seed_data.py` (and `alsoServes` if it changed). This
   is raw pull data, not a correction — it goes straight into `PEOPLE`,
   the same way the existing history was built.

4. Once the pull is done, tell me a short summary of what's new (who
   served, what shift, anything odd), then ask plainly whether
   anything needs correcting — don't make me fill out a form. Cover
   specifically:
   - No-shows: CCB marks a signup as served even if the person didn't
     actually show. Ask if anyone on the new list was really a
     no-show.
   - Off-CCB serves: some people serve without signing up in CCB (e.g.
     Jacob), so the pull won't show them at all. Ask if anyone did
     that this week.
   - Anything else worth noting that CCB wouldn't have caught.

5. If someone's new entry doesn't match their normal rotation (e.g. a
   Greeter covering Parking, a different shift than usual, two shifts
   same day), flag it back to me in one line so I can confirm before
   you save it. Don't silently assume.

6. Write any confirmed no-shows / off-CCB serves to `data/corrections.json`
   following the existing pattern (`addedServedDates` /
   `removedServedDates`, matched by date + position + shift, with a
   note and `recordedBy`).

7. Apply the same logic already built into the dashboard: track against
   known serving rotation, not raw week-by-week check-in. Someone on a
   weekly rotation who's just absent stays "serves weekly," not
   lapsed.

8. Preserve dual-role handling for anyone who serves both Parking and
   Greeter — don't drop them from either roster.

9. Once I confirm everything's right, bump `PULL_DATE` in
   `scripts/build_seed_data.py` to today, rerun the script to
   regenerate `data/seed-data.json`, and tell me exactly what changed
   in plain language — no code dump.

This replaces asking me to recall the week from memory — CCB is the
primary source, and I'm only prompted for the small set of things CCB
can't tell you (no-shows, off-book serves, anomalies).
