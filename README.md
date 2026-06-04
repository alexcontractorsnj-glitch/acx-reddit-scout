# ACX Build — Reddit Scout

A **read-only** research tool for ACX Build LLC, a licensed home remodeling
company in New Jersey. It monitors public posts in home-improvement and
NJ-local subreddits to surface the questions homeowners commonly ask, so our
team can publish accurate, helpful content.

## What it does
- Authenticates as a registered **read-only** Data API client (application-only OAuth).
- Reads recent public posts from a fixed list of subreddits.
- Flags posts matching a keyword list (remodel costs, permits, contractors, NJ counties).
- Saves matches to a local CSV for the team to review.

## What it does NOT do
This tool is strictly read-only. It never:
- posts, comments, or replies
- votes or saves
- sends messages or DMs
- modifies anything on Reddit

It explicitly refuses to run if the Reddit session is not in read-only mode.

## Data handling
- Stores only public metadata: title, body, score, comment count, timestamp, permalink.
- Retains data only as long as needed for content planning.
- Never sells, licenses, shares, or uses the data to train ML/AI models.
- Never profiles or attempts to identify individual users.

## Setup
1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and add your app credentials, or export them
   as environment variables:
   ```
   export REDDIT_CLIENT_ID="your_client_id"
   export REDDIT_CLIENT_SECRET="your_client_secret"
   ```
3. Run:
   ```
   python reddit_scout.py
   ```

## Configuration
Edit `SUBREDDITS` and `KEYWORDS` at the top of `reddit_scout.py` to match the
subreddits and topics you want to monitor.

---
Operated by ACX Build LLC · Reddit account: u/Far_Ad_9968 · App: ACX_BUILD_AI369
