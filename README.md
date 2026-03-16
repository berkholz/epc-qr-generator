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
pyinstaller EPC-QR-Generator.py
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
pyinstaller EPC-QR-Generator.py
```
## More Information about EPC
* https://de.wikipedia.org/wiki/EPC-QR-Code
* https://www.europeanpaymentscouncil.eu/sites/default/files/kb/file/2022-06/EPC121-16%20SCT%20Inst%20C2PSP%20IG%202023%20V1.0.pdf