# OpenClaw Setup & Operations Guide

**Host:** `mac-mini-von-open`  
**User:** `remobot`  
**Letzte Aktualisierung:** 2026-02-20

---

## Aktueller Setup-Status

### Gateway Service
- **Typ:** macOS LaunchAgent
- **Config:** `~/Library/LaunchAgents/ai.openclaw.gateway.plist`
- **Wrapper:** `~/.openclaw/run-gateway.sh`
- **Port:** 18789
- **Auto-Start:** Ja (bei Login)

### Secrets Management
- **Datei:** `~/.openclaw/.env` (oder `secrets.env`)
- **Rechte:** `chmod 600` (nur User kann lesen)
- **Inhalt:** Provider API Keys (ANTHROPIC, OPENAI, SLACK, etc.)
- **Geladen via:** Wrapper-Script beim Service-Start

### Konfiguration
- **Hauptconfig:** `~/.openclaw/openclaw.json`
- **Backups:** `~/.openclaw/openclaw.json.bak*`
- **Logs:** `~/.openclaw/logs/gateway.log` und `gateway.err.log`

---

## Wichtige Commands

### Gateway Service Kontrolle

**Starten / Neu starten:**
```bash
launchctl kickstart -k gui/$UID/ai.openclaw.gateway
```

**Stoppen:**
```bash
launchctl bootout gui/$UID/ai.openclaw.gateway
```

**Status prüfen:**
```bash
launchctl list | grep openclaw
# Exit Code 0 = OK, Exit Code 1 = Fehler
```

**Neu laden (nach plist-Änderung):**
```bash
launchctl bootout gui/$UID/ai.openclaw.gateway 2>/dev/null || true
launchctl bootstrap gui/$UID ~/Library/LaunchAgents/ai.openclaw.gateway.plist
launchctl kickstart -k gui/$UID/ai.openclaw.gateway
```

### Health & Diagnostics

**Gateway Health:**
```bash
npx openclaw health
```

**Logs anschauen:**
```bash
tail -f ~/.openclaw/logs/gateway.log
tail -f ~/.openclaw/logs/gateway.err.log
```

**Device Pairing:**
```bash
npx openclaw devices list
npx openclaw devices approve <REQUEST_ID>
```

**Channel Pairing (Slack/Telegram DMs):**
```bash
npx openclaw pairing list slack
npx openclaw pairing approve slack <CODE>
```

### TUI (Terminal Interface)

**Starten:**
```bash
npx openclaw tui
```

**Nützliche Shortcuts im TUI:**
- `Ctrl+L` → Model-Picker
- `Ctrl+G` → Agent-Picker
- `Ctrl+P` → Session-Picker
- `Ctrl+D` → Exit
- `/model <name>` → Modell wechseln
- `/status` → Session-Info
- `/help` → Alle Befehle

---

## Konfiguration anpassen

### Channels aktivieren/deaktivieren

```bash
npx openclaw config set channels.slack.enabled true
npx openclaw config set channels.telegram.enabled true
```

### Modell ändern

```bash
npx openclaw config set agents.defaults.model.primary "anthropic/claude-sonnet-4-5"
```

### Config anschauen

```bash
npx openclaw config get agents.defaults.model
npx openclaw config get channels.slack
```

---

## Secrets rotieren (API Keys ändern)

**Wenn API-Keys erneuert werden müssen:**

1. **Neue Keys generieren** (bei Provider)

2. **`.env` aktualisieren:**
```bash
nano ~/.openclaw/.env
# Oder: ~/.openclaw/secrets.env (je nachdem was verwendet wird)
```

3. **Service neu starten:**
```bash
launchctl kickstart -k gui/$UID/ai.openclaw.gateway
```

4. **Prüfen:**
```bash
tail -n 20 ~/.openclaw/logs/gateway.err.log
npx openclaw health
```

---

## Troubleshooting

### "gateway closed (1008): pairing required"

**Lösung:** Device-Pairing durchführen
```bash
npx openclaw devices list
npx openclaw devices approve <REQUEST_ID>
```

### "missing API keys" in Logs

**Lösung:** Prüfen, ob `.env` korrekt geladen wird
```bash
ls -la ~/.openclaw/.env  # oder secrets.env
cat ~/.openclaw/run-gateway.sh  # Prüfen ob source-Zeile da ist
```

### Service startet nicht (Exit Code 1)

**Diagnose:**
```bash
tail -n 50 ~/.openclaw/logs/gateway.err.log
launchctl print gui/$UID/ai.openclaw.gateway
```

### Channels funktionieren nicht

**Prüfen:**
```bash
npx openclaw channels status --probe
npx openclaw config get channels.slack.enabled
npx openclaw config get channels.telegram.enabled
```

---

## Model-Routing (Clawmic's Tier-System)

Das in `context/model-routing-spec.md` definierte Tier-System (P-A/P-B/P-C, E-S/E-A/E-B/E-C) ist **nicht automatisch** in OpenClaw implementiert.

**Umsetzung:**
- OpenClaw kann `primary` + `fallbacks` + Model-Katalog konfigurieren
- Das intelligente Tier-Switching muss als **Agent Instructions** umgesetzt werden
- Clawmic muss aktiv mit `/model` wechseln

**System Prompt Location:**
```bash
nano ~/.openclaw/workspace/AGENTS.md
# Oder: agents.list[].instructions in openclaw.json
```

---

## Backup & Recovery

### Config-Backup erstellen

```bash
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup-$(date +%Y%m%d)
```

### Auf Backup zurücksetzen

```bash
cp ~/.openclaw/openclaw.json.bak ~/.openclaw/openclaw.json
launchctl kickstart -k gui/$UID/ai.openclaw.gateway
```

### Komplettes OpenClaw neu installieren

```bash
# Service stoppen
launchctl bootout gui/$UID/ai.openclaw.gateway

# Backups sichern
cp -r ~/.openclaw ~/.openclaw.backup-$(date +%Y%m%d)

# Neu installieren
npm i -g openclaw@latest
npx openclaw onboard
```

---

## Security Best Practices

Aus `Open_R/SECURITY.md`:

- ✅ Secrets nur in `~/.openclaw/.env` (nie in Git)
- ✅ `chmod 600` für alle Credential-Files
- ✅ Regelmäßig `openclaw security audit --deep`
- ✅ Keys alle 3-6 Monate rotieren
- ✅ `.openclaw/` nie in Cloud-Sync
- ✅ Logs regelmäßig prüfen auf Anomalien

---

## Kontakt & Dokumentation

- **OpenClaw Docs:** https://docs.openclaw.ai
- **GitHub:** https://github.com/openclaw/openclaw
- **Clawmic Identity:** `Documents/Open_R/IDENTITY.md`
- **Clawmic Security Policy:** `Documents/Open_R/SECURITY.md`
- **Model Routing Spec:** `Documents/Open_R/context/model-routing-spec.md`

---

*Dieses Dokument wird aktualisiert, wenn sich der Setup ändert.*
