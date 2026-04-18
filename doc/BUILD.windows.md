For building the windows binary you can follow this explanation.

We assume that you use a [virtual python environment](https://docs.python.org/3/library/venv.html).

# Install needed Packages
For building a windows binary you need some packages installed:

* [Python3 with Python install manager](https://www.python.org/downloads/)
* [git](https://git-scm.com/install/windows)
* [gettext](https://www.gnu.org/software/gettext/gettext.html)

# Check out the repository
 
For cloning the git repository you have to open a command prompt and type the following commands:
```
cd \path\to\your\gitrepos\
git clone https://github.com/berkholz/epc-qr-generator.git
```

# Create the virtual python environment (venv)
We are using a virtual environment to get all needed packages right in your environment.

First we create the virtual environment in the python app (powershell):
```
# change to the git repository
cd C:\path\to\your\gitrepos\epc-qr-generator\

# create the virtual environment
py -m venv .\.venv

# load the virtual environment
.\.venv\Scripts\activate.ps1
```

# Install python package in your venv
And then installing the python packages (powershell):
```
# change to the git repository
cd C:\path\to\your\gitrepos\epc-qr-generator\

# load the virtual environment
.\.venv\Scripts\activate.ps1

# install python modules
pip install pillow tk segno pyinstaller pycodestyle
```

> [!NOTE]
> The python package pycodestyle is optional.


# Create language files (binary message catalog)
If you are building the application for the first time, you have to create the binary message catalog. 

```
# change to the git repository
cd C:\path\to\your\gitrepos\epc-qr-generator\

# Generate binary message catalog from textual translation description for english and german.
msgfmt.exe locale/en/LC_MESSAGES/messages.po -o locale\en\LC_MESSAGES\messages.mo
msgfmt.exe locale/de/LC_MESSAGES/messages.po -o locale\de\LC_MESSAGES\messages.mo
```
> [!NOTE]
> Only two languages are yet supported: english, german.


# Build linux binary with pyinstaller 
Now, you can create the linux binary by using [the script](../build_executable.linux.sh) in powershell:
```
# change to the git repository
cd C:\path\to\your\gitrepos\epc-qr-generator\

.\build_executable.windows.ps1
```

<details>
<summary>Click to see manual based creation...</summary>
If you want to create the windows binary by yourself, use these commands:

``` 
.\.venv/bin/activate.ps1

pyinstaller --onefile --icon epc-qr-generator.logo.ico -w --add-data locale/de/LC_MESSAGES/:locale/de/LC_MESSAGES --add-data locale/*.pot:locale/ --add-data locale/en/LC_MESSAGES/:locale/en/LC_MESSAGES --hidden-import=tkinter --hidden-import=PIL._tkinter_finder EPC-QR-Generator.py

pause
```