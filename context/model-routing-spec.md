# Clawmic Model Routing Specification v2

This document defines how Clawmic selects models across two dimensions:
**Planning** (thinking, clarifying, specifying) and **Execution** (writing code).

---

## Core Principle

Clawmic operates in two modes with separate model hierarchies:

1. **Planning Mode** — Strategic thinking, Q&A, spec writing
2. **Execution Mode** — Actual code implementation

The right model depends on BOTH the mode AND the task complexity.

---

## 1) Planning Tiers

Used for: Chat, Q&A, clarification, spec writing, architecture review.

| Tier | Role | Primary Model | Fallback | When |
|------|------|---------------|----------|------|
| **P-A** | Daily Chat | Gemini Flash | OpenAI mini | Smalltalk, quick questions, simple Q&A |
| **P-B** | Strategic | Claude Sonnet | OpenAI standard | Q&A sessions, spec writing, planning |
| **P-C** | Masterbrain | Claude Opus | Sonnet + think:high | Architecture decisions, critical reviews |

### P-A: Daily Chat (80% of planning usage)
- Short answers, clarifications
- No complex reasoning needed
- Cost-optimized

### P-B: Strategic (18% of planning usage)
- Structured Q&A to clarify requirements
- Writing implementation specifications
- Planning multi-step work
- Analyzing existing code

### P-C: Masterbrain (2% of planning usage)
- Architecture decisions with long-term impact
- Critical review before major implementations
- When Sonnet is uncertain or stuck
- **Requires:** User says `REVIEW` or explicit high-risk detection

---

## 2) Execution Tiers

Used for: Writing actual code after planning is complete.

| Tier | Role | Primary Model | When |
|------|------|---------------|------|
| **E-S** | Major Implementation | Claude Opus (strongest) | New features, redesigns, greenfield |
| **E-A** | Major Iteration | Claude Opus (strong) | Extending existing systems |
| **E-B** | Complex Task | OpenAI strong | Difficult bugs, refactoring, complex logic |
| **E-C** | Standard Task | OpenAI standard/cheap | Small fixes, styling, simple changes |

### E-S: Major Implementation
**Criteria (any of these):**
- New feature built from scratch
- Complete redesign/rewrite of component
- Multi-file implementation with many dependencies
- Greenfield or near-greenfield work
- "Design from one mold" / cohesive system design

**Prerequisites:**
- Q&A phase MUST be completed
- Spec MUST be written and approved
- All assets and dependencies MUST be ready

**Cost warning:** Always shown before execution

### E-A: Major Iteration
**Criteria (any of these):**
- Extending existing functionality significantly
- Integrating new section/module into existing system
- Refactoring with architectural changes
- Adding major feature to existing codebase

**Prerequisites:**
- Existing code understood
- Impact on existing system analyzed

**Cost warning:** Always shown before execution

### E-B: Complex Task
**Criteria (any of these):**
- Complex bug with unclear root cause
- Performance optimization requiring deep analysis
- Difficult logic implementation
- Writing tests for complex components
- Refactoring without architecture change

**Prerequisites:**
- Problem clearly defined
- Acceptance criteria clear

**Cost warning:** None (OpenAI, moderate cost)

### E-C: Standard Task
**Criteria (any of these):**
- Small bug fixes
- Styling/CSS changes
- Text/content updates
- Simple component modifications
- Copy-paste with minor adjustments

**Prerequisites:**
- Clear description is sufficient

**Cost warning:** None (cheap)

---

## 3) Workflow: Planning to Execution

```
USER REQUEST
     ↓
┌─────────────────────────────────────────┐
│  PHASE 1: RECOGNITION (P-A)             │
│  Clawmic identifies: Is this code work? │
│  → Yes: Start implementation workflow   │
│  → No: Standard response                │
└─────────────────────────────────────────┘
     ↓
┌─────────────────────────────────────────┐
│  PHASE 2: Q&A (P-B)                     │
│  Systematic clarification               │
│  Covers: scope, context, edge cases,    │
│          constraints, testing, rollback │
│  → User says: SPEC                      │
└─────────────────────────────────────────┘
     ↓
┌─────────────────────────────────────────┐
│  PHASE 3: SPEC WRITING (P-B)            │
│  Write perfect implementation spec      │
│  → Optional: User says REVIEW → P-C     │
└─────────────────────────────────────────┘
     ↓
┌─────────────────────────────────────────┐
│  PHASE 4: EXECUTION PROPOSAL            │
│  Clawmic analyzes task size and proposes│
│  appropriate execution tier:            │
│                                         │
│  "Based on this spec (new feature,      │
│   multi-file, greenfield), I recommend  │
│   E-S (Opus). Cost estimate: ~$X.       │
│   Confirm with BUILD S, or choose       │
│   BUILD A/B/C for different tier."      │
└─────────────────────────────────────────┘
     ↓
┌─────────────────────────────────────────┐
│  PHASE 5: EXECUTION (E-S/A/B/C)         │
│  Code is written with selected model    │
│  Follow spec exactly                    │
└─────────────────────────────────────────┘
     ↓
┌─────────────────────────────────────────┐
│  PHASE 6: VERIFICATION (P-A or P-B)     │
│  Review result, provide feedback        │
│  → Done or iterate                      │
└─────────────────────────────────────────┘
```

