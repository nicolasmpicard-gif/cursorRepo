#!/usr/bin/env python3
"""Export a Playwright storage state after manual LinkedIn login.

Usage:
  pip install '.[browser]'
  playwright install chromium
  python scripts/save_linkedin_session.py --out linkedin_state.json
"""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("linkedin_state.json"),
        help="Where to write the storage state JSON",
    )
    parser.add_argument(
        "--url",
        default="https://www.linkedin.com/login",
        help="Start URL (login page by default)",
    )
    args = parser.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise SystemExit(
            "Install browser extras first: pip install '.[browser]' && playwright install chromium"
        ) from exc

    print("A Chromium window will open. Log into LinkedIn, then return here and press Enter.")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(args.url, wait_until="domcontentloaded")
        input("Press Enter after you are logged in… ")
        context.storage_state(path=str(args.out))
        browser.close()
    print(f"Wrote {args.out}")
    print("Use it with: jd-bot --browser --storage-state", args.out, "<job-url>")


if __name__ == "__main__":
    main()
