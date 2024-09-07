[Setup]
; Basic setup options
AppName=CurrencyConverter
AppVersion=1.0
DefaultDirName={pf}\CurrencyConverter
DefaultGroupName=CurrencyConverter
OutputDir={src}
OutputBaseFilename=CurrencyConverterSetup
Compression=lzma
SolidCompression=yes

[Files]
; Specify the files to be included in the installer
Source: "dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs
Source: "icons\*"; DestDir: "{app}\icons"; Flags: ignoreversion recursesubdirs
Source: "app.ui"; DestDir: "{app}"; Flags: ignoreversion
Source: "loadui.py"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Create a shortcut on the desktop with a custom icon
Name: "{group}\CurrencyConverter"; Filename: "{app}\loadui.exe"; IconFilename: "{app}\icons\custom_icon.ico"
Name: "{commondesktop}\CurrencyConverter"; Filename: "{app}\loadui.exe"; IconFilename: "{app}\icons\custom_icon.ico";

[Run]
; Run the application after installation
Filename: "{app}\loadui.exe"; Description: "{cm:LaunchProgram,MyApp}"; Flags: nowait postinstall skipifsilent
