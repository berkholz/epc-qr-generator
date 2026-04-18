.\.venv\Scripts\Activate.ps1

pyinstaller --onefile --icon epc-qr-generator.logo.ico -w --add-data locale/de/LC_MESSAGES/:locale/de/LC_MESSAGES --add-data locale/*.pot:locale/ --add-data locale/en/LC_MESSAGES/:locale/en/LC_MESSAGES --hidden-import=tkinter --hidden-import=PIL._tkinter_finder EPC-QR-Generator.py

pause
