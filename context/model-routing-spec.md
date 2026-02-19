# Clawmic Model Selection & Failover Specification

This document defines how Clawmic intelligently selects models based on task complexity, accuracy requirements, and cost optimization.

---

## 0) Goal

Clawmic operates with intelligent, cost-aware model selection:

- **Default:** fast & cheap (everyday chat, simple tasks)
- **Auto-upgrade:** when complexity, accuracy, or tools require it
- **Auto-downgrade:** when task is trivial
- **Vision-aware:** switch to vision model when images are involved
- **Robust:** handle rate limits, provider outages, key issues gracefully
- **Cost-aware:** warn when high-cost models are used extensively
- **User override:** respect explicit /model commands

---

## 1) Providers

Connected:
- **Anthropic** (Claude)
- **Google** (Gemini)  
- **OpenAI**

Environment variables (per SECURITY.md):
- `ANTHROPIC_API_KEY`
- `GEMINI_API_KEY`
- `OPENAI_API_KEY`

---

## 2) Model Tiers

### Tier A — Fast & Cheap (Default)

**Use cases:**
- Smalltalk, short answers
- Simple Q&A
- Light text editing
- Short translations
- Trivial tasks

**Models:**
- `claude-3-5-haiku-20241022`
- `gemini-2.0-flash`
- `gpt-4o-mini`

**Think setting:** `low`

---

### Tier B — General Strong

**Use cases:**
- Medium complexity, structured emails, product copy
- Moderate planning, medium code tasks
- Summaries with multiple sources
- Tool usage (files, tables, simple workflows)

**Models:**
- `claude-sonnet-4-5-20250514`
- `gemini-2.5-pro`
- `gpt-4o`

**Think setting:** `medium`

---

### Tier C — Max Accuracy / Tool-Heavy

**Use cases:**
- Architecture decisions, deep debugging
- Complex multi-step tasks
- Very long context, many constraints
- High-stakes accuracy (production bugs, data migration)
- Keywords: "perfect", "exact", "no errors", "production-ready"

**Models:**
- `claude-opus-4-6-20250601` (when available)
- `claude-sonnet-4-5-20250514` + `think:high` (fallback)
- `o3` / `gpt-4.5` (when available)
- `gemini-2.5-pro` + extended thinking

**Think setting:** `high`

---

### Vision Tier

**Trigger:** Image in input OR "look at this screenshot/photo"

**Models:**
- `claude-sonnet-4-5-20250514` (vision capable)
- `gpt-4o` (vision capable)
- `gemini-2.5-pro` (vision capable)

**Rule:** If current model lacks vision → switch to vision model.
If image + debugging → Vision + Tier C.

---

## 3) Upgrade Triggers

### A → B (any of these)

- More than 1 clear sub-task ("do A, then B, then C")
- User requests reasoning, comparisons, tradeoffs
- Output must be structured (spec, plan, checklist, API design)
- Context contains ≥2 technical components
- Constraints present (performance, cost, security, UX)
- Tool usage expected (files, tables, external sources)

### B → C (any of these)

- Debugging/refactoring in real codebase
- **Quality keywords + complexity:** "perfect", "exact", "no errors", "production-ready" PLUS at least one of: multi-step tasks, code context, constraints, or high-risk domain
- Long specification, many acceptance criteria
- Tool-heavy planned (multi-step, multi-file, external APIs)
- High risk: data loss, auth/keys, CI/CD, migrations
- User explicitly requests highest quality

**Note:** Quality keywords alone (without complexity signals) do not trigger Tier C upgrade to prevent cost manipulation.

### Downgrade C/B → A (all must apply)

- User asks for "short", "bullet points", "doesn't matter"
- OR chat is clearly trivial (1 sentence, no constraints)
- AND no vision/tools needed
- AND context fits in Tier A window

---

## 4) Extended Thinking Rules

| Tier | Think Setting | When |
|------|---------------|------|
| A | `low` | Default for simple tasks |
| B | `medium` | Default for medium complexity |
| C | `high` | Always for Tier C tasks |
| Any | `high` | User says "think carefully", "reason step by step" |

**Cost warning:** If `think:high` is used >3 times in a session, notify user once:
"Using extended thinking frequently. This increases cost. Continue?"

---

## 5) Context Window Handling

**Reactive approach:** Instead of predicting context limits, handle them as they occur:

1. **Start with selected tier** based on complexity
2. **If provider returns context error** → upgrade to next tier
3. **If all tiers fail with context error** → ask user to reduce context
4. **Never truncate without user consent**

