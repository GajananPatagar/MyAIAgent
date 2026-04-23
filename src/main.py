import os
import sys
import subprocess
import pyautogui
import base64
import json
from PIL import Image

# This finds the internal "baked-in" model after unzipping
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

MODEL_PATH = resource_path("model.gguf")
ENGINE_PATH = resource_path("llama-cli.exe")

class PortableAgent:
    def __init__(self):
        # Self-contained memory
        self.memory_path = os.path.join(os.getenv('APPDATA'), "agent_brain.json")
        self.memory = self.load_mem()

    def load_mem(self):
        if os.path.exists(self.memory_path):
            with open(self.memory_path, "r") as f: return json.load(f)
        return {}

    def run_inference(self, prompt, image_path):
        # Runs the bundled C++ engine directly
        cmd = [
            ENGINE_PATH, 
            "-m", MODEL_PATH, 
            "--image", image_path,
            "-p", f"USER: {prompt}\nASSISTANT:",
            "--temp", "0", "-n", "64"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout

    def execute(self, task):
        if task in self.memory:
            # MILLISECOND RESPONSE: Trigger learned action
            pyautogui.click(self.memory[task]['x'], self.memory[task]['y'])
            return "Executing learned task..."
        
        # VISION MODE: If new, take a screenshot and analyze
        scr = pyautogui.screenshot()
        scr.save("temp_scr.jpg")
        
        response = self.run_inference(f"Find the coordinates for {task}", "temp_scr.jpg")
        # (Parsing logic for coordinates here...)
        return "Task processed."

if __name__ == "__main__":
    app = PortableAgent()
    print("Portable AI Agent Ready (No Internet/No Downloads)")
    while True:
        query = input("Command: ")
        print(app.execute(query))
