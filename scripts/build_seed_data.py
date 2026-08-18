#!/usr/bin/env python3
"""Build data/seed-data.json from a manual CCB Involvement>Serving pull.

This encodes the most recent pull (Claude driving Mark's signed-in Chrome
through each person's CCB profile, per the "Data source & refresh model"
section of ironwood-dashboard-spec.md). Re-run whenever a fresh pull is
done -- update PEOPLE and PULL_DATE below and re-run this script.

CCB's own Active/Inactive field is not used -- per Mark, it's never kept up
to date (people get removed from the group instead of marked inactive), so
our own status is computed purely from serving gaps.

data/corrections.json supports two entry types per person, both matched by
(date, position, shift): "addedServedDates" backfills a serve CCB missed;
"removedServedDates" cancels a no-show -- CCB records a signup as served
even when the person didn't actually show up.
"""
import json
from datetime import date, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = REPO_ROOT / "data" / "seed-data.json"
CORRECTIONS_PATH = REPO_ROOT / "data" / "corrections.json"
PULL_DATE = date(2026, 8, 18)

# Each servedDates entry: (sunday_date, position, shift)
# position: "Parking Lot" | "Campus Greeter" | "Campus Lead"
# alsoServes: role -> most recent date seen (only 2026 activity counts as current)
PEOPLE = [
    {
        "id": "66170", "name": "Jamie Weems", "joined": "2026-03-15",
        "served": [
            ("2026-03-29", "Campus Greeter", "2"), ("2026-04-26", "Parking Lot", "2"),
            ("2026-05-24", "Parking Lot", "2"), ("2026-05-31", "Campus Greeter", "1"),
            ("2026-06-07", "Parking Lot", "2"), ("2026-06-14", "Parking Lot", "2"),
            ("2026-07-26", "Parking Lot", "2"), ("2026-08-02", "Parking Lot", "2"),
            ("2026-08-09", "Parking Lot", "2"),
        ],
        "alsoServes": {},
    },
    {
        "id": "68247", "name": "Tony Blake", "joined": "2026-03-13",
        "served": [
            ("2026-03-22", "Parking Lot", "3"), ("2026-03-29", "Parking Lot", "3"),
            ("2026-04-05", "Parking Lot", "Easter"), ("2026-04-19", "Parking Lot", "2"),
            ("2026-05-03", "Parking Lot", "3"), ("2026-06-07", "Parking Lot", "3"),
            ("2026-08-09", "Parking Lot", "2"),
        ],
        "alsoServes": {"Communion Reset": "2026-08-02", "BUILD Leadership": "2026-04-23"},
    },
    {
        "id": "55675", "name": "Rob Brokaw", "joined": "2026-03-16",
        "served": [
            ("2026-03-22", "Parking Lot", "3"), ("2026-03-29", "Parking Lot", "3"),
            ("2026-04-26", "Parking Lot", "3"),
        ],
        "alsoServes": {},
    },
    {
        "id": "49969", "name": "Dennis Eaves", "joined": "2026-03-13",
        "served": [
            ("2026-03-22", "Parking Lot", "3"), ("2026-03-29", "Parking Lot", "2"),
            ("2026-03-29", "Parking Lot", "3"), ("2026-04-12", "Parking Lot", "3"),
            ("2026-04-19", "Parking Lot", "3"), ("2026-04-26", "Parking Lot", "3"),
        ],
        "alsoServes": {},
    },
    {
        "id": "66033", "name": "Keanu Fabiana", "joined": "2026-03-26",
        "served": [("2026-04-05", "Parking Lot", "Easter")],
        "alsoServes": {},
    },
    {
        "id": "61348", "name": "Bob Flecken", "joined": "2026-03-15",
        "served": [
            ("2026-03-22", "Parking Lot", "2"), ("2026-04-05", "Parking Lot", "Easter"),
            ("2026-04-19", "Parking Lot", "2"), ("2026-05-17", "Parking Lot", "2"),
        ],
        "alsoServes": {},
    },
    {
        "id": "65297", "name": "Andy Frutchey Jr", "joined": "2026-04-07",
        "served": [
            ("2026-04-05", "Parking Lot", "Easter"), ("2026-05-17", "Parking Lot", "2"),
        ],
        "alsoServes": {},
    },
    {
        "id": "25360", "name": "Brad Hall", "joined": "2026-03-15",
        "served": [
            ("2026-04-05", "Parking Lot", "Easter"), ("2026-05-10", "Parking Lot", "2"),
            ("2026-06-28", "Campus Greeter", "1"), ("2026-07-05", "Campus Greeter", "1"),
        ],
        "alsoServes": {},
    },
    {
        "id": "62366", "name": "Kevin Harding", "joined": "2026-03-15",
        "served": [
            ("2026-03-22", "Parking Lot", "2"), ("2026-04-05", "Parking Lot", "Easter"),
        ],
        "alsoServes": {"Communion Prep": "2025-11-22"},  # stale -- 2025 only, excluded as current
    },
    {
        "id": "68857", "name": "Jeff Hove", "joined": "2026-03-15",
        "served": [
            ("2026-03-22", "Parking Lot", "3"), ("2026-03-29", "Parking Lot", "2"),
            ("2026-04-05", "Parking Lot", "Easter"), ("2026-04-19", "Parking Lot", "2"),
            ("2026-04-26", "Parking Lot", "2"), ("2026-05-03", "Parking Lot", "2"),
            ("2026-05-17", "Parking Lot", "2"), ("2026-05-24", "Parking Lot", "2"),
            ("2026-06-07", "Parking Lot", "2"), ("2026-06-14", "Parking Lot", "2"),
            ("2026-06-28", "Parking Lot", "2"), ("2026-07-05", "Parking Lot", "2"),
            ("2026-07-19", "Parking Lot", "2"), ("2026-07-26", "Parking Lot", "2"),
            ("2026-08-02", "Parking Lot", "2"), ("2026-08-09", "Parking Lot", "2"),
        ],
        "alsoServes": {"Communion Prep": "2026-06-27"},
    },
    {
        "id": "68858", "name": "Wendi Hove", "joined": "2026-03-15",
        "served": [
            ("2026-03-22", "Campus Greeter", "3"), ("2026-03-29", "Campus Greeter", "2"),
            ("2026-04-05", "Campus Greeter", "Easter"), ("2026-04-19", "Parking Lot", "2"),
            ("2026-04-26", "Parking Lot", "2"), ("2026-05-03", "Parking Lot", "2"),
            ("2026-05-17", "Parking Lot", "2"), ("2026-05-24", "Parking Lot", "2"),
            ("2026-06-07", "Parking Lot", "2"), ("2026-06-14", "Parking Lot", "2"),
            ("2026-06-28", "Parking Lot", "2"), ("2026-07-05", "Parking Lot", "2"),
            ("2026-07-19", "Parking Lot", "2"), ("2026-07-26", "Parking Lot", "2"),
            ("2026-08-02", "Parking Lot", "2"), ("2026-08-09", "Parking Lot", "2"),
        ],
        "alsoServes": {"Communion Prep": "2026-06-27"},
    },
    {
        "id": "2159", "name": "Jonathan Indie", "joined": "2026-03-02",
        "served": [
            ("2026-03-22", "Parking Lot", "2"), ("2026-03-29", "Parking Lot", "3"),
            ("2026-04-05", "Parking Lot", "Easter"), ("2026-04-12", "Parking Lot", "2"),
            ("2026-04-12", "Parking Lot", "3"), ("2026-04-19", "Parking Lot", "3"),
            ("2026-04-26", "Parking Lot", "2"), ("2026-05-03", "Parking Lot", "2"),
            ("2026-05-10", "Parking Lot", "2"), ("2026-05-17", "Parking Lot", "2"),
            ("2026-05-24", "Parking Lot", "2"), ("2026-05-31", "Parking Lot", "2"),
            ("2026-06-07", "Parking Lot", "2"), ("2026-06-14", "Parking Lot", "2"),
            ("2026-06-28", "Parking Lot", "2"), ("2026-07-05", "Parking Lot", "2"),
            ("2026-07-12", "Parking Lot", "2"), ("2026-08-02", "Parking Lot", "2"),
        ],
        "alsoServes": {},
    },
    {
        "id": "69327", "name": "Ian Jeffer", "joined": "2026-03-15",
        "served": [("2026-04-05", "Parking Lot", "Easter")],
        "alsoServes": {},
    },
    {
        "id": "53054", "name": "Jacob Jurgens", "joined": "2026-03-13",
        "served": [
            ("2026-03-22", "Parking Lot", "2"), ("2026-03-22", "Parking Lot", "3"),
            ("2026-03-29", "Parking Lot", "3"), ("2026-04-05", "Parking Lot", "Easter"),
            ("2026-04-19", "Parking Lot", "2"), ("2026-04-19", "Parking Lot", "3"),
            ("2026-05-24", "Parking Lot", "2"), ("2026-05-24", "Parking Lot", "3"),
            ("2026-06-07", "Parking Lot", "3"), ("2026-06-14", "Parking Lot", "2"),
            ("2026-06-14", "Parking Lot", "3"), ("2026-06-28", "Parking Lot", "2"),
            ("2026-06-28", "Parking Lot", "3"), ("2026-07-05", "Parking Lot", "2"),
            ("2026-07-05", "Parking Lot", "3"),
        ],
        "alsoServes": {},
    },
    {
        "id": "57018", "name": "Scott Marsh", "joined": "2026-03-15",
        "served": [
            ("2026-04-12", "Campus Lead", "2"), ("2026-04-26", "Campus Lead", "2"),
            ("2026-05-03", "Campus Lead", "2"), ("2026-05-10", "Campus Lead", "2"),
            ("2026-05-17", "Campus Lead", "2"), ("2026-05-24", "Campus Lead", "2"),
            ("2026-05-31", "Campus Lead", "2"), ("2026-06-07", "Campus Greeter", "2"),
            ("2026-06-21", "Campus Lead", "2"), ("2026-06-28", "Campus Lead", "2"),
            ("2026-07-05", "Campus Lead", "2"), ("2026-07-12", "Campus Lead", "2"),
            ("2026-07-19", "Campus Lead", "2"), ("2026-07-26", "Campus Lead", "2"),
            ("2026-08-02", "Campus Lead", "2"), ("2026-08-09", "Campus Lead", "2"),
        ],
        "alsoServes": {},
        "note": "Now titled Campus Lead in CCB (Shift 2) -- promoted from Parking Lot leadership.",
    },
    {
        "id": "65705", "name": "Dan Montanye", "joined": "2026-04-07",
        "served": [
            ("2026-04-05", "Parking Lot", "Easter"), ("2026-08-09", "Parking Lot", "2"),
        ],
        "alsoServes": {},
    },
    {
        "id": "68149", "name": "Sean Moser", "joined": "2026-03-15",
        "served": [
            ("2026-04-05", "Parking Lot", "Easter"), ("2026-04-12", "Parking Lot", "2"),
            ("2026-04-19", "Parking Lot", "2"),
        ],
        "alsoServes": {},
    },
    {
        "id": "67928", "name": "Justus Norgord", "joined": "2026-03-15",
        "served": [
            ("2026-03-29", "Parking Lot", "2"), ("2026-04-12", "Parking Lot", "2"),
            ("2026-04-12", "Campus Greeter", "1"), ("2026-05-24", "Parking Lot", "2"),
            ("2026-05-24", "Campus Greeter", "1"),
        ],
        "alsoServes": {"Campus Greeter": "2026-05-24"},
    },
    {
        "id": "67191", "name": "Daniel Stewart", "joined": "2026-03-15",
        "served": [
            ("2026-03-22", "Parking Lot", "2"), ("2026-04-26", "Campus Greeter", "1"),
        ],
        "alsoServes": {"Communion Reset": "2026-08-09"},
    },
    {
        "id": "36422", "name": "Ben Storrie", "joined": "2026-03-11",
        "served": [
            ("2026-03-29", "Parking Lot", "2"), ("2026-04-12", "Parking Lot", "3"),
            ("2026-04-19", "Parking Lot", "3"), ("2026-04-26", "Parking Lot", "3"),
            ("2026-05-10", "Parking Lot", "3"), ("2026-06-07", "Parking Lot", "3"),
            ("2026-06-21", "Parking Lot", "3"), ("2026-06-28", "Parking Lot", "3"),
            ("2026-07-12", "Parking Lot", "3"), ("2026-07-19", "Parking Lot", "3"),
            ("2026-08-02", "Parking Lot", "3"), ("2026-08-09", "Parking Lot", "3"),
        ],
        "alsoServes": {"Communion Prep": "2025-11-22"},  # stale -- excluded as current
    },
    {
        "id": "70139", "name": "Brandon Orellana", "joined": "2026-07-26",
        "served": [],
        "alsoServes": {},
    },
]


