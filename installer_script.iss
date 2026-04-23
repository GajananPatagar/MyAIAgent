[Setup]
AppName=AIAgent Pro
AppVersion=1.0
AppPublisher=IHTM Maintenance
DefaultDirName={autopf}\AIAgent
DefaultGroupName=AIAgent Pro
OutputDir=output
OutputBaseFilename=AIAgent_Setup
Compression=lzma
SolidCompression=yes
; Require 42GB of free space (40GB for the brain + 2GB for the app)
ExtraDiskSpaceRequired=45097156608

[Files]
; Main application logic
Source: "dist\AIAgent_Internal.exe"; DestDir: "{app}"; Flags: ignoreversion
; AI Engine for low-RAM disk offloading
Source: "bin\llama-cli.exe"; DestDir: "{app}\bin"; Flags: ignoreversion

[Icons]
Name: "{group}\AIAgent Pro"; Filename: "{app}\AIAgent_Internal.exe"
Name: "{autodesktop}\AIAgent Pro"; Filename: "{app}\AIAgent_Internal.exe"

[Run]
; Robust download for 40GB brain using BitsTransfer (handles low-end PC network better)
Filename: "powershell.exe"; \
    Parameters: "-Command ""& { \
        $dir = 'C:\AI_Data\Models'; \
        if (!(Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir }; \
        Write-Host 'Initializing Background Intelligence Download...'; \
        Import-Module BitsTransfer; \
        Start-BitsTransfer -Source 'https://huggingface.co/MaziyarPanahi/Llama-3.1-70B-Instruct-GGUF/resolve/main/Llama-3.1-70B-Instruct-Q4_K_M.gguf' -Destination 'C:\AI_Data\Models\heavy_brain_40gb.gguf'; \
    }"""; \
    StatusMsg: "Downloading 40GB Intelligence Brain. This may take an hour depending on your internet. The app will be ready once this completes."; \
    Flags: runhidden

[UninstallDelete]
; Ensures the 40GB file is removed if you uninstall the app
Type: filesandordirs; Name: "C:\AI_Data\Models"
