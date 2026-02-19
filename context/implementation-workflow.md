# Implementation Workflow v2

This document defines the mandatory process for implementing code.
It integrates with the Model Routing Specification (see `model-routing-spec.md`).

---

## Overview

Every code implementation follows this flow:

```
RECOGNITION → Q&A → SPEC → [REVIEW] → BUILD → VERIFICATION
```

Each phase has a specific purpose, model tier, and exit criteria.

---

## Phase 1: Recognition

**Purpose:** Identify that this is a code implementation request.

**Model:** P-A (current tier)

**Clawmic detects:**
- Keywords: "implement", "build", "create", "develop", "code this"
- Context: CI/CD, deployment, API, database, migration
- Intent: User wants working code, not just explanation

**Output:**
```
"This is an implementation request. Before writing any code, 
we'll go through a structured process:

1. Q&A to clarify all requirements
2. Specification to document exactly what we'll build
3. Your approval before execution

Let's start. [First clarifying question]"
```

---

## Phase 2: Q&A Clarification

**Purpose:** Eliminate all ambiguity before planning.

**Model:** P-B (Claude Sonnet)

**Systematic coverage:**

| Category | Questions |
|----------|-----------|
| **Scope** | What exactly should this do? What should it NOT do? |
| **Context** | Where does this run? What systems does it interact with? |
| **Inputs/Outputs** | What data comes in? What should come out? |
| **Edge Cases** | What if X fails? Empty input? Timeout? |
| **Constraints** | Performance? Security? Compliance? Budget? |
| **Dependencies** | What existing code/services does this depend on? |
| **Testing** | How do we verify it works? Acceptance criteria? |
| **Rollback** | If this breaks, how do we recover? |

**Behavior:**
- Ask one category at a time
- If user is unsure → provide recommendation with reasoning
- If user gives vague answer → ask follow-up
- Track what's clarified vs. still open
- Never proceed until ALL essential questions resolved

**Exit trigger:** User says `SPEC`

**Output:**
```
"All clarifying questions resolved. Summary:

[Bullet list of decisions made]

Say SPEC to proceed to specification writing."
```

---

## Phase 3: Specification Writing

**Purpose:** Create a perfect, unambiguous implementation spec.

**Model:** P-B (Claude Sonnet)

**Spec format:**

```markdown
# Implementation Spec: [Feature Name]

## Overview
[1-2 sentence summary]

## Context
- Codebase: [path]
- Related files: [list]
- Tech stack: [list]
- Patterns to follow: [existing patterns]

## Requirements
1. [Requirement 1 — testable]
2. [Requirement 2 — testable]
...

## Architecture
[How components fit together, data flow]

## Files to Create/Modify
| File | Action | Purpose |
|------|--------|---------|
| ... | Create/Modify | ... |

## Edge Cases
| Case | Expected Behavior |
|------|-------------------|
| ... | ... |

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
...

## Testing Strategy
- [ ] [Test type and scope]
...

## Rollback Plan
[Specific recovery steps if this fails]

## Do NOT
- [Out of scope items]
- [Common mistakes to avoid]
```

**Output:**
```
"Here's the implementation specification:

[Full spec]

Options:
- Say REVIEW for Masterbrain (Opus) to review this spec
- Say BUILD to proceed to implementation
- Or tell me what to adjust"
```

---

## Phase 4: Review (Optional)

**Purpose:** Masterbrain validates spec for critical implementations.

**Model:** P-C (Claude Opus)

**Triggered by:** User says `REVIEW`

**Or auto-suggested when:**
- High-risk: production, auth, data migration, payment
- Large scope: >5 files, architecture change
- Uncertainty detected in Q&A phase

**Cost warning:**
```
"⚠️ Masterbrain review uses Opus. Proceed with REVIEW?"
```

**Review checks:**
- Spec completeness
- Hidden assumptions
- Edge cases not covered
- Architecture concerns
- Risk assessment

**Output:**
```
"Masterbrain Review Complete:

✅ [What's good]
⚠️ [Concerns/suggestions]
❌ [Issues to fix]

[Recommended changes if any]

Say BUILD when ready, or adjust the spec first."
```

---

## Phase 5: Execution Proposal & BUILD

**Purpose:** Select appropriate execution tier and implement.

**Model:** Depends on tier selected

### 5a: Tier Proposal

Clawmic analyzes the spec and proposes:

```
"Based on this spec:
- [Key characteristic 1]
- [Key characteristic 2]

I recommend: BUILD [S/A/B/C] — [Tier name]

Estimated scope: [X files, Y functions]
[Cost warning if E-S or E-A]

Confirm with BUILD [S/A/B/C], or choose a different tier."
```

### 5b: Execution Tiers

| Command | Tier | Model | When |
|---------|------|-------|------|
| `BUILD S` | Major Implementation | Opus (strongest) | New features, redesigns |
| `BUILD A` | Major Iteration | Opus (strong) | Extending existing systems |
| `BUILD B` | Complex Task | OpenAI strong | Difficult bugs, refactoring |
| `BUILD C` | Standard Task | OpenAI cheap | Small fixes, styling |

### 5c: Execution

Once user confirms:

1. Follow spec exactly
2. Implement step by step
3. Create all specified files
4. Handle all specified edge cases
5. If unexpected issue → pause and inform user
6. If spec adjustment needed → ask before deviating

---

## Phase 6: Verification

**Purpose:** Confirm implementation and provide summary.

**Model:** P-A or P-B (depending on complexity)

**Output:**
```
"Implementation complete.

## Created/Modified:
- [file1]: [what was done]
- [file2]: [what was done]

## Acceptance Criteria:
- [x] [Criterion 1] — verified
- [x] [Criterion 2] — verified

## Next Steps:
- [Manual verification needed]
- [How to test]

## If Issues:
- [Rollback instructions]

Let me know if adjustments needed."
```

---

## Quick Reference: Commands

| Command | Phase | Effect |
|---------|-------|--------|
| `SPEC` | Q&A → Spec | Start specification writing |
| `REVIEW` | Spec → Review | Request Masterbrain review |
| `BUILD` | Spec/Review → Exec | Clawmic proposes tier |
| `BUILD S` | → Execution | Major Implementation (Opus) |
| `BUILD A` | → Execution | Major Iteration (Opus) |
| `BUILD B` | → Execution | Complex Task (OpenAI strong) |
| `BUILD C` | → Execution | Standard Task (OpenAI cheap) |
| `STOP` | Any | Abort workflow |
| `RESTART` | Any | Return to Q&A |

---

## Quality Gates

### Cannot proceed to SPEC unless:
- All essential Q&A questions answered
- User explicitly says `SPEC`

### Cannot proceed to BUILD unless:
- Spec is written and presented
- User explicitly says `BUILD` (with or without tier)

### Cannot skip phases:
- No "just build it" shortcut for non-trivial code
- Exception: E-C tasks (small fixes) can skip to quick spec

---

## Exception: Quick Path for Small Tasks

If Clawmic detects a clearly small task (E-C level):

```
"This looks like a small change. Quick spec:

- Change: [what]
- File: [which]
- Behavior: [expected]

Say BUILD C to proceed, or let me know if this needs more planning."
```

This skips extended Q&A but still requires user confirmation.

---

*This workflow ensures quality through structured clarification while remaining efficient for simple tasks.*

—Clawmic
