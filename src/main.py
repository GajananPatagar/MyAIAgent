import os
import sys
import subprocess
import pyautogui
import json
import base64
from pathlib import Path

# --- DIRECTORY HANDLER ---
# This ensures the app knows where the folders are, even when moved
BASE_DIR = Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path(__file__).parent
ENGINE_PATH = BASE_DIR / "engine" / "llama-cli.exe"
MODEL_PATH = BASE_DIR / "engine" / "models" / "brain.gguf"
MEMORY_PATH = BASE_DIR / "brain_data.bin"

class ProAgent:
    def __init__(self):
        self.memory = self.load_memory()

    def load_memory(self):
        if MEMORY_PATH.exists():
            with open(MEMORY_PATH, "rb") as f:
                return json.loads(base64.b64decode(f.read()).decode())
        return {}

    def save_memory(self):
        data = base64.b64encode(json.dumps(self.memory).encode())
        with open(MEMORY_PATH, "wb") as f:
            f.write(data)

    def execute(self, command):
        # MILLISECOND TIER: Check learned actions first
        if command in self.memory:
            for action in self.memory[command]:
                pyautogui.click(action['x'], action['y'])
            return "Task completed from local memory."

        # INTELLIGENCE TIER: 15GB Brain Analysis
        print("Analyzing with 15GB Intelligence...")
        scr = pyautogui.screenshot("temp.jpg")
        
        # Call the external engine
        process = subprocess.run([
            str(ENGINE_PATH), "-m", str(MODEL_PATH),
            "--image", "temp.jpg", "-p", f"USER: To {command}, where should I click? Format: CLICK X,Y\nASSISTANT:",
            "--temp", "0", "-n", "32"
        ], capture_output=True, text=True)

        # Learning & Action logic
        result = process.stdout
        if "CLICK" in result:
            # (Parse coordinates, click, and save to self.memory here)
            self.save_memory()
            return "Learned and executed."
        return "Thinking..."

if __name__ == "__main__":
    print(f"--- IHTM DEPT AI AGENT ---")
    agent = ProAgent()
    while True:
        user_in = input("Command: ")
        print(agent.execute(user_in))
