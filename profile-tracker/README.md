# Wortkarte profile tracker

Cloudflare Worker backend that records classroom profile creations.

## Live API

- `POST /profiles` `{ "name": "Alex", "userAgent": "...", "source": "share" }`
- `GET /profiles` list + count

Temporary preview worker (claim to keep permanently):

- API: https://wortkarte-profiles.goofy-drifter.workers.dev
- Claim: https://dash.cloudflare.com/claim-preview?claimToken=U5aVHJGY47Z5O9EONdX4p1ckT64pu9zmb7RcaoLC5C0

Claim within 60 minutes of deploy, or recreate with `npx wrangler deploy --temporary`.
