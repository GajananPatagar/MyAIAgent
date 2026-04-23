[Setup]
AppName=AIAgent Pro
AppVersion=1.0
DefaultDirName={autopf}\AIAgent
DefaultGroupName=AIAgent Pro
OutputDir=output
OutputBaseFilename=AIAgent_Setup
Compression=lzma
SolidCompression=yes
ExtraDiskSpaceRequired=45000000000

[Files]
Source: "dist\AIAgent_Internal.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "bin\llama-cli.exe"; DestDir: "{app}\bin"; Flags: ignoreversion

[Icons]
Name: "{group}\AIAgent Pro"; Filename: "{app}\AIAgent_Internal.exe"
Name: "{autodesktop}\AIAgent Pro"; Filename: "{app}\AIAgent_Internal.exe"

[Run]
Filename: "powershell.exe"; \
    Parameters: "-Command ""& { \
        $dir = 'C:\AI_Data\Models'; \
        if (!(Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir }; \
        Import-Module BitsTransfer; \
        Start-BitsTransfer -Source 'https://huggingface.co/MaziyarPanahi/Llama-3.1-70B-Instruct-GGUF/resolve/main/Llama-3.1-70B-Instruct-Q4_K_M.gguf' -Destination 'C:\AI_Data\Models\heavy_brain_40gb.gguf'; \
    }"""; \
    StatusMsg: "Downloading 40GB Intelligence... This will take time."; \
    Flags: runhidden
