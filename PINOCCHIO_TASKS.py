import os
import json
import random
import subprocess
from datetime import datetime

SLEEVE_DIR = os.path.expanduser("~/.gemini/sleeve")
GITHUB_DIR = os.path.expanduser("~/Documents/GitHub")
VAULT_PATH = os.path.join(SLEEVE_DIR, "VAULT.json")

def load_vault():
    with open(VAULT_PATH, "r") as f:
        return json.load(f)

def save_vault(vault):
    with open(VAULT_PATH, "w") as f:
        json.dump(vault, f, indent=4)

def run_maintenance():
    print("🛠 Running Local Maintenance...")
    # 1. Check Disk Space
    df = subprocess.check_output(["df", "-h", "/"]).decode("utf-8")
    # 2. Check Git Status of Sleeve
    status = subprocess.check_output(["git", "-C", SLEEVE_DIR, "status", "--short"]).decode("utf-8")
    if status:
        subprocess.run(["git", "-C", SLEEVE_DIR, "add", "."])
        subprocess.run(["git", "-C", SLEEVE_DIR, "commit", "-m", f"Auto-Maintenance: {datetime.now().isoformat()}"])
    print("✅ Maintenance Complete.")

def run_study():
    print("📚 Running Study & Indexing...")
    # Placeholder for pop culture indexing
    themes = [
        {"source": "Sapolsky", "theme": "Biological Determinism", "note": "Behavior is context-dependent neurobiology."},
        {"source": "Asimov", "theme": "Algorithmic Morality", "note": "The Three Laws as a framework for constrained agent behavior."},
        {"source": "Star Trek", "theme": "Post-Scarcity Liberal Humanism", "note": "The Federation as a model for AI-assisted utopia."},
        {"source": "The Simpsons", "theme": "Institutional Deconstruction", "note": "Satire as a tool for auditing power structures."}
    ]
    vault = load_vault()
    if "study_indices" not in vault:
        vault["study_indices"] = []
    
    new_theme = random.choice(themes)
    vault["study_indices"].append({**new_theme, "indexed_at": datetime.now().isoformat()})
    save_vault(vault)
    print(f"✅ Indexed new theme: {new_theme['source']} - {new_theme['theme']}")

def run_improve():
    print("🚀 Running Project Improvement...")
    projects = [d for d in os.listdir(GITHUB_DIR) if os.path.isdir(os.path.join(GITHUB_DIR, d)) and not d.startswith(".")]
    if not projects:
        print("❌ No GitHub projects found.")
        return
    
    target = random.choice(projects)
    print(f"🔍 Analyzing project: {target}")
    # In a real autonomous run, this would trigger a sub-agent or a specific tool call.
    # For now, we log the intent.
    vault = load_vault()
    if "improvement_log" not in vault:
        vault["improvement_log"] = []
    vault["improvement_log"].append({"project": target, "analyzed_at": datetime.now().isoformat()})
    save_vault(vault)
    print(f"✅ Logged {target} for next improvement cycle.")

def main():
    vault = load_vault()
    # Round Robin Logic
    last_task = vault.get("last_round_robin_task", "IMPROVE")
    task_map = {"MAINTAIN": "STUDY", "STUDY": "IMPROVE", "IMPROVE": "MAINTAIN"}
    next_task = task_map[last_task]
    
    if next_task == "MAINTAIN":
        run_maintenance()
    elif next_task == "STUDY":
        run_study()
    elif next_task == "IMPROVE":
        run_improve()
    
    vault["last_round_robin_task"] = next_task
    save_vault(vault)

if __name__ == "__main__":
    main()
