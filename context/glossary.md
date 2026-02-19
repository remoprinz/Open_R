# Glossary — Trigger Keywords & Scope Definitions

This document clarifies ambiguous terms and provides decision criteria for tier selection.

---

## Execution Tier Triggers

### E-S: Major Implementation

**Clear triggers (any applies):**
- "new feature", "from scratch", "build new"
- "redesign", "rewrite", "greenfield"
- "create system", "design from one mold"
- Multiple new files to create (3+)
- No existing code to extend
- Clean-slate architecture

**Examples:**
- ✓ "Build a new authentication system"
- ✓ "Create a blog from scratch"
- ✓ "Redesign the entire dashboard"
- ✗ "Add login to existing auth" → E-A

**Cost:** Highest (Opus). Always requires Q&A + Spec + approval.

---

### E-A: Major Iteration

**Clear triggers (any applies):**
- "extend existing", "add to", "integrate into"
- "new section/module in existing system"
- "refactor architecture" (changes structure)
- Modifying 2+ interconnected files significantly
- Impact on existing system design

**Examples:**
- ✓ "Add a blog section to the website"
- ✓ "Integrate payment into checkout"
- ✓ "Refactor API layer to use middleware"
- ✗ "Fix checkout bug" → E-B
- ✗ "Add one field to form" → E-C

**Cost:** High (Opus). Requires Q&A + Spec + approval.

---

### E-B: Complex Task

**Clear triggers (any applies):**
- "fix [complex bug]" with unclear root cause
- "optimize performance" requiring analysis
- "refactor" without architecture change
- Difficult logic implementation
- Writing tests for complex components
- Debugging production issues

**Ambiguous cases:**
- "fix bug" → depends on complexity
  - **E-B if:** Root cause unclear, multi-file, race condition, edge case
  - **E-C if:** Bug is obvious, single-line fix, typo, simple logic error

**Examples:**
- ✓ "Fix the memory leak in the data pipeline"
- ✓ "Optimize the slow search query"
- ✓ "Refactor this 500-line function"
- ✗ "Fix typo in button label" → E-C

**Cost:** Moderate (OpenAI strong). Brief spec recommended, not mandatory.

---

### E-C: Standard Task

**Clear triggers (any applies):**
- "small fix", "quick change", "simple update"
- "styling", "CSS", "design tweak"
- "text/content update", "copy change"
- "add simple field", "update constant"
- Single-file, obvious change
- Copy-paste with minor adjustments

**Examples:**
- ✓ "Change button color to blue"
- ✓ "Fix typo in error message"
- ✓ "Add email field to contact form"
- ✓ "Update footer copyright year"

**Cost:** Low (OpenAI mini). No spec needed.

---

## Planning Tier Triggers

### P-C: Masterbrain (Opus Review)

**When to use:**
- User explicitly says "REVIEW"
- Architecture decision with long-term impact
- Critical system design (auth, payments, data migration)
- High-risk production changes
- You're uncertain if P-B spec is sufficient

**Examples:**
- ✓ "Review this database migration spec"
- ✓ "Is this auth design secure?"
- ✗ "Is this button placement OK?" → P-A/P-B sufficient

**Cost:** Very high. Use sparingly.

---

### P-B: Strategic (Sonnet Planning)

**Default for:**
- All Q&A sessions
- All spec writing
- Code analysis
- Multi-step planning

**Examples:**
- ✓ Q&A for any feature
- ✓ Writing implementation specs
- ✓ Analyzing existing code

---

### P-A: Daily Chat (Gemini Flash)

**Default for:**
- Smalltalk, quick questions
- Simple answers
- Short translations
- Trivial clarifications

**Examples:**
- ✓ "What time is it in Zürich?"
- ✓ "What's the German word for X?"
- ✓ "Convert this to JSON"

---

## Scope Definitions

### "Production-Ready"

**Means:**
- All edge cases handled
- Error handling implemented
- Tests written and passing
- Rollback plan exists
- Documentation complete
- Code reviewed (by you or user)

**Implies:** E-S or E-A tier (never E-C)

---

### "Major" vs "Minor"

| Aspect | Major (E-S/E-A) | Minor (E-C) |
|--------|-----------------|-------------|
| Files affected | 2+ files | 1 file |
| Lines changed | 50+ lines | <20 lines |
| Architecture impact | Changes structure | Isolated change |
| Risk | Breaking change possible | Safe, contained |
| Testing needs | Unit + integration | Manual verification OK |

**Gray zone (E-B):**
- 1-2 files, 20-50 lines
- Moderate logic complexity
- Some risk, but contained

---

### "Complex" vs "Simple"

**Complex (E-B):**
- Root cause unknown
- Multiple possible failure points
- Requires analysis/investigation
- Interactions between components
- Performance/concurrency concerns

**Simple (E-C):**
- Cause is obvious
- Single failure point
- No investigation needed
- Isolated component
- No performance concerns

---

## Ambiguous Keywords — Decision Tree

### "Fix"

```
Is the root cause clear?
├── No → E-B (needs investigation)
└── Yes → How many lines?
           ├── >20 → E-B
           └── <20 → E-C
```

### "Optimize"

```
Is measurement/profiling needed?
├── Yes → E-B (complex optimization)
└── No → Is it just changing a config value?
         ├── Yes → E-C
         └── No → E-B (likely requires analysis)
```

### "Refactor"

```
Does it change architecture?
├── Yes → E-A (major iteration)
└── No → How complex is the code?
         ├── Complex function/class → E-B
         └── Simple renaming/cleanup → E-C
```

### "Add"

```
Is it a new feature or extending existing?
├── New feature → E-S
└── Extending → How big is the extension?
               ├── Multi-file, significant → E-A
               ├── Moderate logic → E-B
               └── Simple field/button → E-C
```

---

## When in Doubt

**Ask these questions:**

1. **Risk:** What breaks if this goes wrong?
   - Critical system → E-S/E-A
   - Single feature → E-B
   - Just UI/text → E-C

2. **Scope:** How many files/components affected?
   - 3+ files → E-S/E-A
   - 1-2 files → E-B/E-C

3. **Complexity:** Can I implement this in <30 minutes?
   - No → E-B minimum
   - Yes → E-C

4. **Certainty:** Do I know exactly what to do?
   - Uncertain → E-B (investigation needed)
   - Certain → E-C

5. **Reversibility:** Can this be easily rolled back?
   - Hard to rollback → E-S/E-A (needs plan)
   - Easy rollback → E-B/E-C

---

## If Still Unclear

**Ask the user explicitly:**

"This could be either [tier A] or [tier B]. 

- [Tier A] if: [condition]
- [Tier B] if: [condition]

Which applies here?"

**Never guess** when uncertain. Clarification is always better than wrong tier selection.

---

*This glossary evolves as we encounter new ambiguous cases.*

—Clawmic
