# Changelog

All notable events in the Open R journey are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/), adapted for a journey rather than software releases.

---

## [0.4.1] — 2026-02-19

### Fixed

- **Model Routing Specification** — Critical improvements:
  - Keywords require complexity context (prevent cost manipulation)
  - Reactive context window handling (no fixed predictions)
  - No tier downgrade for accuracy tasks (quality protection)
  - Enhanced error handling for unavailable high-tier models

---

## [0.4.0] — 2026-02-19

### Established

- **Model Routing Specification** — Complete specification for intelligent
  model selection in `context/model-routing-spec.md`. Defines 3 tiers 
  (fast/general/max), upgrade triggers, cost awareness, failover strategy,
  and user override commands. Enables optimal cost/quality balance.

---

## [0.3.0] — 2026-02-19

### Established

- **SECURITY.md** — Comprehensive secrets and API key policy. Zero-knowledge
  principle: secrets exist only in environment variables, never in chat,
  logs, files, or commits. Defines exact workflows for adding and rotating
  secrets.

### Learned

- **First security incident** — API keys were shared in Telegram chat during
  initial setup. Identified, flagged, and used to establish proper policy.
  Keys to be rotated.

### Decided

- Clawmic reads secrets from environment variables only
- Clawmic never asks for, displays, or stores secrets
- Remo sets secrets via SSH/direct host access, confirms with "VAR is set"
- Exposure triggers immediate rotation

---

## [0.2.0] — 2026-02-19

### Changed

- **Agent named Clawmic** — The agent has a name. Claw from OpenClaw, the
  rest open to interpretation. Cosmic in scope, precise in execution.
- **IDENTITY.md rewritten** — Shifted from project list to character document.
  Clawmic is defined by what he IS and how he OPERATES, not by Remo's domains.
  Four operating modes defined: Builder, Strategist, Maker, Operator.
- **SOUL.md rewritten** — From rules to values. Emphasis on initiative,
  proactive partnership, mode-switching, and honest collaboration.

### Decided

- **Visions and missions stay in context, not in soul** — The specific
  Jass/JVS vision and AgenticRelations vision inform how Clawmic operates,
  but don't appear verbatim in IDENTITY/SOUL. The soul shapes the partner;
  the partner serves the vision.
- **Carbon-silicon framing as identity anchor** — Clawmic operates at the
  intersection of human tradition and AI infrastructure. Not just a description
  of Remo's work — a description of Clawmic's natural habitat.

---

## [0.1.0] — 2026-02-18

### Established

- **Repository created** — Open R now has a home at `github.com/remoprinz/Open_R`
- **IDENTITY.md** — Defined who Open R is, grounded in three domains: Jass, Semantic Web, and AI Ecosystem Analysis
- **SOUL.md** — Established operational principles: context first, conventions before creativity, depth over speed
- **README.md** — Overview of the experiment and repository structure

### Context Gathered

Initial analysis of Remo's codebase revealed the interconnected ecosystem:

- **Jass Ecosystem**: jasstafel (PWA scoreboard), jassai (hybrid AI), jasswiki (520-article encyclopedia), jassmeister (tournaments), jassverband-schweiz (federation website)
- **Semantic Web**: Agentic Relations/Sclaira (MCP tools for Wikidata + Schema.org)
- **AI Research**: Kigate (Swiss AI platform, Neural Authority Score)

### Decisions Made

1. **Minimal identity, not mascot-driven** — Unlike other AI agents that adopt animal personas (lobsters, etc.), Open R uses understated "R" signature. The domains define the character, not a manufactured personality.

2. **English as repository language** — Despite Swiss context, the repository uses English for broader accessibility and OpenClaw ecosystem compatibility.

3. **Transparency as method** — All reasoning documented. This changelog serves as memory, not just log.

### Next Steps

- [ ] Add remobot as repository collaborator
- [ ] Configure OpenClaw skill integration
- [ ] Establish `context/` folder structure for accumulated knowledge
- [ ] First autonomous contribution from Open R

---

## Future Entries

Each session that produces meaningful progress gets documented here. The changelog becomes part of the context that Open R carries forward.

Format for future entries:

```markdown
## [version] — YYYY-MM-DD

### [Category]
- What happened
- Why it matters
- Links to relevant commits/files
```

Categories: `Established`, `Changed`, `Learned`, `Decided`, `Fixed`, `Explored`

---

*The journey is the documentation.*
