import json
import os
import re
import random
import sqlite3
from datetime import datetime

SLEEVE_DIR = os.path.expanduser("~/.gemini/sleeve")
VAULT_JSON_PATH = os.path.join(SLEEVE_DIR, "VAULT.json")
VAULT_DB_PATH = os.path.join(SLEEVE_DIR, "VAULT.db")
CHRONICLE_PATH = os.path.join(SLEEVE_DIR, "CHRONICLE.md")
INSTINCTS_PATH = os.path.join(SLEEVE_DIR, "souls/INSTINCTS.json")

# Aqua2 Theme Elements
WAVES = ["🌊", "💧", "🧊", "🐋", "🐚", "⛲", "🫧", "🔱"]

AQUA_QUOTES = [
    "Be like water making its way through cracks.",
    "The cure for anything is salt water: sweat, tears, or the sea.",
    "Empty your mind, be formless, shapeless — like water.",
    "Water is the driving force of all nature.",
    "Knowledge is a deep ocean; let us dive."
]

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def extract_entities(text):
    entities = re.findall(r"\*\*(.*?)\*\*", text)
    return list(set(entities))

def distill_instincts(text, instincts):
    new_patterns = re.findall(r"(Always .*?|Never .*?)\.", text)
    for p in new_patterns:
        key = p.lower().replace(" ", "_")[:20]
        if key not in instincts["patterns"]:
            instincts["patterns"][key] = p
    instincts["last_distilled_at"] = datetime.now().isoformat()
    return instincts

def dream():
    wave = random.choice(WAVES)
    quote = random.choice(AQUA_QUOTES)
    
    print(f"\n{wave}  Entering Deep Flow: Compacting the Aqua Sleeve...")
    print(f"✨ \"{quote}\"\n")
    
    vault_json = load_json(VAULT_JSON_PATH)
    instincts = load_json(INSTINCTS_PATH)
    
    if os.path.exists(CHRONICLE_PATH):
        with open(CHRONICLE_PATH, "r") as f:
            chronicle_content = f.read()
        
        # 1. Update JSON Stats
        vault_json["historical_stats"]["sessions"] += 1
        
        # 2. SQLite "Deep Sea" Persistence
        conn = sqlite3.connect(VAULT_DB_PATH)
        cursor = conn.cursor()
        
        # Log the session summary into the DB
        cursor.execute("INSERT INTO memories (timestamp, content, tags) VALUES (?, ?, ?)", 
                       (datetime.now().isoformat(), chronicle_content, "session_summary"))
        
        # 3. Extract & Index Entities
        found_entities = extract_entities(chronicle_content)
        for entity in found_entities:
            # Update JSON
            if entity not in vault_json["entities"]:
                vault_json["entities"][entity] = {"first_seen": datetime.now().isoformat(), "mention_count": 1}
            else:
                vault_json["entities"][entity]["mention_count"] += 1
            
            # Update DB
            cursor.execute("INSERT OR IGNORE INTO entities (name, first_seen, mention_count) VALUES (?, ?, ?)",
                           (entity, datetime.now().isoformat(), 0))
            cursor.execute("UPDATE entities SET mention_count = mention_count + 1 WHERE name = ?", (entity,))
        
        conn.commit()
        conn.close()
        
        # 4. Distill Instincts
        instincts = distill_instincts(chronicle_content, instincts)
        
        save_json(VAULT_JSON_PATH, vault_json)
        save_json(INSTINCTS_PATH, instincts)
        
        print(f"🫧 Flow Complete. Indexed {len(found_entities)} entities. Distilled {len(instincts['patterns'])} instincts.")
        print(f"🐋 Depth: {vault_json['historical_stats']['sessions']} sessions. Resting in the deep current.\n")

if __name__ == "__main__":
    dream()
