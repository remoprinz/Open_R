#!/usr/bin/env python3
"""
OpenClaw Model Routing Setup Script
Konfiguriert Clawmic für intelligentes Model-Routing.

Ausführung: python3 ~/Documents/Open_R/scripts/setup_model_routing.py
"""

import json
import shutil
from pathlib import Path
from datetime import datetime

def main():
    print("=" * 60)
    print("🦞 OpenClaw Model Routing Setup")
    print("=" * 60)
    
    home = Path.home()
    config_path = home / ".openclaw" / "openclaw.json"
    workspace_path = home / ".openclaw" / "workspace"
    open_r_path = home / "Documents" / "Open_R"
    
    # 1. Backup erstellen
    if config_path.exists():
        backup_path = config_path.with_suffix(f".json.bak-{datetime.now().strftime('%Y%m%d-%H%M%S')}")
        shutil.copy(config_path, backup_path)
        print(f"✅ Backup erstellt: {backup_path.name}")
    
    # 2. Config laden
    if config_path.exists():
        config = json.loads(config_path.read_text())
    else:
        print("❌ openclaw.json nicht gefunden!")
        return
    
    # 3. Model-Config updaten
    agents = config.setdefault("agents", {})
    defaults = agents.setdefault("defaults", {})
    model = defaults.setdefault("model", {})
    
    # Primary auf Gemini Flash (billig)
    model["primary"] = "google/gemini-2.0-flash"
    model["fallbacks"] = ["openai/gpt-4o-mini", "openai/gpt-4o", "anthropic/claude-sonnet-4-5"]
    
    print("✅ Primary Model: google/gemini-2.0-flash")
    print("✅ Fallbacks: gpt-4o-mini → gpt-4o → sonnet")
    
    # 4. Models mit Aliases
    defaults["models"] = {
        "google/gemini-2.0-flash": {"alias": "flash"},
        "openai/gpt-4o-mini": {"alias": "mini"},
        "openai/gpt-4o": {"alias": "gpt"},
        "anthropic/claude-sonnet-4-5": {"alias": "sonnet"},
        "anthropic/claude-opus-4": {"alias": "opus"}
    }
    print("✅ Model-Aliases konfiguriert: flash, mini, gpt, sonnet, opus")
    
    # 5. Agent mit System Prompt (falls nicht vorhanden)
    agents_list = agents.setdefault("list", [])
    
    # Prüfen ob Clawmic Agent existiert
    clawmic_exists = any(a.get("id") == "clawmic" for a in agents_list)
    
    if not clawmic_exists:
        # Neuen Agent hinzufügen (ohne $include, da das Probleme macht)
        agents_list.append({
            "id": "clawmic",
            "default": True
        })
        print("✅ Clawmic Agent registriert")
    else:
        print("✅ Clawmic Agent bereits vorhanden")
    
    # 6. Config speichern
    config_path.write_text(json.dumps(config, indent=2) + "\n")
    print("✅ Config gespeichert")
    
    # 7. Workspace vorbereiten
    workspace_path.mkdir(parents=True, exist_ok=True)
    
    # System Prompt in Workspace kopieren (Symlink)
    system_prompt_src = open_r_path / "CLAWMIC_SYSTEM_PROMPT.md"
    system_prompt_dst = workspace_path / "AGENTS.md"
    
    if system_prompt_src.exists():
        # Kopiere statt Symlink (robuster)
        shutil.copy(system_prompt_src, system_prompt_dst)
        print(f"✅ System Prompt kopiert: {system_prompt_dst}")
    else:
        print(f"⚠️  System Prompt nicht gefunden: {system_prompt_src}")
    
    # Quick-Reference kopieren
    quickref_src = open_r_path / "context" / "MODEL_QUICKREF.md"
    quickref_dst = workspace_path / "MODEL_QUICKREF.md"
    
    if quickref_src.exists():
        shutil.copy(quickref_src, quickref_dst)
        print(f"✅ Quick-Reference kopiert: {quickref_dst}")
    
    # 8. Zusammenfassung
    print("\n" + "=" * 60)
    print("🎉 Setup abgeschlossen!")
    print("=" * 60)
    print("\nNächster Schritt:")
    print("  launchctl kickstart -k gui/$UID/ai.openclaw.gateway")
    print("\nDann im Chat testen:")
    print('  "Hallo!" (sollte Flash nutzen)')
    print('  "nimm opus" (sollte zu Opus wechseln)')
    print('  "bau ein neues Feature" (sollte fragen ob Opus)')
    print("=" * 60)

if __name__ == "__main__":
    main()
