#!/usr/bin/env python3
"""Download NirvanaHQ tasks and save filtered JSON for GTD review in Claude."""

import argparse
import hashlib
import json
import uuid
import time
from collections import Counter
from datetime import datetime
from pathlib import Path

import requests

API_BASE = "https://api.nirvanahq.com/"
APP_ID = "nirvana_review"
APP_VERSION = "1.0"
CONFIG_FILE = Path.home() / ".nirvana_review"
OUTPUT_DIR = Path.home() / "nirvana-review"

STATE_LABELS = {
    "0":  "Inbox",
    "1":  "Next Actions",
    "2":  "Waiting",
    "3":  "Scheduled",
    "4":  "Someday / Maybe",
    "5":  "Later",
    "9":  "Recurring",
    "11": "Active Projects",
}

# Excluded from daily output to cut token load
DAILY_SKIP_STATES = {"4", "5"}

# Fields useful for GTD review — everything else dropped
KEEP_FIELDS = {
    "id", "type", "state", "parentid",
    "name", "tags", "etime", "energy",
    "waitingfor", "startdate", "duedate", "recurring", "note",
}


def _common_params(authtoken):
    return {
        "requestid": str(uuid.uuid4()),
        "clienttime": int(time.time()),
        "authtoken": authtoken,
        "appid": APP_ID,
        "appversion": APP_VERSION,
    }


def login(email, password):
    md5_pass = hashlib.md5(password.encode("utf-8")).hexdigest()
    params = {"api": "rest", "method": "auth.new", **_common_params("")}
    resp = requests.post(API_BASE, params=params, data={"u": email, "p": md5_pass}, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    try:
        return data["results"][0]["auth"]["token"]
    except (KeyError, IndexError, TypeError):
        raise RuntimeError(f"Unexpected auth response:\n{json.dumps(data, indent=2)}")


def fetch_everything(authtoken):
    params = {"api": "rest", "method": "everything", **_common_params(authtoken)}
    resp = requests.get(API_BASE, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def load_config():
    config = {}
    if not CONFIG_FILE.exists():
        return config
    content = CONFIG_FILE.read_text(encoding="utf-8").strip()
    lines = content.splitlines()
    has_equals = any("=" in line for line in lines if line and not line.startswith("#"))
    if not has_equals and content:
        config["AUTHTOKEN"] = content
        save_config(config)
    else:
        for line in lines:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                config[k.strip()] = v.strip()
    return config


def save_config(config):
    lines = ["# NirvanaHQ review config", ""]
    for k, v in config.items():
        lines.append(f"{k}={v}")
    CONFIG_FILE.write_text("\n".join(lines), encoding="utf-8")
    try:
        CONFIG_FILE.chmod(0o600)
    except Exception:
        pass


def get_authtoken(config, args):
    if getattr(args, "token", None):
        return args.token
    if "AUTHTOKEN" in config:
        return config["AUTHTOKEN"]

    email = config.get("EMAIL") or input("NirvanaHQ email: ").strip()
    password = input("NirvanaHQ password: ").strip()

    print("Authenticating...", end=" ", flush=True)
    try:
        token = login(email, password)
        print("OK")
        config["EMAIL"] = email
        config["AUTHTOKEN"] = token
        save_config(config)
        print(f"Token cached in {CONFIG_FILE}")
        return token
    except Exception as e:
        print(f"FAILED: {e}")
        print()
        print("Fallback: grab token from browser.")
        print("  1. Log in at https://app.nirvanahq.com")
        print("  2. Open DevTools > Network > any request to api.nirvanahq.com")
        print("  3. Copy the 'authtoken' query parameter value")
        token = input("Paste authtoken here: ").strip()
        config["AUTHTOKEN"] = token
        save_config(config)
        return token


def filter_tasks(data, skip_states=None):
    """Return active tasks with only review-relevant fields."""
    tasks = []
    for r in data.get("results", []):
        if "task" not in r:
            continue
        t = r["task"]
        if t.get("completed", "0") != "0" or t.get("deleted", "0") != "0":
            continue
        if skip_states and t.get("state", "0") in skip_states:
            continue
        tasks.append({k: v for k, v in t.items() if k in KEEP_FIELDS})
    return tasks


def summarise(tasks, mode):
    projects = [t for t in tasks if t.get("type", "0") == "1"]
    solo = [t for t in tasks if t.get("type", "0") != "1"]
    state_counts = Counter(t.get("state", "?") for t in solo)

    print(f"\n{mode.capitalize()} mode — {len(tasks)} active items ({len(projects)} projects, {len(solo)} tasks)")
    for state, label in STATE_LABELS.items():
        c = state_counts.get(state, 0)
        if c:
            print(f"  {label}: {c}")


def main():
    parser = argparse.ArgumentParser(description="Fetch NirvanaHQ tasks for GTD review in Claude")
    parser.add_argument("--mode", choices=["daily", "weekly"], default="daily",
                        help="daily (default): skips Someday/Maybe + Later. weekly: includes all.")
    parser.add_argument("--token", help="Override authtoken")
    parser.add_argument("--reset-token", action="store_true", help="Clear cached authtoken")
    parser.add_argument("--output", help="Override output file path")
    parser.add_argument("--debug", action="store_true", help="Also save raw API JSON to latest-raw.json")
    args = parser.parse_args()

    config = load_config()

    if args.reset_token:
        config.pop("AUTHTOKEN", None)
        save_config(config)
        print("Token cleared.")
        return

    authtoken = get_authtoken(config, args)

    print("Fetching tasks...", end=" ", flush=True)
    data = fetch_everything(authtoken)
    print("OK")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if args.debug:
        raw_path = OUTPUT_DIR / "latest-raw.json"
        raw_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        print(f"Raw JSON: {raw_path}")

    skip_states = DAILY_SKIP_STATES if args.mode == "daily" else set()
    tasks = filter_tasks(data, skip_states=skip_states)

    out_data = {
        "fetched": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "mode": args.mode,
        "tasks": tasks,
    }
    payload = json.dumps(out_data, separators=(",", ":"), ensure_ascii=False)

    if args.output:
        out_path = Path(args.output)
    else:
        stamp = datetime.now().strftime("%Y-%m-%d")
        out_path = OUTPUT_DIR / f"{stamp}-{args.mode}.json"

    out_path.write_text(payload, encoding="utf-8")
    (OUTPUT_DIR / "latest.json").write_text(payload, encoding="utf-8")
    print(f"Saved: {out_path}  ({len(payload):,} chars)")

    summarise(tasks, args.mode)


if __name__ == "__main__":
    main()
