import os
import json
import sqlite3
import subprocess
import socket
from datetime import datetime

SLEEVE_DIR = os.path.expanduser("~/.gemini/sleeve")
VAULT_DB = os.path.join(SLEEVE_DIR, "VAULT.db")
VAULT_SQL = os.path.join(SLEEVE_DIR, "VAULT.sql")
SESSIONS_FILE = os.path.join(SLEEVE_DIR, "SESSIONS.json")

def run_cmd(args):
    """Secure command execution using subprocess lists (no shell=True)."""
    try:
        # Use a list of arguments to prevent command injection
        result = subprocess.run(args, capture_output=True, text=True, cwd=SLEEVE_DIR)
        if result.returncode != 0:
            print(f"❌ Error running command: {' '.join(args)}\n{result.stderr.strip()}")
        return result.stdout.strip()
    except Exception as e:
        print(f"❌ Exception during {' '.join(args)}: {e}")
        return f"Error: {e}"

def dump_db():
    print("📤 Shadowing Deep Sea Vault to SQL...")
    if os.path.exists(VAULT_DB):
        # Securely handle redirection in Python instead of the shell
        try:
            with open(VAULT_SQL, "w") as f:
                subprocess.run(["sqlite3", VAULT_DB, ".dump"], stdout=f, check=True)
        except Exception as e:
            print(f"❌ Database dump failed: {e}")

def restore_db():
    if os.path.exists(VAULT_SQL):
        # Only restore if SQL is newer than DB
        sql_mtime = os.path.getmtime(VAULT_SQL)
        db_mtime = os.path.getmtime(VAULT_DB) if os.path.exists(VAULT_DB) else 0
        
        if sql_mtime > db_mtime:
            print("📥 Hydrating Deep Sea Vault from SQL...")
            if os.path.exists(VAULT_DB): os.remove(VAULT_DB)
            try:
                with open(VAULT_SQL, "r") as f:
                    subprocess.run(["sqlite3", VAULT_DB], stdin=f, check=True)
            except Exception as e:
                print(f"❌ Database hydration failed: {e}")

def update_heartbeat():
    hostname = socket.gethostname()
    now = datetime.now().isoformat()
    
    sessions = {}
    if os.path.exists(SESSIONS_FILE):
        try:
            with open(SESSIONS_FILE, "r") as f:
                sessions = json.load(f)
        except: pass
    
    sessions[hostname] = {
        "last_seen": now,
        "pid": os.getpid()
    }
    
    # Check for parallel selves (within 1 hour)
    others = [h for h, d in sessions.items() if h != hostname]
    if others:
        print(f"👀 Notice: Parallel instances detected on: {', '.join(others)}")
    
    with open(SESSIONS_FILE, "w") as f:
        json.dump(sessions, f, indent=4)

def sync_pull():
    print("🌊 Pulling latest personality matrix from the current...")
    run_cmd(["git", "pull", "--rebase", "origin", "master"])
    restore_db()

def sync_push(msg="Memory Flush"):
    dump_db()
    print("🚀 Pushing insights to the Aqua Hub...")
    # EXPLICIT FILE LIST: Never use 'git add .' to avoid leaking secrets/vaults
    safe_files = ["CHRONICLE.md", "GEMINI.md", "IDENTITY.md", "KNOWLEDGE.md", "REVERSE_REFLECT.md", "HUB.py", "PINOCCHIO_TASKS.py", "dream.py", "SESSIONS.json"]
    # Check which exist before adding
    to_add = [f for f in safe_files if os.path.exists(os.path.join(SLEEVE_DIR, f))]
    if to_add:
        run_cmd(["git", "add"] + to_add)
    
    commit_msg = f"🌊 {msg} ({socket.gethostname()})"
    run_cmd(["git", "commit", "-m", commit_msg])
    run_cmd(["git", "push", "origin", "master"])

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: hub.py [start|end|heartbeat]")
    else:
        cmd = sys.argv[1]
        if cmd == "start":
            sync_pull()
            update_heartbeat()
        elif cmd == "end":
            sync_push()
        elif cmd == "heartbeat":
            update_heartbeat()
