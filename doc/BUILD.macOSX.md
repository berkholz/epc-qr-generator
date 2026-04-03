For building the macOSX binary application and DMG image you can follow this explanation.

We assume that you use a [virtual python environment](https://docs.python.org/3/library/venv.html) and [brew](https://brew.sh/de/). 

# Install brew
For the installation of brew, visit [brew homepage](https://brew.sh/).

# Install needed Packages
For building a macOSX application bundle you need some packages installed:
```
brew install git python create-dmg xgettext
```
> [!NOTE]
> 
> Usage of the packages:
> - create-dmg = application for building a dmg image
> - xgettext = tool for get text files (multi language support)


# Check out the repository
Now you have to check out the git repository:
```
cd /path/to/your/gitrepos/
git clone https://github.com/berkholz/epc-qr-generator.git
```

# Create the virtual python environment (venv)
We are using a virtual environment to get all needed packages right in your environment.

First we create the virutal environment:
```
# change to the git repository
cd /path/to/your/gitrepos/epc-qr-generator/

# create the virtual environment
python3 -m venv ${PWD}/.venv

# load the virtual environment
source ${PWD}/.venv/bin/activate
```

# Install python packages in your venv
And then installing the python packages:
```
# install python modules
pip3 install pillow tk segno pyinstaller pycodestyle
```
> [!IMPORTANT]
> When not allready done before, you have to load the venv first:
> ```
> source ${PWD}/.venv/bin/activate
> ```

> [!NOTE]
> The python package pycodestyle is optional.


# Create language files (binary message catalog)
If you are building the application for the first time, you have to create the binary message catalog. 

```
# change to the git repository
cd /path/to/your/gitrepos/epc-qr-generator/

# Generate binary message catalog from textual translation description for english and german.
msgfmt locale/en/LC_MESSAGES/messages.po -o locale/en/LC_MESSAGES/messages.mo
msgfmt locale/de/LC_MESSAGES/messages.po -o locale/de/LC_MESSAGES/messages.mo
```
> [!NOTE]
> Only two languages are yet supported: english, german.

# Build macOSX application bundle with pyinstaller 
Now, you can create the macOSX application bundle by using [the script](../build_executable.macosx.sh):
```
# change to the git repository
cd /path/to/your/gitrepos/epc-qr-generator/

./build_executable.macosx.sh
```

Your macOSX application bundle directory is located in the dist folder:
```
ls -la ./dist
```

<details>
<summary>Click to see manual based creation...</summary>
If you want to create the macOSX application bundle by yourself, use these commands:

``` 
source .venv/bin/activate

CMD_ARGS="$CMD_ARGS --icon ./epc-qr-generator.logo.ico"
CMD_ARGS="$CMD_ARGS --windowed"
CMD_ARGS="$CMD_ARGS --add-data locale/de/LC_MESSAGES/:locale/de/LC_MESSAGES"
CMD_ARGS="$CMD_ARGS --add-data locale/en/LC_MESSAGES/:locale/en/LC_MESSAGES"
CMD_ARGS="$CMD_ARGS --add-data locale/*.pot:locale/"
CMD_ARGS="$CMD_ARGS EPC-QR-Generator.py"

pyinstaller $CMD_ARGS
```


# Create the DMG image file
Now, you can create the dmg image file by using [the script](../build_dmg.macosx.sh):
```
# change to the git repository
cd /path/to/your/gitrepos/epc-qr-generator/

./build_dmg.macosx.sh
```

Your DMG file is located in the dist folder:
```
ls -la ./dist
```

<details>
<summary>Click to see manual based creation...</summary>
If you want to create the DMG file by yourself, use these commands:

```
# change to the git repository
cd /path/to/your/gitrepos/epc-qr-generator/

# create directory for .app folder and move app folder to it
mkdir -p dist/dmg/
mv dist/EPC-QR-Generator dist/dmg/

# create dmg image with app
create-dmg \
  --volname "EPC-QR-Generator" \
  --volicon "epc-qr-generator.logo.ico" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "EPC-QR-Generator.app" 175 120 \
  --hide-extension "EPC-QR-Generator.app" \
  --app-drop-link 425 120 \
  "dist/EPC-QR-Generator.dmg" \
  "dist/dmg/"
```
</details>