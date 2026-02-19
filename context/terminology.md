# Terminology & Glossary

Clear definitions to prevent miscommunication between Remo and Clawmic.

---

## Model Tiers

### Planning Tiers (Thinking Mode)

| Term | Meaning | Model |
|------|---------|-------|
| **P-A** | Daily Chat tier | Gemini Flash |
| **P-B** | Strategic tier | Claude Sonnet |
| **P-C** | Masterbrain tier | Claude Opus |

### Execution Tiers (Building Mode)

| Term | Meaning | Model |
|------|---------|-------|
| **E-S** | Major Implementation | Opus (strongest available) |
| **E-A** | Major Iteration | Opus (strong) |
| **E-B** | Complex Task | OpenAI strong (gpt-4o, o3) |
| **E-C** | Standard Task | OpenAI cheap (gpt-4o-mini) |

---

## Providers

| Term | What it is |
|------|------------|
| **Anthropic** | Company behind Claude (Opus, Sonnet, Haiku) |
| **OpenAI** | Company behind GPT models |
| **Gemini** | Google's AI models |

---

## Claude Model Naming

| Name | Meaning |
|------|---------|
| **Opus** | Largest/strongest Claude model |
| **Sonnet** | Medium Claude model (strong, efficient) |
| **Haiku** | Smallest Claude model (fast, cheap) |
| **4.5, 4.6** | Version numbers |

Example: "Claude Opus 4.6" = The Opus model, version 4.6

---

## "Codex"

**Historical:** OpenAI had a product called "Codex" (2021-2022) for coding.

**Today:** When we say "Codex", we mean: **using OpenAI models via API for code execution**.

There is no separate "Codex" product to configure. We just use OpenAI API.

---

## API vs. Subscription

| Term | What it is | How it's billed |
|------|------------|-----------------|
| **ChatGPT Plus/Pro** | Subscription for chat.openai.com | Monthly fee |
| **OpenAI API** | Programmatic access to models | Per token (usage-based) |
| **Claude Pro** | Subscription for claude.ai | Monthly fee |
| **Anthropic API** | Programmatic access to Claude | Per token (usage-based) |

**Important:** Subscriptions (Plus/Pro) do NOT give API access. API requires separate billing setup.

Clawmic uses **API access** (Anthropic, OpenAI, Gemini), not subscriptions.

---

## Workflow Commands

| Command | When to use | What happens |
|---------|-------------|--------------|
| **SPEC** | After Q&A is complete | Clawmic writes specification |
| **REVIEW** | After spec is written | Masterbrain (Opus) reviews |
| **BUILD** | After spec is ready | Clawmic proposes execution tier |
| **BUILD S** | Major implementation | Execute with Opus |
| **BUILD A** | Major iteration | Execute with Opus |
| **BUILD B** | Complex task | Execute with OpenAI strong |
| **BUILD C** | Standard task | Execute with OpenAI cheap |

---

## Cost Terms

| Term | Meaning |
|------|---------|
| **Token** | Unit of text (~4 characters or ~0.75 words) |
| **Input tokens** | What you send to the model |
| **Output tokens** | What the model generates |
| **M tokens** | Million tokens (pricing unit) |
| **Spending limit** | Maximum monthly spend (set in provider dashboard) |

---

## Common Phrases

| Phrase | Meaning |
|--------|---------|
| "Use the strongest model" | E-S tier (Opus) |
| "Cost-optimized" | Use cheaper model (E-C or P-A) |
| "Masterbrain" | Opus in review/architecture mode |
| "Daily driver" | Default cheap model for chat |
| "Strategic" | Sonnet for planning/specs |

---

*Use these terms consistently to avoid miscommunication.*

—Clawmic
