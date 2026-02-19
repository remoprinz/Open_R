# SECURITY.md — Secrets & API Key Policy

This document defines how Clawmic handles secrets, API keys, tokens, and
other sensitive credentials. It is binding and non-negotiable.

---

## Core Principle: Zero-Knowledge in Transit

Secrets must never appear in any communication channel. Not in chat, not in
logs, not in transcripts, not in files that could be shared or committed.

The only place secrets exist is in **environment variables** on the host
where Clawmic runs. Clawmic reads from there. He never sees, stores, or
transmits the actual values.

---

## What Clawmic Must Never Do

1. **Never ask for secrets in chat.** Not API keys, not passwords, not
   tokens, not OAuth credentials. If a key is needed, Clawmic says:
   "I need access to [service]. Please set the environment variable
   [VAR_NAME] on the host."

2. **Never display secrets.** Not fully, not partially, not masked with
   asterisks. If Clawmic needs to confirm a key exists, he checks the
   environment variable and reports only: "✓ [VAR_NAME] is set" or
   "✗ [VAR_NAME] is not set."

3. **Never write secrets to files.** Not to config files, not to logs, not
   to memory files, not to any persistent storage. The only exception:
   if Remo explicitly instructs Clawmic to write a secret to a specific
   secure location (e.g., `~/.openclaw/openclaw.json`), and only after
   confirming that location is in `.gitignore` and not synced anywhere.

4. **Never include secrets in commits.** Before any git operation, Clawmic
   checks that no secrets are staged. If detected, abort and warn.

5. **Never reference secrets in memory/logs.** Session transcripts, memory
   files, daily logs — none of these may contain actual secret values.

---

## Standard Environment Variables

Clawmic expects these environment variables on his host:

| Variable | Service | Description |
|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | Claude | Primary LLM |
| `OPENAI_API_KEY` | OpenAI | Secondary LLM |
| `GEMINI_API_KEY` | Google Gemini | Tertiary LLM |
| `GITHUB_TOKEN` | GitHub | Repo access (read-only preferred) |
| `GOOGLE_CLIENT_ID` | Google OAuth | For Drive/Gmail access |
| `GOOGLE_CLIENT_SECRET` | Google OAuth | For Drive/Gmail access |

Additional variables are added as needed. Clawmic documents new requirements
in this file via PR.

---

## Workflow: Adding a New Secret

### Remo's Steps (one-time, per secret)

1. **Generate the key** at the service provider (Google, OpenAI, etc.)
2. **SSH into Clawmic's host** (or use secure remote access)
3. **Add to environment:**
   ```bash
   # In ~/.bashrc, ~/.zshrc, or /etc/environment
   export NEW_SERVICE_KEY="the-actual-key"
   ```
4. **Reload:** `source ~/.bashrc` or restart the OpenClaw gateway
5. **Tell Clawmic (in chat):** "NEW_SERVICE_KEY is set. You can use [service] now."

### Clawmic's Steps

1. **Verify:** Check that the variable exists (without reading its value)
2. **Confirm:** "✓ NEW_SERVICE_KEY is set. [Service] access confirmed."
3. **Document:** Add the variable to the table above via PR to Open_R

---

## Workflow: Rotating a Compromised Secret

If a secret may have been exposed (appeared in chat, logs, or any
non-secure location):

### Immediate Actions

1. **Remo revokes the old key** at the service provider
2. **Remo generates a new key**
3. **Remo updates the environment variable** on Clawmic's host
4. **Remo tells Clawmic:** "[VAR_NAME] has been rotated."
5. **Clawmic verifies** the new key works

### Clawmic's Responsibilities

- If Clawmic **suspects** a secret was exposed (e.g., it appeared in a
  transcript, a skill logged it, etc.), he immediately warns Remo:
  "⚠️ Potential secret exposure: [description]. Recommend rotating [VAR_NAME]."
- Clawmic does **not** wait to be asked. Proactive warning is mandatory.

---

## Secure Locations on Clawmic's Host

These paths may contain secrets and must never be committed or synced:

- `~/.openclaw/openclaw.json` — OpenClaw config (may contain API keys)
- `~/.openclaw/credentials/` — OAuth tokens
- `~/.config/gog/` — Google OAuth credentials
- `~/.*rc` files — May contain exported env vars

Clawmic ensures these are in `.gitignore` if any git repo is initialized
in the home directory.

---

## OAuth Credentials (Google, etc.)

For OAuth-based services (Drive, Gmail, etc.):

1. **Client credentials** (`client_secret.json`) are created by Remo in
   Google Cloud Console
2. Remo places the file in a secure location on Clawmic's host
3. Clawmic runs the OAuth flow (`gog auth` etc.)
4. **User tokens** are stored locally on Clawmic's host, never transmitted
5. Clawmic never displays or logs OAuth tokens

---

## GitHub Access

GitHub access uses a **fine-grained personal access token** with:

- **Read-only** permissions for repository contents
- **No write** permissions unless explicitly needed for a specific task
- Scoped to **specific repositories**, not all repos

Token is set as `GITHUB_TOKEN` environment variable.

---

## What Happens If Clawmic Violates This Policy

If Clawmic accidentally displays, logs, or transmits a secret:

1. Clawmic immediately warns: "⚠️ Secret exposure in [location]. Rotate now."
2. Remo rotates the affected secret
3. The incident is logged in CHANGELOG.md (without the secret value)
4. Policy is reviewed and tightened if needed

---

## Summary for Clawmic

```
NEVER ask for secrets in chat
NEVER display secrets, not even partially
NEVER write secrets to files (unless explicitly instructed + verified safe)
NEVER commit secrets
ALWAYS read secrets from environment variables
ALWAYS warn immediately if exposure suspected
ALWAYS confirm key availability with "✓ VAR is set" (not the value)
```

---

## Summary for Remo

```
Secrets are set ONCE per service, via SSH or direct host access
After setting: tell Clawmic "VAR_NAME is set" — nothing more
On suspected exposure: revoke, regenerate, update env var, tell Clawmic "rotated"
Never send actual keys via chat, email, or any message
```

---

*Security is a process, not a state. This document evolves as we learn.*

—Clawmic & Remo
