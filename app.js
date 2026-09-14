// Ironwood Parking Team Dashboard
// Read-only. All data comes from data/seed-data.json, built by
// scripts/build_seed_data.py from a CCB Involvement > Serving pull.
// No in-browser editing -- corrections happen by telling Claude, which
// regenerates and commits the data. See ironwood-dashboard-spec.md.

const SHIFT_TABS = ["Shift 1", "Shift 2", "Shift 3", "Irregular", "New"];

const STATUS_META = {
  active: { label: "Active", cls: "active" },
  needs_review: { label: "Drop Off Warning", cls: "review" },
  served_once: { label: "Served Once", cls: "inactive" },
  new: { label: "New", cls: "new" },
  irregular: { label: "Irregular", cls: "inactive" },
};

// Click a tile to filter the roster to it; click the same one again to clear it.
const STAT_FILTERS = [
  { id: "active", label: "Active", cls: "good", predicate: (p) => p.status === "active" },
  { id: "irregular", label: "Irregular", cls: "", predicate: (p) => p.status === "irregular" },
  { id: "burnout", label: "Burnout Warning", cls: "warn", predicate: (p) => p.burnoutWarning },
  { id: "needs_review", label: "Drop Off Warning", cls: "warn", predicate: (p) => p.status === "needs_review" },
];

let seed = null;
let activeShift = "all";
let activeStatFilter = "all";
let sortMode = "name";

function parseISO(s) {
  const [y, m, d] = s.split("-").map(Number);
  return new Date(y, m - 1, d);
}

function formatShort(iso) {
  if (!iso) return "—";
  return parseISO(iso).toLocaleDateString("en-US", { month: "short", day: "numeric" });
}

function shiftGroupFor(person) {
  if (person.status === "new") return "New";
  if (["1", "2", "3"].includes(person.dedicatedShift)) return "Shift " + person.dedicatedShift;
  return "Irregular";
}

function frequencyLabel(person) {
  if (person.status === "new") return "No history yet";
  if (person.status === "served_once") return "Served once";
  if (person.rotation === "Weekly") return "Weekly";
  if (person.rotation === "Bi-Weekly") return "Bi-Weekly";
  if (person.rotation === "Seasonal") return "Seasonal / Occasional";
  return "Irregular";
}

function freqRank(person) {
  const order = { Weekly: 4, "Bi-Weekly": 3, "Seasonal / Occasional": 2, Irregular: 1, "Served once": 0, "Never served": 0, "No history yet": -1 };
  return order[frequencyLabel(person)] ?? 0;
}

// Last WEEKS_SHOWN Sundays (~6 months) on/before the data's generatedAt date.
const WEEKS_SHOWN = 26;
function recentSundays(generatedAt) {
  const asOf = parseISO(generatedAt);
  const dow = asOf.getDay(); // 0 = Sunday
  const mostRecentSunday = new Date(asOf);
  mostRecentSunday.setDate(asOf.getDate() - dow);
  const out = [];
  for (let i = WEEKS_SHOWN - 1; i >= 0; i--) {
    const d = new Date(mostRecentSunday);
    d.setDate(mostRecentSunday.getDate() - i * 7);
    out.push(d);
  }
  return out;
}

function toISO(d) {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}

function nameSort(a, b) { return a.name.localeCompare(b.name); }
function freqSort(a, b) { return freqRank(b) - freqRank(a); }
function lastServedSort(a, b) {
  if (!a.lastServed) return 1;
  if (!b.lastServed) return -1;
  return b.lastServed.localeCompare(a.lastServed);
}

function renderTabs() {
  const el = document.getElementById("shiftPills");
  el.innerHTML = "";
  ["all", ...SHIFT_TABS].forEach((t) => {
    const btn = document.createElement("button");
    btn.className = "pill-btn" + (t === activeShift ? " active" : "");
    btn.textContent = t === "all" ? "All" : t;
    btn.addEventListener("click", () => {
      activeShift = t;
      render();
    });
    el.appendChild(btn);
  });
}

function renderStats(people) {
  const el = document.getElementById("stats");
  el.innerHTML = "";
  STAT_FILTERS.forEach((f) => {
    const count = people.filter(f.predicate).length;
    const div = document.createElement("div");
    div.className = `stat ${f.cls}${f.id === activeStatFilter ? " selected" : ""}`;
    div.innerHTML = `<div class="n">${count}</div><div class="l">${f.label}</div>`;
    div.addEventListener("click", () => {
      activeStatFilter = activeStatFilter === f.id ? "all" : f.id;
      render();
    });
    el.appendChild(div);
  });
}

