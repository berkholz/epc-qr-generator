#!/bin/bash
source .venv/bin/activate

CMD_ARGS="$CMD_ARGS --icon ./epc-qr-generator.logo.ico"
CMD_ARGS="$CMD_ARGS --windowed"
CMD_ARGS="$CMD_ARGS --add-data locale/de/LC_MESSAGES/:locale/de/LC_MESSAGES"
CMD_ARGS="$CMD_ARGS --add-data locale/en/LC_MESSAGES/:locale/en/LC_MESSAGES"
CMD_ARGS="$CMD_ARGS --add-data locale/*.pot:locale/"
CMD_ARGS="$CMD_ARGS EPC-QR-Generator.py"

pyinstaller $CMD_ARGS