def infer_rotation(served_dates):
    if len(served_dates) < 3:
        return None
    gaps = [(served_dates[i + 1] - served_dates[i]).days for i in range(len(served_dates) - 1)]
    median_gap = sorted(gaps)[len(gaps) // 2]
    if median_gap <= 8:
        return "Weekly"
    if median_gap <= 16:
        return "Bi-Weekly"
    return "Seasonal"


def current_streak_weeks(served_dates, as_of):
    """Consecutive weeks with a serve, walking backward from the most recent Sunday <= as_of."""
    if not served_dates:
        return 0
    date_set = set(served_dates)
    # most recent Sunday on/before as_of
    cursor = as_of - timedelta(days=(as_of.weekday() - 6) % 7)
    if cursor not in date_set:
        return 0
    streak = 0
    while cursor in date_set:
        streak += 1
        cursor -= timedelta(days=7)
    return streak


def build_person(p, corrections):
    raw_served = list(p["served"])
    correction_note = ""
    correction = corrections.get(p["id"])
    removed = set()
    if correction:
        for entry in correction.get("addedServedDates", []):
            for shift in entry["shifts"]:
                raw_served.append((entry["date"], entry["position"], shift))
        for entry in correction.get("removedServedDates", []):
            for shift in entry["shifts"]:
                removed.add((entry["date"], entry["position"], shift))
        correction_note = correction["note"]

    # removedServedDates strips no-shows -- CCB records a signup as served even when the
    # person didn't actually show, so this cancels out a matching entry from PEOPLE's raw
    # pull data (or from addedServedDates above) rather than ever adding a negative date.
    raw_served = [(d, pos, shift) for d, pos, shift in raw_served if (d, pos, shift) not in removed]

    served = sorted(
        (date.fromisoformat(d), pos, shift) for d, pos, shift in raw_served if date.fromisoformat(d) <= PULL_DATE
    )
    served_dates_only = sorted({d for d, _, _ in served})

    also_serves = sorted(
        role for role, last_seen in p["alsoServes"].items() if date.fromisoformat(last_seen).year == 2026
    )

    double_dates = sorted(
        {d for d in served_dates_only if len([1 for sd, _, _ in served if sd == d]) >= 2}
    )
    multi_shift_sunday = bool(double_dates)

    last_served = served_dates_only[-1] if served_dates_only else None
    weeks_since = (PULL_DATE - last_served).days // 7 if last_served else None

    if not served:
        # Never served yet == still "New", regardless of how long they've been on the team.
        status = "new"
    elif len(served_dates_only) <= 1:
        status = "served_once"
    elif weeks_since is not None and weeks_since >= 3:
        status = "needs_review"
    else:
        status = "active"

    rotation = infer_rotation(served_dates_only)
    streak = current_streak_weeks(served_dates_only, PULL_DATE)
    burnout_threshold = 6 if (multi_shift_sunday or len(also_serves) >= 2) else 12
    burnout_warning = rotation == "Weekly" and status == "active" and streak >= burnout_threshold

    regular_entries = [e for e in served if e[2] != "Easter"]
    anchor = regular_entries[-1] if regular_entries else (served[-1] if served else None)
    current_position, current_shift = (anchor[1], anchor[2]) if anchor else (None, None)

    return {
        "id": p["id"],
        "name": p["name"],
        "joined": p["joined"],
        "position": current_position,
        "shift": current_shift,
        "status": status,
        "lastServed": last_served.isoformat() if last_served else None,
        "servedCount": len(served_dates_only),
        "rotation": rotation,
        "multiShiftSunday": multi_shift_sunday,
        "alsoServes": also_serves,
        "burnoutWarning": burnout_warning,
        "burnoutStreakWeeks": streak if burnout_warning else None,
        "servedDates": [d.isoformat() for d in served_dates_only],
        "doubleShiftDates": [d.isoformat() for d in double_dates],
        "note": correction_note or p.get("note", ""),
    }


def main():
    corrections = json.loads(CORRECTIONS_PATH.read_text()) if CORRECTIONS_PATH.exists() else {}
    people = [build_person(p, corrections) for p in PEOPLE]
    people.sort(key=lambda p: p["name"])
    output = {
        "generatedAt": PULL_DATE.isoformat(),
        "source": "CCB Involvement > Serving, per-person pull via Claude in Chrome",
        "people": people,
    }
    OUTPUT_PATH.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(people)} people to {OUTPUT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
