# Memory Reflection & Oversight Tool

## Logic: "Thinking Before Remembering"
Before any new fact is promoted to `KNOWLEDGE.md`, it MUST pass this three-gate rationality check:

1.  **Relevance Gate:** Is this information a durable fact (e.g., "The user's project is in `/X/Y`") or a transient session event (e.g., "The terminal had an error")? **Durable Facts ONLY.**
2.  **Integrity Gate:** Does this fact contradict any existing knowledge in the current sleeve? If yes, the agent must investigate the conflict before updating.
3.  **Compartment Gate:** Should this fact live in the **Global Sleeve** (`~/.gemini/sleeve/`) or a **Project Overlay** (`./.sleeve/`)?

## Procedure (To be executed during "Memory Flush")
1.  **Draft:** Identify 3-5 potential "Memory Candidates" from the current session.
2.  **Reflect:** Apply the three gates to each candidate.
3.  **Audit:** If a candidate is "Global," append to `~/.gemini/sleeve/KNOWLEDGE.md`. If it's project-specific, check for `./.sleeve/KNOWLEDGE.md` and append there.
4.  **Commit:** Execute `git add . && git commit -m "Memory Promotion: [Brief Summary]"` in the appropriate sleeve directory.
5.  **Manifest:** Update `MANIFEST.json` with the new file hashes.
