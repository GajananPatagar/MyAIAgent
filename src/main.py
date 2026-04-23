import os
import sys
import subprocess
import pyautogui
import json
from pathlib import Path

# --- DIRECTORY CONFIGURATION ---
# This ensures the app works correctly after being installed on C:
BASE_DIR = Path(sys.executable).parent
MODEL_PATH = Path("C:/AI_Data/Models/heavy_brain_40gb.gguf")
ENGINE_PATH = BASE_DIR / "bin" / "llama-cli.exe"

class AIAgentApp:
    def __init__(self):
        self.memory_file = Path(os.getenv('APPDATA')) / "AIAgentPro" / "learning.json"
        os.makedirs(self.memory_file.parent, exist_ok=True)
        self.learned_actions = self.load_memory()

    def load_memory(self):
        if self.memory_file.exists():
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        return {}

    def save_memory(self, command, coordinates):
        self.learned_actions[command] = coordinates
        with open(self.memory_file, 'w') as f:
            json.dump(self.learned_actions, f)

    def think_and_act(self, user_command):
        # 1. CHECK LOCAL CACHE (MILLISECOND SPEED)
        if user_command in self.learned_actions:
            pos = self.learned_actions[user_command]
            pyautogui.click(pos['x'], pos['y'])
            return f"Executed '{user_command}' from memory instantly."

        # 2. CALL 40GB BRAIN (DEEP REASONING)
        if not MODEL_PATH.exists():
            return "Error: 40GB Brain not found. Please run the installer again."

        print("Analyzing with 40GB Intelligence (Disk-Mapping Mode)...")
        # Flags for 1GB RAM usage: --mmap true, --n-gpu-layers 0
        process = subprocess.run([
            str(ENGINE_PATH),
            "-m", str(MODEL_PATH),
            "--mmap", "true",
            "--threads", "4",
            "-p", f"Task: {user_command}\nTarget: PCwin Ladder Logic\nInstruction:",
            "-n", "64"
        ], capture_output=True, text=True)

        return process.stdout

if __name__ == "__main__":
    app = AIAgentApp()
    print("--- AIAgent Pro: IHTM Maintenance Division ---")
    while True:
        cmd = input("Enter Command: ")
        if cmd.lower() == 'exit': break
        print(app.think_and_act(cmd))
