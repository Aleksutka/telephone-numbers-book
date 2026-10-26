# pyinstaller guide in terminal
for windows with problems is python -m PyInstaller --onefile --windowed app_name.py --icon=icon.ico //all in one folder opened in terminal
for MacOS is pyinstaller --noconfirm --onedir --windowed --target-arch arm64 --collect-all customtkinter app_name.py --icon=icon.icns

# windows meanings:
--onefile - put all needed information in exe file
--windowed - without terminal to start normally
--icon-icon.ico - give exe file an icon (Windows have .ico)

# MacOS meanings:
--noconfirm - no need confirmation to update app if it's made
--onedir - make in one folder
--windowed - application without console
--target-arch arm64 - to open on any M Chipset
--collect-all customtkinter - to get all infromation of ctk in application
--icon-icon.icns - give application an icon (MacOS have .icns)
