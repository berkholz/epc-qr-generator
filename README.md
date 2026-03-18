# epc-qr-generator
Python program for generating EPC QR codes. With this program you can generate QR codes to transfer money via your banking app.

## Python version to run with
3.14

## Packages to install for building
* tk
* pillow
* segno

When using a virtual environment:
```
# change to the git repository
cd /path/to/gitrepository/epc-qr-generator/

# create the virtual environment
python3 -m venv ./

# load the virtual environment
source /path/to/gitrepository/epc-qr-generator/.venv/bin/activate

# install python modules
pip3 install pillow tk segno
```

## Build with pyinstaller
To build it with pyinstaller for generating binaries for executing without python:
```
# change to the git repository
cd /path/to/gitrepository/epc-qr-generator/

# create binaries with pyinstaller
pyinstaller --onefile EPC-QR-Generator.py
```

If you have setup a virtual environment, you can:
```
# change to the git repository
cd /path/to/gitrepository/epc-qr-generator/

# create the virtual environment
python3 -m venv ./

# load the virtual environment
source /path/to/gitrepository/epc-qr-generator/.venv/bin/activate

# install python modules and pyinstaller
pip3 install pillow tk segno pyinstaller pycodestyle

# create binaries with pyinstaller
pyinstaller --onefile EPC-QR-Generator.py
```
## Running EPC-QR-Generator
To run with python:
´´´´
python3 EPC-QR-Generator.py
´´´

To run the binary, just double click the application.

> [!NOTE]
> If you execute the macOSx binary the start of the application could be delayed for 5 seconds. Please wait 5 seconds to let the application window appear.

## Generating new languages
For generating a new language file for tranlation, you have to execute the following commands, e.g. for englisch: 
```
mkdir locale
# extracting POT files with xgettext 
xgettext epc-qr-generator.py -d messages -p locale
mv locale/messages.po locale/messages.pot
mkdir -p locale/en/LC_MESSAGES/
msginit -i locale/messages.pot --locale=en_EN -o locale/en/LC_MESSAGES/messages.po
msgfmt locale/en/LC_MESSAGES/messages.po -o locale/en/LC_MESSAGES/messages.mo
```

### Updating languages
```
msgmerge locale/en/LC_MESSAGES/messages.po locale/messages.pot -o locale/en/LC_MESSAGES/messages.po
msgmerge locale/de/LC_MESSAGES/messages.po locale/messages.pot -o locale/de/LC_MESSAGES/messages.po

```

## More Information about EPC
* https://de.wikipedia.org/wiki/EPC-QR-Code
* https://www.europeanpaymentscouncil.eu/sites/default/files/kb/file/2022-06/EPC121-16%20SCT%20Inst%20C2PSP%20IG%202023%20V1.0.pdf