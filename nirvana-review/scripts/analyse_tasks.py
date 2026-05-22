#!/usr/bin/env python3
"""Output all GTD review data in one pass for Claude to read."""

import json
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

BASE = Path.home() / "nirvana-review"
TODAY = datetime.now().strftime("%Y%m%d")
TODAY_DISPLAY = datetime.now().strftime("%Y-%m-%d")

STATE_LABELS = {
    "0": "Inbox", "1": "Next", "2": "Waiting", "3": "Scheduled",
    "4": "Someday", "5": "Later", "9": "Recurring", "11": "Project",
}
ENERGY = {"": "?", "0": "?", "1": "low", "2": "med", "3": "high"}


def fetch_fresh(mode="daily"):
    """Run nirvana_review.py to pull latest data from the API."""
    import subprocess
    fetcher = Path(__file__).parent / "nirvana_review.py"
    print(f"No data for today — fetching from NirvanaHQ...", flush=True)
    result = subprocess.run(
        [sys.executable, str(fetcher), "--mode", mode],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print("ERROR: fetch failed.")
        print(result.stdout)
        print(result.stderr)
        sys.exit(1)
    print(result.stdout.strip())


def find_json(mode="daily"):
    today_file = BASE / f"{TODAY_DISPLAY}-{mode}.json"
    if today_file.exists():
        return today_file
    fetch_fresh(mode)
    if today_file.exists():
        return today_file
    # fall back to latest if fetch somehow wrote elsewhere
    latest = BASE / "latest.json"
    if latest.exists():
        return latest
    return None


def load(path):
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    if "results" in d and "tasks" not in d:
        print("ERROR: This file is a raw API dump, not processed output.")
        print(f"  Run: python nirvana_review.py  (or --mode weekly)")
        sys.exit(1)
    return d


def fmt_time(etime):
    try:
        m = int(etime)
    except (TypeError, ValueError):
        return "?"
    if m <= 0:
        return "?"
    return f"{m // 60}h{m % 60:02d}m" if m >= 60 else f"{m}m"


def project_label(t, pmap):
    pid = t.get("parentid") or ""
    return pmap.get(pid, "standalone")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "daily"
    path = find_json(mode)
    if path is None:
        print(f"ERROR: No JSON found in {BASE}. Run nirvana_review.py first.")
        sys.exit(1)

    d = load(path)
    tasks = d["tasks"]
    fetched = d.get("fetched", "?")
    data_mode = d.get("mode", mode)

    pmap = {t["id"]: t["name"] for t in tasks if t.get("type") == "1"}
    next_parents = {t.get("parentid") for t in tasks if t.get("state") == "1"}
    active_projects = [t for t in tasks if t.get("type") == "1" and t.get("state") == "11"]
    projects_no_next = [p for p in active_projects if p["id"] not in next_parents]

    inbox = [t for t in tasks if t.get("state") == "0"]
    overdue_act = sorted(
        [t for t in tasks if t.get("state") == "1" and t.get("duedate") and t["duedate"] < TODAY],
        key=lambda x: x["duedate"],
    )
    overdue_wait = sorted(
        [t for t in tasks if t.get("state") == "2" and t.get("duedate") and t["duedate"] < TODAY],
        key=lambda x: x["duedate"],
    )
    due_today = [t for t in tasks if t.get("duedate") == TODAY and t.get("state") in ("1", "2")]
    next_actions = [t for t in tasks if t.get("state") == "1"]
    standalone = [t for t in next_actions if not pmap.get(t.get("parentid", ""))]

    # --- SNAPSHOT ---
    print("=== SNAPSHOT ===")
    print(f"date: {TODAY_DISPLAY}  fetched: {fetched}  mode: {data_mode}")
    print(
        f"inbox: {len(inbox)}  "
        f"overdue: {len(overdue_act) + len(overdue_wait)} ({len(overdue_act)} actionable, {len(overdue_wait)} waiting)  "
        f"due_today: {len(due_today)}"
    )
    print(
        f"projects: {len(active_projects)} active  {len(projects_no_next)} without next action  "
        f"next_actions: {len(next_actions)}"
    )

    # --- INBOX ---
    print(f"\n=== INBOX ({len(inbox)}) ===")
    for t in inbox:
        note = (t.get("note") or "").replace("\n", " ")[:100]
        print(f"  {t['name']}")
        if note:
            print(f"    note: {note}")

    # --- OVERDUE ACTIONABLE ---
    print(f"\n=== OVERDUE — ACTIONABLE ({len(overdue_act)}) ===")
    for t in overdue_act:
        due = t["duedate"][:4] + "-" + t["duedate"][4:6] + "-" + t["duedate"][6:]
        print(f"  [{due}] {t['name']} | {project_label(t, pmap)} | {fmt_time(t.get('etime'))} | {ENERGY.get(t.get('energy',''), '?')}")

    # --- OVERDUE WAITING ---
    print(f"\n=== OVERDUE — WAITING ({len(overdue_wait)}) ===")
    for t in overdue_wait:
        due = t["duedate"][:4] + "-" + t["duedate"][4:6] + "-" + t["duedate"][6:]
        print(f"  [{due}] {t['name']} | {project_label(t, pmap)} | waiting: {t.get('waitingfor', '?')}")

    # --- DUE TODAY ---
    print(f"\n=== DUE TODAY ({len(due_today)}) ===")
    for t in due_today:
        state = STATE_LABELS.get(t.get("state", ""), "?")
        print(f"  {t['name']} | {project_label(t, pmap)} | {fmt_time(t.get('etime'))} | {ENERGY.get(t.get('energy',''), '?')} | {state}")

    # --- PROJECT NEXT ACTIONS ---
    by_proj = defaultdict(list)
    for t in next_actions:
        pid = t.get("parentid", "")
        if pid in pmap:
            by_proj[pid].append(t)

    print(f"\n=== PROJECT NEXT ACTIONS ===")
    for pid, name in sorted(pmap.items(), key=lambda x: x[1]):
        if pid not in {p["id"] for p in active_projects}:
            continue
        if pid in by_proj:
            t = by_proj[pid][0]
            due = ""
            if t.get("duedate"):
                dd = t["duedate"]
                due = f" | due:{dd[:4]}-{dd[4:6]}-{dd[6:]}"
            print(f"  [{name}] {t['name']} | {fmt_time(t.get('etime'))} | {ENERGY.get(t.get('energy',''), '?')}{due}")
        else:
            print(f"  [{name}] *** NO NEXT ACTION ***")

    # --- STANDALONE ---
    print(f"\n=== STANDALONE NEXT ACTIONS ({len(standalone)}) ===")
    for t in sorted(standalone, key=lambda x: (x.get("duedate") or "z", x.get("name", ""))):
        due = ""
        if t.get("duedate"):
            dd = t["duedate"]
            due = f" | due:{dd[:4]}-{dd[4:6]}-{dd[6:]}"
        print(f"  {t['name']} | {fmt_time(t.get('etime'))} | {ENERGY.get(t.get('energy',''), '?')}{due}")


if __name__ == "__main__":
    main()
