# Email Integration Plan

This plan covers future email reading and sending tools while keeping Phase 1 unchanged.

## Recommended Scope

Start with Gmail because it has strong OAuth support and clear APIs. Add generic SMTP only for sending simple outbound email later.

## Future Backend Modules

```text
backend/app/integrations/email/
├── oauth_service.py
├── gmail_client.py
├── email_reader.py
├── email_sender.py
└── schemas.py
```

## Suggested Tables

### integration_accounts

- `id`: UUID primary key.
- `user_id`: owner.
- `provider`: `gmail`, `outlook`, etc.
- `email`: connected account address.
- `access_token_encrypted`: encrypted OAuth access token.
- `refresh_token_encrypted`: encrypted OAuth refresh token.
- `scopes_json`: granted scopes.
- `created_at` and `updated_at`.

### email_drafts

- `id`: UUID primary key.
- `user_id`: owner.
- `to_json`, `cc_json`, `bcc_json`: recipients.
- `subject`: draft subject.
- `body`: draft body.
- `status`: `draft`, `needs_confirmation`, `sent`, `failed`.
- `created_at` and `updated_at`.

## Safe Sending Flow

1. User asks PAIOS to write or send an email.
2. Tool mode calls `email_draft_create`, not direct send.
3. UI displays draft and asks for confirmation.
4. User confirms.
5. Backend sends email through Gmail API.
6. Store status and provider message ID.

## Tools To Add Later

- `gmail_search`: searches messages.
- `gmail_read_thread`: reads a thread by ID.
- `email_draft_create`: creates a draft for confirmation.
- `email_send_confirmed`: sends only a previously confirmed draft.

## Security Notes

- Encrypt OAuth tokens at rest.
- Keep email sending behind explicit confirmation.
- Log tool calls but avoid logging full email bodies in application logs.
- Use least-privilege OAuth scopes.
