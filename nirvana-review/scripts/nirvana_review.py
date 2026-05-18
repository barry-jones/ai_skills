#!/usr/bin/env python3
"""Download NirvanaHQ tasks and save raw JSON for GTD review in Claude."""

import argparse
import hashlib
import json
import uuid
import time
from datetime import datetime
from pathlib import Path

import requests

API_BASE = "https://api.nirvanahq.com/"
APP_ID = "nirvana_review"
APP_VERSION = "1.0"
CONFIG_FILE = Path.home() / ".nirvana_review"
JSON_OUT = Path.home() / "nirvana-review" / "latest.json"

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


def _common_params(authtoken):
    return {
        "requestid": str(uuid.uuid4()),
        "clienttime": int(time.time()),
        "authtoken": authtoken,
        "appid": APP_ID,
        "appversion": APP_VERSION,
    }


def login(email, password):
    """Authenticate with email + password and return authtoken."""
    md5_pass = hashlib.md5(password.encode("utf-8")).hexdigest()
    params = {
        "api": "rest",
        "method": "auth.new",
        **_common_params(""),
    }
    resp = requests.post(API_BASE, params=params, data={"u": email, "p": md5_pass}, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    try:
        return data["results"][0]["auth"]["token"]
    except (KeyError, IndexError, TypeError):
        raise RuntimeError(f"Unexpected auth response:\n{json.dumps(data, indent=2)}")


def fetch_everything(authtoken):
    """Fetch all tasks from NirvanaHQ and return raw JSON."""
    params = {
        "api": "rest",
        "method": "everything",
        **_common_params(authtoken),
    }
    resp = requests.get(API_BASE, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def load_config():
    """Load config from ~/.nirvana_review.

    Handles two formats:
    - Legacy: raw token on single line (no '=')
    - Current: KEY=VALUE lines
    """
    config = {}
    if not CONFIG_FILE.exists():
        return config
    content = CONFIG_FILE.read_text(encoding="utf-8").strip()
    lines = content.splitlines()
    has_equals = any("=" in line for line in lines if line and not line.startswith("#"))
    if not has_equals and content:
        # Legacy format — entire file is a raw token
        config["AUTHTOKEN"] = content
        # Migrate to proper format immediately
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
        pass  # Windows may not support chmod


def get_authtoken(config, args):
    """Return authtoken, prompting/logging in if needed."""
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


def summarise(data):
    """Print a quick count summary to stdout."""
    tasks = [r["task"] for r in data.get("results", []) if "task" in r]
    active = [t for t in tasks if t.get("completed", "0") == "0" and t.get("deleted", "0") == "0"]
    projects = [t for t in active if t.get("type", "0") == "1"]
    solo = [t for t in active if t.get("type", "0") != "1"]

    from collections import Counter
    state_counts = Counter(t.get("state", "?") for t in solo)
    proj_counts  = Counter(t.get("state", "?") for t in projects)

    print(f"\nActive: {len(active)} total ({len(projects)} projects, {len(solo)} tasks)")
    for state, label in STATE_LABELS.items():
        tc = state_counts.get(state, 0)
        pc = proj_counts.get(state, 0)
        if tc or pc:
            parts = []
            if tc: parts.append(f"{tc} tasks")
            if pc: parts.append(f"{pc} projects")
            print(f"  {label}: {', '.join(parts)}")


def main():
    parser = argparse.ArgumentParser(description="Fetch NirvanaHQ tasks for GTD review in Claude")
    parser.add_argument("--token", help="Override authtoken")
    parser.add_argument("--reset-token", action="store_true", help="Clear cached authtoken")
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

    JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"Saved: {JSON_OUT}")

    summarise(data)


if __name__ == "__main__":
    main()
