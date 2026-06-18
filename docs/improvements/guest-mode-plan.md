# Guest Mode Plan

The current guest mode is frontend-only. It lets you explore the UI without login and does not persist messages or call OpenRouter.

## Option 1: Keep Frontend-Only Guest Mode

Best while building UI quickly. No backend changes, no database pollution, no model cost.

## Option 2: Anonymous Backend Sessions

Add an `anonymous_sessions` table and let guests create temporary conversations. This allows persistence for a browser session and real model calls with rate limits.

Suggested fields:

- `id`: UUID primary key.
- `session_token_hash`: anonymous browser token hash.
- `expires_at`: cleanup deadline.
- `created_at`.

## Option 3: Demo User Account

Create one seeded demo account with limited model access. This is easy but can mix data between users unless every visitor gets isolated demo data.

## Recommendation

Use frontend-only guest mode during early development. Add anonymous backend sessions only when you want real model testing without forcing signup.
