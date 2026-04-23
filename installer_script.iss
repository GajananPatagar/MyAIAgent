[Setup]
AppName=AIAgent Pro
AppVersion=1.0
DefaultDirName={autopf}\AIAgent
DefaultGroupName=AIAgent Pro
OutputDir=output
OutputBaseFilename=AIAgent_Setup
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\AIAgent_Internal.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "bin\llama-cli.exe"; DestDir: "{app}\bin"; Flags: ignoreversion

[Icons]
Name: "{group}\AIAgent Pro"; Filename: "{app}\AIAgent_Internal.exe"
Name: "{autodesktop}\AIAgent Pro"; Filename: "{app}\AIAgent_Internal.exe"

[Run]
; Downloads the 40GB brain to the local machine during installation
Filename: "powershell.exe"; Parameters: "-Command ""New-Item -ItemType Directory -Force -Path C:\AI_Data\Models; Invoke-WebRequest -Uri 'https://huggingface.co/MaziyarPanahi/Llama-3.1-70B-Instruct-GGUF/resolve/main/Llama-3.1-70B-Instruct-Q4_K_M.gguf' -OutFile 'C:\AI_Data\Models\heavy_brain_40gb.gguf'"""; StatusMsg: "Downloading 40GB Intelligence Brain (This may take an hour)..."
