"""
ACX Build - Reddit Scout
========================
A READ-ONLY research tool for ACX Build LLC, a licensed home remodeling
company in New Jersey.

Purpose: monitor public posts in home-improvement and NJ-local subreddits to
understand the questions homeowners commonly ask (remodel costs, permits,
contractor selection), so the team can publish accurate, helpful content.

This application is strictly read-only. It NEVER posts, comments, votes,
saves, or sends messages. It only reads public listings via Reddit's Data API,
and it refuses to run if the API session is not in read-only mode.
"""

from __future__ import annotations

import csv
import os
import sys
import datetime as dt

import praw


# --- Configuration ----------------------------------------------------------

SUBREDDITS = [
    "HomeImprovement",
    "Renovations",
    "Construction",
    "DIY",
    "HVAC",
    "Plumbing",
    "newjersey",
]

KEYWORDS = [
    "bathroom remodel",
    "kitchen remodel",
    "home addition",
    "deck",
    "patio",
    "roofing",
    "general contractor",
    "contractor recommendation",
    "remodel cost",
    "permit",
    "morris county",
    "sussex county",
    "passaic county",
    "essex county",
    "warren county",
    "dover nj",
    "rockaway nj",
]

POSTS_PER_SUBREDDIT = 75
OUTPUT_CSV = "scout_findings.csv"

# Reddit's expected User-Agent format: platform:app_id:version (by /u/username)
USER_AGENT = "web:ACX_BUILD_AI369:v1.0 (by /u/Far_Ad_9968)"


# --- Authentication (read-only) ---------------------------------------------

def get_reddit() -> praw.Reddit:
    """Return a READ-ONLY Reddit instance.

    Read-only mode uses only the app's client_id + client_secret
    (application-only OAuth). No user login is used, which keeps this tool
    strictly non-interactive and incapable of taking any action on Reddit.
    """
    try:
        client_id = os.environ["REDDIT_CLIENT_ID"]
        client_secret = os.environ["REDDIT_CLIENT_SECRET"]
    except KeyError as missing:
        sys.exit(f"Missing environment variable: {missing}. See README.md.")

    return praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=USER_AGENT,
    )


# --- Core logic --------------------------------------------------------------

def find_keywords(text: str) -> list[str]:
    """Return the keywords found in the given text (case-insensitive)."""
    lowered = (text or "").lower()
    return [kw for kw in KEYWORDS if kw in lowered]


def scan() -> None:
    reddit = get_reddit()

    print(f"Read-only mode: {reddit.read_only}")  # expected: True
    if not reddit.read_only:
        sys.exit("Refusing to run: this app must operate in read-only mode.")

    findings = []
    for name in SUBREDDITS:
        print(f"Scanning r/{name} ...")
        try:
            for post in reddit.subreddit(name).new(limit=POSTS_PER_SUBREDDIT):
                hits = find_keywords(post.title) + find_keywords(post.selftext)
                if not hits:
                    continue
                findings.append({
                    "subreddit": name,
                    "title": post.title,
                    "matched_keywords": ", ".join(sorted(set(hits))),
                    "score": post.score,
                    "num_comments": post.num_comments,
                    "created_utc": dt.datetime.utcfromtimestamp(
                        post.created_utc).strftime("%Y-%m-%d %H:%M"),
                    "url": f"https://www.reddit.com{post.permalink}",
                })
        except Exception as exc:  # one bad subreddit shouldn't stop the run
            print(f"  ! Skipped r/{name}: {exc}")

    if not findings:
        print("No matching posts found this run. Try widening KEYWORDS.")
        return

    findings.sort(key=lambda f: f["num_comments"], reverse=True)
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(findings[0].keys()))
        writer.writeheader()
        writer.writerows(findings)

    print(f"\nFound {len(findings)} relevant posts. Saved to {OUTPUT_CSV}")


if __name__ == "__main__":
    scan()
