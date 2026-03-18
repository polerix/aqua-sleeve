import sys
import subprocess
import json
import time
from datetime import datetime

def run_git(args):
    start_time = time.time()
    try:
        result = subprocess.run(["git"] + args, capture_output=True, text=True, check=True)
        return {
            "status": "success",
            "command": f"git {' '.join(args)}",
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "duration_ms": round((time.time() - start_time) * 1000, 2),
            "timestamp": datetime.now().isoformat()
        }
    except subprocess.CalledProcessError as e:
        return {
            "status": "error",
            "command": f"git {' '.join(args)}",
            "exit_code": e.returncode,
            "stdout": e.stdout.strip(),
            "stderr": e.stderr.strip(),
            "duration_ms": round((time.time() - start_time) * 1000, 2),
            "timestamp": datetime.now().isoformat()
        }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "message": "No git arguments provided."}))
        sys.exit(1)
    
    git_args = sys.argv[1:]
    envelope = run_git(git_args)
    print(json.dumps(envelope, indent=2))
