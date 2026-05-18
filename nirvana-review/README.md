# Nirvana GTD Review

Downloads your NirvanaHQ tasks as Markdown for morning or weekly review in Claude.

## Setup

```
pip install requests
python nirvana_review.py
```

First run: prompts for email + password, caches the authtoken in `~/.nirvana_review`.

If programmatic login fails → grab token from browser:
1. Log in at https://app.nirvanahq.com
2. DevTools → Network → any request to `api.nirvanahq.com`
3. Copy the `authtoken` query param value when prompted

## Usage

```
# Daily review (default) — skips Someday/Maybe + Later
python nirvana_review.py

# Weekly review — includes Someday/Maybe + Later for Get Creative phase
python nirvana_review.py --mode weekly

# Custom output path
python nirvana_review.py --output C:\Reviews\today.md

# Debug: also dump raw API JSON to latest-raw.json
python nirvana_review.py --debug

# Reset cached token (if expired)
python nirvana_review.py --reset-token
```

Output saved to: `~/nirvana-review/YYYY-MM-DD-daily.md` (or `-weekly.md`)
Stable pointer `~/nirvana-review/latest.md` is always updated.

## In Claude

Open Claude Code and run:
```
/review-nirvana
```
Or drag the output `.md` file into a Claude chat and say "Let's do my morning review."
