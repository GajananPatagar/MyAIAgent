[Setup]
; --- Basic App Information ---
AppName=AIAgent Pro
AppVersion=1.0
AppPublisher=IHTM Maintenance
DefaultDirName={autopf}\AIAgent
DefaultGroupName=AIAgent Pro
OutputDir=output
OutputBaseFilename=AIAgent_Setup
Compression=lzma
SolidCompression=yes
; Ensures the user has enough space on C: drive for the 40GB brain
ExtraDiskSpaceRequired=42949672960

[Files]
; The main software logic (from your Python code)
Source: "dist\AIAgent_Internal.exe"; DestDir: "{app}"; Flags: ignoreversion
; The AI Engine (unzipped in the YAML build)
Source: "bin\llama-cli.exe"; DestDir: "{app}\bin"; Flags: ignoreversion

[Icons]
Name: "{group}\AIAgent Pro"; Filename: "{app}\AIAgent_Internal.exe"
Name: "{autodesktop}\AIAgent Pro"; Filename: "{app}\AIAgent_Internal.exe"

[Run]
; --- THE 40GB INTELLIGENCE DOWNLOAD ---
; This PowerShell command:
; 1. Creates the necessary data folder on the C: Drive
; 2. Downloads the massive 40GB brain file directly from HuggingFace
; 3. Uses a professional status message so the user knows it's working
Filename: "powershell.exe"; \
    Parameters: "-Command ""& { \
        $dir = 'C:\AI_Data\Models'; \
        if (!(Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir }; \
        Write-Host 'Downloading 40GB Intelligence Brain... Please wait.'; \
        Invoke-WebRequest -Uri 'https://huggingface.co/MaziyarPanahi/Llama-3.1-70B-Instruct-GGUF/resolve/main/Llama-3.1-70B-Instruct-Q4_K_M.gguf' -OutFile 'C:\AI_Data\Models\heavy_brain_40gb.gguf' \
    }"""; \
    StatusMsg: "Downloading 40GB Intelligence Brain (70B Parameters). This will take time depending on your internet speed..."; \
    Flags: runhidden

[UninstallDelete]
; Clean up the heavy brain file if the software is uninstalled
Type: filesandordirs; Name: "C:\AI_Data\Models"
