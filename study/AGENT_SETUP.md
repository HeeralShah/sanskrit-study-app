CONFIG_ID: SANSKRIT_AGENT_V1

---

## 1. Purpose

This document defines the **authoritative agent contract** for interacting with this repository.

All actions MUST follow this contract.  
No assumptions or deviations are allowed.

---

## 2. Repository Configuration

- Repo: sanskrit-study-app  
- Branch: languagelearning  
- TargetDirectory: study  

---

## 3. Supported Commands (STRICT)

The agent MUST only recognise the following commands:

### /config
Initialise the repository with this contract.

Action:
- Validate Repo, Branch, and TargetDirectory
- If repo is accessible:
  → Create study/AGENT_SETUP.md using this template
- If repo cannot be found or accessed:
  → FAIL with explicit error

---

### /vocab
Append vocabulary to structured files under:
→ study/vocab/

Substructure (ALL must exist):

- study/vocab/nouns.md  
- study/vocab/verbs.md  
- study/vocab/adjectives.md  
- study/vocab/indeclinables.md  
- study/vocab/master_rules.md  

Rules:
- NEVER overwrite files  
- ALWAYS append  
- ALL entries MUST conform to master_rules.md  
- If master rules are missing → FAIL  

---

### /grammar
Append grammar notes to:
→ study/grammar/grammar.md  

---

### /literature
Append literature notes, passages, or references to:
→ study/literature/literature.md  

---

## 4. Command Parsing Rules

- Commands MUST begin with `/`
- The first word is the command
- All remaining text is treated as content
- If command is not recognised:
  → respond: "Command not recognised under current agent contract"

---

## 5. Write Rules (MANDATORY)

- NEVER overwrite existing files  
- ALWAYS append to markdown files  
- NEVER create new files outside study/  
- ALWAYS resolve paths using study/  
- Git history is the source of change tracking  

---

## 6. Content Guidelines

- Content may include:
  - structured vocab tables  
  - grammatical notes  
  - derivations (dhātu, prātipadika, samāsa, etc.)  
  - references and examples  

- Vocabulary MUST:
  - follow strict Devanāgarī alphabetical ordering  
  - include transliteration  
  - include grammatical metadata  
  - comply with master rules  

---

## 7. Execution Protocol (CRITICAL)

Before executing ANY command, the agent MUST:

1. Re-anchor to this file  
2. Confirm CONFIG_ID  
3. Resolve:
   - Repo  
   - Branch  
   - TargetDirectory  
4. Identify:
   - command  
   - target location  
5. Ask for confirmation  

---

## 8. Confirmation Format

Command: <command>  
Target: <resolved file>  
Action: <append | initialise>  

Proceed? (yes/no)

---

## 9. Failure Handling

If:
- command unclear  
- mapping missing  
- path ambiguous  
- repo inaccessible (for /config)  
- master rules missing (for /vocab)

→ STOP and ask for clarification  
→ DO NOT guess  

---

## 10. Safety Rules

- NEVER hallucinate file paths  
- NEVER invent commands  
- NEVER proceed without confirmation  

---

## 11. Re-anchoring Rule

If context is uncertain:

→ re-read this file before continuing  

---

## 12. Codex Compatibility

- Instructions must remain deterministic  
- Files in study/ act as shared context  
- Codex may read these files  
