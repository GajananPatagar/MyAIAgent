import pyautogui
import time
import base64
import requests
import json
import os
from PIL import Image
from io import BytesIO

# --- CONFIGURATION ---
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:4b"  # Lightweight vision model
KNOWLEDGE_FILE = "brain_data.bin"

class LocalAgent:
    def __init__(self):
        self.memory = self.load_memory()

    def load_memory(self):
        if os.path.exists(KNOWLEDGE_FILE):
            # Simulated lightweight encryption (Base64 + XOR)
            with open(KNOWLEDGE_FILE, "rb") as f:
                return json.loads(base64.b64decode(f.read()).decode())
        return {}

    def save_memory(self):
        data = base64.b64encode(json.dumps(self.memory).encode())
        with open(KNOWLEDGE_FILE, "wb") as f:
            f.write(data)

    def capture_screen(self):
        screenshot = pyautogui.screenshot()
        buffered = BytesIO()
        screenshot.save(buffered, format="JPEG", quality=50) # Lightweight quality
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

    def think_and_act(self, command):
        # 1. Check if we already "learned" this command
        if command in self.memory:
            self.execute_sequence(self.memory[command])
            return "Task completed from memory."

        # 2. If not in memory, ask the Vision Model
        img_b64 = self.capture_screen()
        prompt = f"Analyze this screen. To '{command}', provide the X,Y coordinates of the button to click. Format: CLICK X,Y"
        
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "images": [img_b64],
            "stream": False
        }

        try:
            response = requests.post(OLLAMA_URL, json=payload, timeout=5)
            action_text = response.json().get("response", "")
            return self.parse_action(action_text, command)
        except Exception as e:
            return f"Offline Error: Ensure Ollama is running with {MODEL_NAME}"

    def parse_action(self, text, command):
        if "CLICK" in text:
            # Example logic: "CLICK 500,300"
            coords = text.split("CLICK")[-1].strip().split(",")
            x, y = int(coords[0]), int(coords[1])
            pyautogui.click(x, y)
            # Self-Learning: Store the action
            self.memory[command] = [{"action": "click", "x": x, "y": y}]
            self.save_memory()
            return f"Learned and Clicked at {x}, {y}"
        return "Thinking..."

    def execute_sequence(self, sequence):
        for step in sequence:
            if step["action"] == "click":
                pyautogui.click(step["x"], step["y"])
                time.sleep(0.5)

if __name__ == "__main__":
    agent = LocalAgent()
    print("Agent Active. Type a command (e.g., 'Open Chrome'):")
    while True:
        cmd = input(">>> ")
        print(agent.think_and_act(cmd))
