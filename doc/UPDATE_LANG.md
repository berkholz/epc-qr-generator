If you add text to the code that is relevant for multi language support, then you have to update all the files. 
This gives you a short instruction for updating the language files for german and english.

Find messages in python file:
```
xgettext epc-qr-generator.py -d messages -p locale
```

Update the template:
```
mv locale/messages.po{,t}
``` 

Merge template with language specific files:
``` 
msgmerge locale/en/LC_MESSAGES/messages.po locale/messages.pot -o locale/en/LC_MESSAGES/messages.po
msgmerge locale/de/LC_MESSAGES/messages.po locale/messages.pot -o locale/de/LC_MESSAGES/messages.po
```

Generate the binary message catalog:
```
msgfmt locale/en/LC_MESSAGES/messages.po -o locale/en/LC_MESSAGES/messages.mo
msgfmt locale/de/LC_MESSAGES/messages.po -o locale/de/LC_MESSAGES/messages.mo
```

More information about gettext:
* https://docs.python.org/3/library/gettext.html
* https://phrase.com/blog/posts/translate-python-gnu-gettext/
* https://phrase.com/blog/posts/learn-gettext-tools-internationalization/