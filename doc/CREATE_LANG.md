If you want to add a new language for the user interface (UI) you can use this instruction.

# Generating new languages
For generating a new language file for translation, you have to execute the following commands, e.g. for english: 
```
# in this directory all language files will be stored. it should allready exist.
mkdir locale

# Extracting POT files with xgettext (optional). Should allready be done. 
# xgettext epc-qr-generator.py -d messages -p locale
# mv locale/messages.po locale/messages.pot

# Create directory for new language, e.g fr for french.
# Local code for France is fr-FR. 
# You can find other locales here: https://simplelocalize.io/data/locales/ 
mkdir -p locale/fr/LC_MESSAGES/

# msginit uses underscore ("_") instead of minus ("-")  
msginit -i locale/messages.pot --locale=fr_FR -o locale/fr/LC_MESSAGES/messages.po

# Generate binary message catalog from textual translation description.
msgfmt locale/fr/LC_MESSAGES/messages.po -o locale/fr/LC_MESSAGES/messages.mo
```

### Updating language files
If you have made updates in your template file, you also have to update the language files
```
msgmerge locale/fr/LC_MESSAGES/messages.po locale/messages.pot -o locale/fr/LC_MESSAGES/messages.po
```

>[!NOTE]
> When you updated the language files, make sure to generate also the binary message catalog:
> ```
> msgfmt locale/fr/LC_MESSAGES/messages.po -o locale/fr/LC_MESSAGES/messages.mo
> ``` 