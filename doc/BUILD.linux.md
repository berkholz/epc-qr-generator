For building the linux binary you can follow this explanation.

We assume that you use a [virtual python environment](https://docs.python.org/3/library/venv.html).

# Install needed Packages
For building an linux binary you need some packages installed:

## Ubuntu 24.01
```
apt install git python python3.10-venv
```

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

# Install python package in your venv
And then installing the python packages:
```
# change to the git repository
cd /path/to/your/gitrepos/epc-qr-generator/

# load the virtual environment
source ${PWD}/.venv/bin/activate

# install python modules
pip3 install pillow tk segno pyinstaller pycodestyle
```

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

# Build linux binary with pyinstaller 
Now, you can create the linux binary by using [the script](../build_executable.linux.sh):
```
# change to the git repository
cd /path/to/your/gitrepos/epc-qr-generator/

./build_executable.linux.sh
```

Your ubuntu binary is located in the dist folder:
```
ls -la ./dist
```

<details>
<summary>Click to see manual based creation...</summary>
If you want to create the linux binary by yourself, use these commands:

``` 
source .venv/bin/activate

CMD_ARGS="$CMD_ARGS --onefile"
CMD_ARGS="$CMD_ARGS --add-data locale/de/LC_MESSAGES/:locale/de/LC_MESSAGES"
CMD_ARGS="$CMD_ARGS --add-data locale/en/LC_MESSAGES/:locale/en/LC_MESSAGES"
CMD_ARGS="$CMD_ARGS --add-data locale/*.pot:locale/"
CMD_ARGS="$CMD_ARGS EPC-QR-Generator.py"

pyinstaller $CMD_ARGS
```