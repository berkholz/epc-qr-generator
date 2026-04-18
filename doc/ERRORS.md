
# Error #1 - No module named 'tkinter'
On Ubuntun 24.04 the error is thrown after building the binary with pyinstaller and executing the binary.

## message
```
Traceback (most recent call last):
  File "EPC-QR-Generator.py", line 2, in <module>
    import tkinter
ModuleNotFoundError: No module named 'tkinter'
[PYI-32359:ERROR] Failed to execute script 'EPC-QR-Generator' due to unhandled exception!
```

## resolution
```
apt get install python3-tk
```

# Error #2 - ERROR: On Linux, objdump is required.
On Ubuntun 24.04 as calling the build_exectuable.linux.sh the following error is thrown.

## message
```
ERROR: On Linux, objdump is required. It is typically provided by the 'binutils' package installable via your Linux distribution's package manager.
```

## resolution
```
apt get install binutils
```

# Error #3 - 'msgfmt' wurde nicht gefunden
When creating the binary message catalog with msgfmt command, the following error is thrown:

## message
```
Der Befehl 'msgfmt' wurde nicht gefunden, kann aber installiert werden mit:
sudo apt install gettext
```

## resolution
For Ubuntu 24.04:
```
apt install gettext
```

For Windows you have to install [gettext](https://www.gnu.org/software/gettext/gettext.html).


# Error #4 - No module named 'PIL._tkinter_finder'
In the application on pressing the generate button a dialog with the following message is thrown:

## message
No module named 'PIL._tkinter_finder'

## resolution
In the build_executable.linux.sh have to be added the following pinstaller option:
``` 
CMD_ARGS="$CMD_ARGS --hidden-import=PIL._tkinter_finder"
```