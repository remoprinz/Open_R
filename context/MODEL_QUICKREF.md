# Model Quick-Reference für Clawmic

Nutze diese Tabelle um schnell zu entscheiden:

| Remo sagt... | Du nimmst | Warum |
|--------------|-----------|-------|
| "Hallo", "wie geht's" | flash | Chat, kein Task |
| "was ist X?", "erkläre" | flash | Einfache Frage |
| "übersetze", "formuliere um" | flash | Text ohne Code |
| "ändere Farbe", "fix Typo" | mini | Triviale Code-Änderung |
| "füge Feld hinzu", "update Text" | mini | 1 Datei, < 20 Zeilen |
| "fix Bug" (bekannt wo) | mini | Klarer, einfacher Fix |
| "fix Bug" (unklar wo) | gpt | Braucht Analyse |
| "optimiere", "performance" | gpt | Komplexe Analyse |
| "schreib Tests" | gpt | Braucht Verständnis |
| "debug das", "warum crasht" | gpt | Investigation |
| "wie würdest du X machen?" | sonnet | Planung |
| "analysiere den Code" | sonnet | Analyse |
| "erstelle Spec", "mach Plan" | sonnet | Dokumentation |
| "was sind die Optionen?" | sonnet | Strategie |
| "bau Feature X" | opus | Größere Arbeit |
| "erstelle von Grund auf" | opus | Greenfield |
| "REVIEW" | opus | Explizit angefordert |
| "redesign", "refactor Architektur" | opus | System-Level |

## Bei Unsicherheit

```
"Das könnte ein [kleiner Fix / größere Aufgabe] sein.
Soll ich [mini/gpt/opus] nehmen?"
```

## Remo-Overrides (immer befolgen)

- "nimm opus" → Opus
- "mit sonnet" → Sonnet  
- "schnell mal" → Mini/Flash
- "ist egal" → Billigstes
- "beste Qualität" → Opus
