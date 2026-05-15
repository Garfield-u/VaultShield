[Setup]
AppName=VaultShield
AppVersion=1.0.0
DefaultDirName={pf}\VaultShield
DefaultGroupName=VaultShield
OutputDir=installer_output
OutputBaseFilename=VaultShieldInstaller
Compression=lzma
SolidCompression=yes

[Files]
Source: "VaultShield.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\VaultShield"; Filename: "{app}\VaultShield.exe"
Name: "{commondesktop}\VaultShield"; Filename: "{app}\VaultShield.exe"

[Run]
Filename: "{app}\VaultShield.exe"; Flags: nowait postinstall skipifsilent