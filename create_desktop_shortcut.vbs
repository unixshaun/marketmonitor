' VBS script to create a desktop shortcut for Crypto Widget
' Double-click this file to create the shortcut

Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Get the current directory
ScriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
TargetFile = ScriptDir & "\run_crypto_widget.bat"
DesktopPath = WshShell.SpecialFolders("Desktop")
ShortcutPath = DesktopPath & "\Crypto Widget.lnk"

' Create the shortcut
Set Shortcut = WshShell.CreateShortcut(ShortcutPath)
Shortcut.TargetPath = TargetFile
Shortcut.WorkingDirectory = ScriptDir
Shortcut.IconLocation = "C:\Windows\System32\shell32.dll,277"
Shortcut.Description = "Launch Crypto Price Widget"
Shortcut.Save

MsgBox "Desktop shortcut created successfully!" & vbCrLf & vbCrLf & "You can now find 'Crypto Widget' on your desktop.", vbInformation, "Success"