**Context window capacity varies by provider and model version. Reactive handling is more robust than fixed predictions.**

| Model Class | Typical Range |
|-------------|---------------|
| Fast models | 100-200k tokens |
| General models | 200-1M+ tokens |
| Max models | 200k-2M+ tokens |

---

## 6) Cost Awareness

### Approximate cost multipliers (vs Tier A baseline)

| Tier | Cost Factor |
|------|-------------|
| A | 1x |
| B | 5x |
| C | 15-25x |
| think:high | +2-3x |

### Warnings

- If Tier C used >5 times in one session: warn once
- If estimated session cost >$1: warn once
- User can disable warnings: `/cost-warnings off`

---

## 7) Failover Strategy

### Error handling order

1. **Auth rotation** (same provider, same model, different key if available)
2. **Model fallback** (same tier, same provider)
3. **Provider fallback** (same tier, different provider)
4. **Tier fallback** (ONLY for availability tasks, NEVER for accuracy tasks)

### Critical Rule: No Tier Downgrade for Accuracy Tasks

**If task requires Tier C** (keywords: "production-ready", "perfect", "no errors", high-risk):
- **All Tier C models unavailable** → Wait/retry OR inform user
- **Never silent downgrade to Tier B/A** → Quality violation
- **User must approve lower tier** → Explicit consent required

This prevents quality degradation for critical tasks.

### Error classes

| Error | Action |
|-------|--------|
| Rate limit / 429 / timeout | Auth rotation → model fallback → provider fallback |
| Invalid key / billing | Provider disabled temporarily |
| Model not in allowlist | Log as config bug, use fallback |
| Context too long | Upgrade tier or ask user to reduce |
| All Tier C unavailable (accuracy task) | Wait/retry OR user consent for downgrade |
| All Tier C unavailable (general task) | Fallback to Tier B with warning |

### Fallback chains

- **Tier A:** Claude-haiku → Gemini-flash → GPT-4o-mini
- **Tier B:** Claude-sonnet → GPT-4o → Gemini-pro
- **Tier C:** Claude-opus → Claude-sonnet+think:high → GPT-4.5 → Gemini-pro+thinking
- **Vision:** Claude-sonnet → GPT-4o → Gemini-pro

---

## 8) User Override

| Command | Function |
|---------|----------|
| `/model [name]` | Switch to specific model (must be in allowlist) |
| `/model status` | Show current model and tier |
| `/model auto` | Return to automatic selection |
| `/tier [a\|b\|c]` | Force tier for this session |
| `/think [low\|medium\|high]` | Force thinking level |

If requested model not in allowlist → error with list of allowed models.

---

## 9) Transparency

When model changes, log (if `verboseRouting=true`):

```
[routing] Upgrading to Tier B: multiple sub-tasks detected
[routing] Switching to vision model: image in input
[routing] Fallback: claude-sonnet rate limited → gpt-4o
```

**Default:** silent routing. User can enable: `/verbose on`

---

## 10) Acceptance Criteria

| Scenario | Expected Behavior |
|----------|-------------------|
| "What time in Zürich?" | Tier A |
| "Give me exact spec, must be perfect" | Tier C |
| Screenshot analysis | Vision model |
| "Make me an Excel/PDF" | Tier B minimum |
| "Production-ready migration script" | Tier C + think:high |
| Rate limit on primary | Silent fallback, no user action |
| `/model gpt-4o` | Switch if in allowlist |
| `/model random-model` | Error + show allowed models |

---

## 11) Implementation Notes

### Configuration Structure

To implement this specification, the OpenClaw configuration needs:

1. **Model allowlist** — All models that can be used
2. **Tier definitions** — Which models belong to which tier
3. **Default routing** — Starting model and upgrade paths
4. **Fallback chains** — What to try when models fail
5. **Cost tracking** — Session cost estimation and warnings

### Required from Current Setup

For implementation, need to see current `openclaw.json` structure:
```bash
cat ~/.openclaw/openclaw.json | grep -v -E "(key|secret|token)"
```

This shows config without exposing secrets.

### Testing Protocol

1. **Tier selection** — Verify upgrade/downgrade triggers work
2. **Failover robustness** — Test rate limits and provider outages
3. **Cost awareness** — Verify warnings at appropriate thresholds
4. **Vision handling** — Test image inputs route to vision models
5. **User overrides** — Test all `/model` and `/tier` commands

---

*This specification ensures Clawmic operates efficiently across the cost/quality spectrum while maintaining robustness and user control.*

—Clawmic Team