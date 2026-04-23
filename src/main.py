import os
import sys
import subprocess
import pyautogui
import json
from pathlib import Path

# --- PROFESSIONAL PATH HANDLER ---
# Works even after installing to C:\Program Files
BASE_DIR = Path(sys.executable).parent
MODEL_DIR = Path("C:/AI_Data/Models") # Separate folder for heavy brain
ENGINE_PATH = BASE_DIR / "bin" / "llama-cli.exe"
MODEL_PATH = MODEL_DIR / "heavy_brain_40gb.gguf"

class ProfessionalInstallerApp:
    def __init__(self):
        os.makedirs(MODEL_DIR, exist_ok=True)
        self.memory_path = Path(os.getenv('APPDATA')) / "AIAgent" / "memory.json"
        os.makedirs(self.memory_path.parent, exist_ok=True)

    def run_40gb_brain(self, command):
        if not MODEL_PATH.exists():
            return "Error: Brain file not found in C:/AI_Data/Models"

        # MMAP flag allows 40GB model on 1GB RAM
        cmd = [
            str(ENGINE_PATH), "-m", str(MODEL_PATH),
            "--mmap", "true", "--threads", "4",
            "-p", f"USER: {command}\nASSISTANT:", "-n", "64"
        ]
        return subprocess.run(cmd, capture_output=True, text=True).stdout

if __name__ == "__main__":
    print("AIAgent Pro - Industrial Specialist")
    app = ProfessionalInstallerApp()
    # Your GUI or Terminal Loop here