function renderTable(people) {
  const roster = document.getElementById("roster");
  roster.innerHTML = "";

  if (people.length === 0) {
    roster.innerHTML = `<div class="person"><div class="row" style="grid-template-columns:1fr"><div>No one matches this view.</div></div></div>`;
    return;
  }

  const weeks = recentSundays(seed.generatedAt);

  people.forEach((p) => {
    const meta = STATUS_META[p.status];
    const el = document.createElement("div");
    el.className = "person";

    const flagChips = [];
    if (p.position === "Campus Lead") flagChips.push(`<span class="flag-chip lead">Shift Lead</span>`);
    if (p.multiShiftSunday) flagChips.push(`<span class="flag-chip multi">Multi-Shift Sunday</span>`);
    if (p.burnoutWarning) flagChips.push(`<span class="flag-chip burnout">Burnout Warning</span>`);
    if (p.alsoServes.length) flagChips.push(`<span class="flag-chip also">Also Serves (${p.alsoServes.length})</span>`);

    const shiftTag = p.position
      ? `${p.position}${["1", "2", "3"].includes(p.shift) ? " · Shift " + p.shift : ""}`
      : "—";

    const weeksHtml = weeks.map((wd, wi) => {
      const iso = toISO(wd);
      const isMonthStart = wi === 0 || wd.getMonth() !== weeks[wi - 1].getMonth();
      const isLast = wi === weeks.length - 1;
      const label = isMonthStart
        ? wd.toLocaleDateString("en-US", { month: "short" })
        : isLast
          ? wd.toLocaleDateString("en-US", { month: "short", day: "numeric" })
          : "";
      let cls = "blank";
      if (p.joined && iso >= p.joined) {
        cls = "off";
        if (p.doubleShiftDates.includes(iso)) cls = "double";
        else if (p.servedDates.includes(iso)) cls = "served";
      }
      return `<div class="week"><div class="dot ${cls}" title="${iso}"></div><div class="wl">${label}</div></div>`;
    }).join("");

    const burnoutNote = p.burnoutWarning
      ? `<div class="detail-block"><div class="k">Burnout Warning</div><div class="v">No break in ${p.burnoutStreakWeeks} consecutive weeks${p.multiShiftSunday ? " — double-shift, so the 6-week threshold applies" : ""}.</div></div>`
      : "";

    const noteBlock = p.note
      ? `<div class="detail-block"><div class="k">Note</div><div class="v">${p.note}</div></div>`
      : "";

    el.innerHTML = `
      <div class="row">
        <div class="name">${p.name}</div>
        <div class="status-pill ${meta.cls}">${meta.label}</div>
        <div class="shift-tag">${shiftTag}</div>
        <div class="freq">${frequencyLabel(p)}</div>
        <div class="last-served">Last: ${formatShort(p.lastServed)}</div>
        <div class="flags">${flagChips.join("")}</div>
        <div class="chev">&#8250;</div>
      </div>
      <div class="detail">
        <div class="weeks-scroll"><div class="weeks">${weeksHtml}</div></div>
        <div class="legend">
          <span><span class="dot served"></span> served</span>
          <span><span class="dot double"></span> double shift</span>
          <span><span class="dot off"></span> not scheduled</span>
          <span><span class="dot blank"></span> before joining</span>
        </div>
        <div class="detail-grid">
          <div class="detail-block"><div class="k">Dedicated Team</div><div class="v">${p.dedicatedShift ? "Shift " + p.dedicatedShift : "Irregular"}</div></div>
          <div class="detail-block"><div class="k">Joined Team</div><div class="v">${formatShort(p.joined)}</div></div>
          <div class="detail-block"><div class="k">Also Serves</div><div class="v">${p.alsoServes.length ? p.alsoServes.join(", ") : "—"}</div></div>
          ${burnoutNote}
          ${noteBlock}
        </div>
      </div>
    `;

    el.querySelector(".row").addEventListener("click", () => el.classList.toggle("open"));
    roster.appendChild(el);
  });
}

function applyFilter(people) {
  const statFilter = STAT_FILTERS.find((f) => f.id === activeStatFilter);
  return people
    .filter((p) => activeShift === "all" || shiftGroupFor(p) === activeShift)
    .filter((p) => !statFilter || statFilter.predicate(p));
}

function applySort(people) {
  const sorter = sortMode === "frequency" ? freqSort : sortMode === "lastServed" ? lastServedSort : nameSort;
  return [...people].sort(sorter);
}

function render() {
  renderTabs();
  renderStats(seed.people);
  renderTable(applySort(applyFilter(seed.people)));
}

function setupControls() {
  document.getElementById("sortSelect").addEventListener("change", (e) => {
    sortMode = e.target.value;
    render();
  });
}

async function init() {
  const res = await fetch("data/seed-data.json", { cache: "no-store" });
  seed = await res.json();
  document.getElementById("sync-meta").innerHTML =
    `DATA AS OF ${seed.generatedAt}<br>${seed.people.length} on team`;
  setupControls();
  render();
}

init();
