EPC-QR-Generator is a Python program for generating EPC QR codes. With this QR codes you can easily transfer money via your banking app.

# Running the application
## Prequisite
EPC-QR-Generator is made with Python 3.14.

To run with Python you need the following packages:
* tk
* segno
* pillow

Also, you have to generate the binary message catalog from textual translation description for english and german:
```
msgfmt locale/en/LC_MESSAGES/messages.po -o locale/en/LC_MESSAGES/messages.mo
msgfmt locale/de/LC_MESSAGES/messages.po -o locale/de/LC_MESSAGES/messages.mo
```

## Run
After that, you can run the application:
```
python3 EPC-QR-Generator.py
```

# Building binaries
If you want to create binary files for distribution purposes, you can have a look at the build instructions:
* [Linux](doc/BUILD.linux.md)
* [macOS](doc/BUILD.macOSX.md)

# Language support
## Create new languages
If you want to create a new language for the UI, please see [doc/CREATE_LANG](doc/CREATE_LANG.md).

## Update translations 
If you have added new text that is relevant for multilanguage support, you have to update the template and po and mo files of all languages. To see how, take a look at [doc/UPDATE_LANG](doc/UPDATE_LANG.md).


# More Information about EPC 
* https://de.wikipedia.org/wiki/EPC-QR-Code
* https://www.europeanpaymentscouncil.eu/
  * https://www.europeanpaymentscouncil.eu/sites/default/files/kb/file/2022-06/EPC121-16%20SCT%20Inst%20C2PSP%20IG%202023%20V1.0.pdf


# Other generators
If you don't mind to give your finance and private data to unknown, you may find these online generators interesting:
* https://www.qrcode-generator.de/solutions/epc-qr-code/
* https://epc-qr.eu/?form
