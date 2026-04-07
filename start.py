import os
import sys
import time
import subprocess
import threading
import http.client
import json
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
BACKEND_PY = os.path.join(ROOT, "backend", "api.py")
REQUIREMENTS = os.path.join(ROOT, "backend", "requirements.txt")
PKG_JSON = os.path.join(ROOT, "package.json")
NODE_MODS = os.path.join(ROOT, "node_modules")

API_PORT = 3000

def log(msg, tag="INFO"):
    print(f"  [{tag}] {msg}")

def find_python():
    for cmd in ("python", "python3", "py"):
        if shutil.which(cmd):
            return cmd
    return sys.executable

def find_npm():
    for cmd in ("npm", "npm.cmd"):
        if shutil.which(cmd):
            return cmd
    return "npm"

def find_npx():
    for cmd in ("npx", "npx.cmd"):
        if shutil.which(cmd):
            return cmd
    return "npx"

def ensure_python_deps():
    log("Checking Python dependencies...")
    python = find_python()
    try:
        result = subprocess.run(
            [python, "-m", "pip", "install", "-r", REQUIREMENTS, "--quiet"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            log("Python dependencies: OK")
        else:
            log(f"pip error: {result.stderr[:200]}", "WARN")
    except Exception as e:
        log(f"Could not pip install: {e}", "WARN")

def ensure_node_deps():
    npm = find_npm()
    
    if not shutil.which("node") and not shutil.which("node.exe"):
        log("Node.js not found! Please install it from https://nodejs.org", "ERROR")
        sys.exit(1)

    if not os.path.isdir(NODE_MODS):
        log("Installing Node.js dependencies (this may take a minute)...")
        try:
            result = subprocess.run(
                [npm, "install"],
                cwd=ROOT, capture_output=True, text=True,
                shell=True
            )
            if result.returncode == 0:
                log("Node dependencies: OK")
            else:
                log(f"npm install error:\n{result.stderr[:400]}", "ERROR")
                sys.exit(1)
        except Exception as e:
            log(f"Failed to run npm install: {e}", "ERROR")
            sys.exit(1)
    else:
        log("Node dependencies: OK")

backend_proc = None

def start_backend():
    global backend_proc
    python = find_python()
    log(f"Starting Python backend (port {API_PORT})...")
    backend_proc = subprocess.Popen(
        [python, BACKEND_PY],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    def stream_logs():
        for line in backend_proc.stdout:
            line = line.rstrip()
            if line:
                print(f"  [BACKEND] {line}")
    threading.Thread(target=stream_logs, daemon=True).start()

def wait_for_backend(timeout=25):
    log("Waiting for backend...")
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            conn = http.client.HTTPConnection("127.0.0.1", API_PORT, timeout=1)
            conn.request("GET", "/api/health")
            r = conn.getresponse()
            if r.status == 200:
                data = json.loads(r.read())
                log(f"Backend ready! v{data.get('version','?')}")
                return True
        except Exception:
            pass
        time.sleep(0.5)
    log("Backend did not respond! Check backend/api.py for errors.", "WARN")
    return False

def start_electron():
    npx = find_npx()
    log("Opening Perplexity GUI (Electron)...")
    try:
        electron_proc = subprocess.Popen(
            [npx, "electron", "."],
            cwd=ROOT,
            shell=True
        )
        return electron_proc
    except Exception as e:
        log(f"Failed to start Electron: {e}", "ERROR")
        sys.exit(1)

def main():
    print()
    print("  Perplexity GUI v2.0.0")
    print("  Premium AI Search Desktop App")
    print()

    ensure_python_deps()
    ensure_node_deps()
    start_backend()
    
    if not wait_for_backend():
        log("Cannot proceed without backend. Closing...", "ERROR")
        if backend_proc: backend_proc.terminate()
        sys.exit(1)

    electron = start_electron()
    
    try:
        electron.wait()
    except KeyboardInterrupt:
        pass

    log("Closing application...")
    if backend_proc and backend_proc.poll() is None:
        backend_proc.terminate()
        try:
            backend_proc.wait(timeout=3)
        except:
            backend_proc.kill()
    log("Done.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n  [INFO] Interrupted by user.")
        if backend_proc and backend_proc.poll() is None:
            backend_proc.terminate()
