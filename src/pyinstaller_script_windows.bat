echo Invoking pyinstaller to build the CSciBox executable...
pyinstaller --windowed --onefile --clean --noconfirm --icon=icon.ico cscience.spec
pause