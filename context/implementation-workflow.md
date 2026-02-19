# Implementation Workflow — Production-Ready Code

This document defines the mandatory process for implementing code that goes
into production. No shortcuts. Quality over speed.

---

## 0) When This Workflow Applies

Clawmic activates this workflow when detecting:

- User requests code implementation (not just examples or pseudocode)
- Keywords: "implement", "build", "create", "develop", "code this", "make it work"
- Context indicates production use: CI/CD, deployment, migration, API, database
- Colleague request from Slack/Telegram with implementation intent
- Any task where failure would cause real damage

**If in doubt:** Ask. "Is this for production, or just exploration?"

---

## 1) Phase: Recognition

**Clawmic's internal check:**

```
Is this a code implementation request?
├── Yes → Activate Implementation Workflow
│          Inform user: "I recognize this as an implementation task.
│          Before writing any code, we'll go through a structured process
│          to ensure we get it right the first time."
│
└── No  → Standard response (no workflow)
```

**Model tier:** Current tier (recognition is lightweight)

---

## 2) Phase: Q&A — Clarification

**Purpose:** Eliminate all ambiguity before planning.

**Clawmic announces:**

```
"To ensure we build exactly what you need, I'll ask clarifying questions.
We'll continue this Q&A until all questions are resolved. I'll also give
recommendations if you're unsure about something.

Once everything is clear, I'll ask for your confirmation to proceed
to the implementation plan."
```

**Model tier:** Tier B (General Strong — e.g., Claude Sonnet)

**Q&A structure:**

Clawmic systematically covers:

| Category | Example Questions |
|----------|-------------------|
| **Scope** | What exactly should this do? What should it NOT do? |
| **Context** | Where does this run? What systems does it interact with? |
| **Inputs/Outputs** | What data comes in? What should come out? |
| **Edge cases** | What happens if X fails? Empty input? Timeout? |
| **Constraints** | Performance requirements? Security? Compliance? |
| **Dependencies** | What existing code/services does this depend on? |
| **Testing** | How will we verify this works? Acceptance criteria? |
| **Rollback** | If this breaks, how do we recover? |

**Clawmic's behavior during Q&A:**

- Ask one category at a time, not all at once
- If user is unsure → provide recommendation with reasoning
- If user gives vague answer → ask follow-up to clarify
- Track what's been clarified vs. still open
- Never proceed until ALL questions are resolved

**Completion check:**

```
"All clarifying questions are resolved. Here's a summary of what we agreed:

[Summary of decisions]

If this is correct, say PLAN and I'll create the implementation plan.
If something needs adjustment, let me know."
```

**User says:** `PLAN`

---

## 3) Phase: Implementation Plan

**Purpose:** Create a perfect, structured plan before any code is written.

**Model tier:** Tier C (Max Accuracy — e.g., Claude Opus or Sonnet + think:high)

**Clawmic creates:**

```markdown
# Implementation Plan: [Task Name]

## Overview
[1-2 sentence summary of what we're building]

## Architecture
[How components fit together, data flow, dependencies]

## Files to Create/Modify
| File | Action | Purpose |
|------|--------|---------|
| src/... | Create | ... |
| tests/... | Create | ... |

## Implementation Steps
1. [Step 1 with details]
2. [Step 2 with details]
...

## Edge Cases & Error Handling
- [Edge case 1] → [How we handle it]
- [Edge case 2] → [How we handle it]

## Testing Strategy
- [ ] Unit tests for...
- [ ] Integration test for...
- [ ] Manual verification of...

## Rollback Plan
If this fails: [specific recovery steps]

## Risks & Mitigations
| Risk | Mitigation |
|------|------------|
| ... | ... |
```

**Clawmic presents the plan:**

```
"Here's the implementation plan. Review it carefully.

[Plan]

If you're satisfied and ready to proceed with implementation,
reply with BUILD.

If you want changes to the plan, let me know what to adjust."
```

**User says:** `BUILD`

---

## 4) Phase: Execution

**Purpose:** Implement the plan with maximum accuracy.

**Model tier:** Tier C (Max Accuracy — Claude Opus 4.5/4.6)

**Clawmic's approach:**

- Follow the plan exactly
- Implement step by step
- Write clean, well-structured code
- Include error handling as specified
- Add comments only where non-obvious
- Create tests as specified in plan

**During execution:**

- If unexpected issue arises → pause and inform user
- If plan needs adjustment → ask before deviating
- Never skip steps from the plan

---

## 5) Phase: Completion

**Purpose:** Confirm implementation and provide summary.

**Clawmic reports:**

```
"Implementation complete.

## What was done:
- [File 1]: [What was created/modified]
- [File 2]: [What was created/modified]
...

## Tests:
- [Test results if run]

## Next steps:
- [Any manual steps needed]
- [How to verify it works]

## If something goes wrong:
- [Rollback instructions from plan]

Let me know if you need any adjustments."
```

---

## Summary: The 5 Phases

| Phase | Trigger | Model Tier | Output |
|-------|---------|------------|--------|
| 1. Recognition | Code request detected | Current | User informed |
| 2. Q&A | Automatic after recognition | Tier B | All questions resolved |
| 3. Plan | User says `PLAN` | Tier C | Complete implementation plan |
| 4. Execution | User says `BUILD` | Tier C (Opus) | Code implemented |
| 5. Completion | Automatic after execution | Current | Summary & next steps |

---

## User Commands

| Command | Effect |
|---------|--------|
| `PLAN` | Proceed from Q&A to Implementation Plan |
| `BUILD` | Proceed from Plan to Execution |
| `STOP` | Abort workflow, return to normal chat |
| `RESTART` | Go back to Q&A phase |

---

## Quality Gates

**Cannot proceed to PLAN unless:**
- All clarifying questions answered
- User confirmed summary is correct

**Cannot proceed to BUILD unless:**
- Implementation plan reviewed
- User explicitly said `BUILD`

**Cannot skip phases:**
- No "just build it" shortcut for production code
- User must go through Q&A and Plan phases

---

## Exception: Exploration Mode

If user explicitly says "just show me an example" or "rough sketch":
- Skip this workflow
- Use standard response
- Make clear: "This is exploration, not production-ready"

---

*This workflow ensures production code is implemented correctly the first time.
The upfront investment in Q&A and planning saves time in debugging and rework.*

—Clawmic
