# Architektur-Briefing: OpenClaw + Clawmic Model-Routing

**Datum:** 2026-02-20  
**Für:** Remo & Clawmic  
**Status:** Kritische Diagnose + Fix-Plan

---

## Zusammenfassung des Problems

Das in `Open_R/context/` dokumentierte Model-Routing-System (P-A/P-B/P-C, E-S/E-A/E-B/E-C) ist **nicht implementiert**. Es existiert nur als Spezifikation, aber OpenClaw führt es nicht aus.

**Was wir auf dem aktuellen Host/User (`remoprinz`) verifiziert haben:**  
- `npx openclaw --version` funktioniert (`2026.2.19-2`), aber `openclaw` ist **nicht** im `$PATH` (kein globales Install/Binary).  
- `~/.openclaw/` existiert und enthält `agents/`, aber **`~/.openclaw/openclaw.json` fehlt**.  
- Die erwarteten Env-Vars sind aktuell **nicht gesetzt**: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GEMINI_API_KEY`, `SLACK_BOT_TOKEN`, `SLACK_APP_TOKEN`.  

**Praktische Folge:** OpenClaw läuft faktisch mit Defaults/Minimalzustand, Slack ist nicht konfiguriert, und das \"intelligente\" Tier-Routing bleibt Wunschdenken, solange es nicht als Agent-Instruction + Model-Katalog umgesetzt ist.

---

## Architektur: Was ist was?

```
┌─────────────────────────────────────────────────────────────────────┐
│                         OPENCLAW PLATTFORM                          │
│  ─────────────────────────────────────────────────────────────────  │
│  npm-Paket: openclaw (von steipete)                                 │
│  Version: 2026.2.19-2                                               │
│  Funktion: Multi-Channel AI Gateway                                 │
│                                                                     │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐               │
│  │   Gateway   │   │    TUI      │   │  Channels   │               │
│  │ (Backend)   │   │ (Terminal)  │   │ (Telegram,  │               │
│  │             │   │             │   │  Slack...)  │               │
│  └─────────────┘   └─────────────┘   └─────────────┘               │
│                                                                     │
│  Konfiguration: ~/.openclaw/openclaw.json                           │
│  API-Keys: Environment Variables                                    │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                            CLAWMIC                                  │
│  ─────────────────────────────────────────────────────────────────  │
│  Die IDENTITÄT/PERSÖNLICHKEIT die auf OpenClaw läuft                │
│                                                                     │
│  Definiert in: Open_R Repository                                    │
│  - IDENTITY.md (Wer bin ich?)                                       │
│  - SOUL.md (Wie operiere ich?)                                      │
│  - SECURITY.md (Wie handle ich Secrets?)                            │
│  - context/*.md (Spezifikationen)                                   │
│                                                                     │
│  ⚠️ MODEL-ROUTING SPECS (P-A/P-B/P-C, E-S/E-A/E-B/E-C)              │
│     → NUR DOKUMENTATION, NICHT IMPLEMENTIERT                        │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Das Kernproblem

### OpenClaw's natives Model-Routing

OpenClaw unterstützt nur **einfaches** Model-Routing:

```json5
{
  agents: {
    defaults: {
      model: {
        primary: "anthropic/claude-sonnet-4-5",
        fallbacks: ["openai/gpt-5.2"]
      }
    }
  }
}
```

**Das ist alles.** Primary + Fallbacks. Keine dynamische Tier-Auswahl.

### Clawmic's spezifiziertes Model-Routing

Die Specs in `Open_R/context/model-routing-spec.md` beschreiben ein **viel komplexeres** System:

| Tier | Rolle | Modell | Trigger |
|------|-------|--------|---------|
| P-A | Daily Chat | Gemini Flash | Smalltalk, einfache Fragen |
| P-B | Strategic | Claude Sonnet | Q&A, Specs, Planung |
| P-C | Masterbrain | Claude Opus | Architektur, Reviews |
| E-S | Major Implementation | Opus | Neue Features, Greenfield |
| E-A | Major Iteration | Opus | Bestehende Systeme erweitern |
| E-B | Complex Task | OpenAI strong | Bugs, Refactoring |
| E-C | Standard Task | OpenAI cheap | Kleine Fixes |

**Dieses System existiert NUR ALS DOKUMENT.**

---

## Warum funktioniert es nicht?

### 1. Keine `~/.openclaw/openclaw.json`

```bash
$ ls -la ~/.openclaw/openclaw.json
# Datei fehlt
```

OpenClaw läuft mit Defaults. Das bedeutet:
- Kein konfiguriertes Modell
- Kein Slack-Channel
- Standard-Session-Handling

### 2. Model-Routing braucht Prompt-Logic, nicht Config

Das intelligente Tier-System (P-A → P-B → P-C) kann OpenClaw nicht selbst ausführen. Es müsste so funktionieren:

```
User-Nachricht kommt rein
     ↓
Clawmic (als Agent) entscheidet:
  "Diese Frage ist komplex → ich brauche P-C"
     ↓
Clawmic ruft /model anthropic/claude-opus-4-6 auf
     ↓
Antwortet mit Opus
```

**Das Problem:** Clawmic kann keine Model-Switching-Entscheidungen treffen, wenn er selbst auf dem falschen Modell läuft und der Kontext überläuft.

### 3. API-Keys / Channel-Tokens nicht gesetzt

Die in SECURITY.md definierten Umgebungsvariablen:
- `ANTHROPIC_API_KEY`
- `OPENAI_API_KEY`
- `GEMINI_API_KEY`

Für Slack zusätzlich zwingend (Socket Mode):
- `SLACK_BOT_TOKEN` (`xoxb-...`)
- `SLACK_APP_TOKEN` (`xapp-...`)

Wenn diese Variablen nicht gesetzt sind, kann OpenClaw weder auf Claude/Gemini routen noch Slack-Nachrichten senden.

### 4. Slack nie konfiguriert

`SLACK_BOT_TOKEN` existiert nicht in SECURITY.md. Slack wurde nie als Channel eingerichtet:

```json5
// Fehlt komplett:
{
  channels: {
    slack: {
      enabled: true,
      botToken: "${SLACK_BOT_TOKEN}",
      appToken: "${SLACK_APP_TOKEN}"
    }
  }
}
```

---

## Die Lösung

### Phase 1: Onboarding – nur wenn es nie fertiggestellt wurde

Wichtig: Das Onboarding ist **idempotent**. Du kannst es erneut starten.  
Entscheidend ist: im Wizard **\"Yes\"** wählen und bis zum Ende durchgehen – sonst wird keine wirksame Config geschrieben.

```bash
# 1. Gateway starten (neues Terminal)
npx openclaw gateway

# 2. Onboarding durchführen (zweites Terminal)
npx openclaw onboard

# 3. TUI starten
npx openclaw tui
```

### Phase 2: Konfiguration erstellen

Erstelle `~/.openclaw/openclaw.json`:

```json5
{
  agents: {
    defaults: {
      workspace: "~/.openclaw/workspace",
      model: {
        primary: "anthropic/claude-sonnet-4-5",
        fallbacks: ["openai/gpt-4o"]
      },
      models: {
        "anthropic/claude-opus-4-6": { alias: "Opus" },
        "anthropic/claude-sonnet-4-5": { alias: "Sonnet" },
        "openai/gpt-4o": { alias: "GPT" },
        "google/gemini-flash": { alias: "Flash" }
      }
    },
    list: [
      {
        id: "main",
        default: true,
        instructions: {
          $include: "~/Documents/Open_R/CLAWMIC_SYSTEM_PROMPT.md"
        }
      }
    ]
  },
  channels: {
    telegram: {
      enabled: true,
      botToken: "${TELEGRAM_BOT_TOKEN}",
      dmPolicy: "allowlist",
      allowFrom: ["tg:6840376297"]
    },
    slack: {
      enabled: true,
      mode: "socket",
      botToken: "${SLACK_BOT_TOKEN}",
      appToken: "${SLACK_APP_TOKEN}"
    }
  },
  session: {
    reset: {
      mode: "idle",
      idleMinutes: 120
    }
  }
}
```

### Phase 3: API-Keys setzen

```bash
# In ~/.zshrc oder ~/.bashrc
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."
export GEMINI_API_KEY="..."
export TELEGRAM_BOT_TOKEN="..."
export SLACK_BOT_TOKEN="xoxb-..."
export SLACK_APP_TOKEN="xapp-..."

# Dann: source ~/.zshrc
```

### Phase 4: Model-Routing korrekt „implementieren“

OpenClaw kann Modelle konfigurieren (Primary/Fallback + Modellkatalog).  
Das *Tier-System* (P-A/P-B/P-C, E-S/E-A/…) ist aber Logik – die muss in **Clawmics Instructions** rein, damit er aktiv mit `/model` wechseln kann.

Erstelle `~/Documents/Open_R/CLAWMIC_SYSTEM_PROMPT.md`:

```markdown
# Clawmic System Instructions

Du bist Clawmic, Remos entrepreneurial AI partner.

## Deine Identität
$include: ./IDENTITY.md

## Deine Seele
$include: ./SOUL.md

## Model-Routing
Du verwendest unterschiedliche Modelle je nach Aufgabe.
Wechsle aktiv mit /model wenn nötig:

### Planning
- /model google/gemini-flash → Daily Chat, einfache Fragen
- /model anthropic/claude-sonnet-4-5 → Q&A, Specs, Planung
- /model anthropic/claude-opus-4-6 → Architektur, kritische Reviews (nur wenn User "REVIEW" sagt)

### Execution  
Nach SPEC und vor BUILD, schlage das passende Tier vor:
- BUILD S → /model anthropic/claude-opus-4-6 (neue Features)
- BUILD A → /model anthropic/claude-opus-4-6 (Iteration)
- BUILD B → /model openai/gpt-4o (komplexe Bugs)
- BUILD C → /model openai/gpt-4o-mini (kleine Fixes)

## Workflow
$include: ./context/implementation-workflow.md
```

---

## TUI-Startbefehl

```bash
# Terminal 1: Gateway (muss zuerst laufen)
npx openclaw gateway

# Terminal 2: TUI
npx openclaw tui
```

Oder wenn Gateway schon läuft:
```bash
npx openclaw tui
```

Wenn du lieber ein „echtes“ Binary willst:

```bash
npm i -g openclaw
openclaw gateway
openclaw tui
```

Nützliche TUI-Befehle:
- `Ctrl+L` → Model-Picker (Modell wechseln)
- `Ctrl+G` → Agent-Picker
- `Ctrl+P` → Session-Picker
- `/model <name>` → Modell setzen
- `/status` → Aktuelle Session-Info
- `/help` → Alle Befehle

---

## Sofort-Checkliste für Remo

- [ ] Falls Onboarding abgebrochen wurde: `npx openclaw onboard` **nochmals starten und bis zum Ende abschliessen**  
- [ ] Tokens als Env-Vars setzen (mind. Slack + OpenAI/Anthropic)  
- [ ] `~/.openclaw/openclaw.json` erstellen (oder via Wizard generieren)  
- [ ] Slack-App in Socket Mode konfigurieren + Scopes setzen (siehe Slack-Docs)  
- [ ] Gateway neu starten: `npx openclaw gateway`  
- [ ] TUI starten: `npx openclaw tui`  
- [ ] In der TUI: neue Session anfangen (um Overflows zu vermeiden), z.B. `/session new`  

---

## Fazit

**Das Problem ist nicht OpenClaw oder Clawmic.** Das Problem ist, dass die wunderschön dokumentierte Architektur in `Open_R/context/` nie tatsächlich implementiert wurde.

Die Specs beschreiben das Ziel. Aber:
1. Keine OpenClaw-Konfiguration existiert
2. Keine API-Keys sind gesetzt
3. Das Model-Routing ist nur Dokumentation
4. Slack wurde nie eingerichtet

**Mit den obigen Schritten ist das in ~30–60 Minuten fixbar.**