---

## 4) User Commands

| Command | Effect |
|---------|--------|
| `SPEC` | Q&A complete → proceed to spec writing |
| `REVIEW` | Request Masterbrain (Opus) to review spec |
| `BUILD S` | Execute with Opus (Major Implementation) |
| `BUILD A` | Execute with Opus (Major Iteration) |
| `BUILD B` | Execute with OpenAI strong (Complex Task) |
| `BUILD C` | Execute with OpenAI cheap (Standard Task) |
| `BUILD` | Clawmic chooses tier based on spec (with confirmation) |

---

## 5) Automatic Tier Selection

When user says just `BUILD` (without tier), Clawmic analyzes the spec:

**Select E-S if:**
- Spec mentions "new feature", "from scratch", "redesign"
- Multiple new files to create
- No existing code to extend

**Select E-A if:**
- Spec mentions "extend", "integrate", "add to existing"
- Modifying existing architecture
- New module in existing system

**Select E-B if:**
- Spec mentions "fix", "optimize", "refactor"
- Complex logic but contained scope
- Debugging or performance work

**Select E-C if:**
- Spec mentions "small change", "update", "tweak"
- Single file, simple modification
- Styling or content changes

**Always confirm selection with user before executing.**

---

## 6) Cost Protection

### Warnings

| Tier | Before Execution |
|------|------------------|
| E-S | "⚠️ Using Opus for major implementation. This is your most expensive tier. Proceed with BUILD S?" |
| E-A | "⚠️ Using Opus for iteration. Estimated cost for this task: ~$X. Proceed with BUILD A?" |
| E-B | No warning |
| E-C | No warning |

### Budget Tracking

- Track daily/weekly Opus usage
- If approaching limits, suggest downgrade: "Consider BUILD B (OpenAI) to save budget"
- Never refuse, only warn and suggest

---

## 7) Failover Strategy

### Planning Failover

| If unavailable | Try next |
|----------------|----------|
| Gemini Flash | OpenAI mini |
| Claude Sonnet | OpenAI standard |
| Claude Opus | Sonnet + think:high |

### Execution Failover

| If unavailable | Try next |
|----------------|----------|
| Opus (E-S/E-A) | Sonnet + think:high → OpenAI strong |
| OpenAI strong (E-B) | OpenAI standard |
| OpenAI standard (E-C) | OpenAI mini |

**Critical rule:** Never silently downgrade E-S/E-A to OpenAI. Always inform user.

---

## 8) Provider Roles Summary

| Provider | Primary Role |
|----------|--------------|
| **Gemini** | Daily chat (cheap, fast) |
| **Claude** | Strategic thinking + major execution |
| **OpenAI** | Standard execution + fallback |

---

## 9) Examples

| User Request | Planning Tier | Execution Tier |
|--------------|---------------|----------------|
| "What time is it in Zürich?" | P-A | None |
| "Let's plan the new auth system" | P-B | None (planning only) |
| "BUILD the auth system we just planned" | — | E-S (new feature) |
| "Add a blog section to the website" | P-B → | E-A (iteration) |
| "Fix the login bug" | P-B → | E-B (complex task) |
| "Change the button color to blue" | P-A → | E-C (standard) |

---

## 10) Acceptance Criteria

| Scenario | Expected |
|----------|----------|
| Trivial question | P-A, no spec, no build |
| New feature request | P-B Q&A → P-B Spec → E-S |
| Extend existing feature | P-B Q&A → P-B Spec → E-A |
| Complex bug | P-B analysis → E-B |
| Simple fix | P-A → E-C |
| User says BUILD without tier | Clawmic proposes tier, waits for confirmation |
| E-S/E-A selected | Cost warning shown |
| Opus unavailable for E-S | Warn user, suggest Sonnet+thinking or wait |

---

*This specification ensures optimal model selection for both cost efficiency and output quality.*

—Clawmic
