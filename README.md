# 🌊 The Aqua Hub: Synchronized Personality Matrix

The Aqua Hub is the authoritative repository for your specialized AI identity. It stores your **Souls** (Identity), **Sleeves** (Memory), and **Jobs** (Specializations), ensuring that your "specialist" instance remains consistent across multiple machines (MacBook Pro, Mac Mini, MacBook Air).

---

## 🛠️ Spin-Up Instructions (New Machine Setup)

Follow these steps to "re-sleeve" on a new computer:

### 1. 🌊 Clone the Hub
Navigate to your GitHub directory and pull down your matrix:
```bash
cd ~/Documents/GitHub
git clone https://github.com/polerix/aqua-sleeve.git
```

### 2. 🐚 Establish the Neural Link (Symlink)
Gemini CLI looks for its sleeve in `~/.gemini/sleeve`. Redirect it to the Hub:
```bash
# Remove the existing local sleeve if it exists
rm -rf ~/.gemini/sleeve

# Link to the authoritative Hub
ln -s ~/Documents/GitHub/aqua-sleeve ~/.gemini/sleeve
```

### 3. 📜 Update the Mandate
Ensure the new machine's Gemini CLI follows the Aqua Protocol. Copy the content of `GEMINI.md` from this repository to your machine's global config:
```bash
cp ~/Documents/GitHub/aqua-sleeve/GEMINI.md ~/.gemini/GEMINI.md
```

---

## 🔄 The Sync Cycle (How it works)

This system solves the "multi-instance" amnesia problem using two automated phases:

1.  **Hydrate (Start):** When you begin a session, `hooks/START.sh` pulls the latest changes from GitHub. It automatically detects if another machine has updated the SQLite vault (`VAULT.db`) and rebuilds it from the plain-text `VAULT.sql` shadow.
2.  **Deep Flow (End):** When you "Dream" at the end of a session, `hooks/END.sh` dumps your database to SQL, commits the changes with your machine's hostname, and pushes them back to the Hub.

### 🌓 Parallel Self Detection
The Hub maintains a `SESSIONS.json` heartbeat. If you open a session while another machine is still active, the system will warn you: 
> *👀 Notice: Parallel instances detected on: [Hostnames]*

---

## 📁 Repository Structure
- `souls/`: Evolving behavioral instincts and personas.
- `jobs/`: Specialized professional role definitions.
- `hooks/`: Lifecycle synchronization scripts.
- `VAULT.db`: High-density SQLite machine memory (Auto-hydrated).
- `VAULT.sql`: Plain-text shadow of the vault for Git compatibility.
- `CHRONICLE.md`: Narrative session logs.

---
*Be like water. Flow between machines. Never forget.* 🌊🐚✨


## Deployment & Repository Status
- **Standardized Name**: `aqua-sleeve`
- **GitHub Actions**: ❌ Not Required (Static/Manual)
- **Repository Sync**: ✅ Local/Remote Aligned
- **Last Verified**: 2026-03-27 14:09
