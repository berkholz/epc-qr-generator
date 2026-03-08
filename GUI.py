import tkinter
from tkinter import ttk, messagebox, simpledialog
import segno  # qr code generation
import tk
from PIL import Image, ImageTk

class EPCgenerator(tkinter.Frame):

    def __init__(self, parent=None):
        ttk.Frame.__init__(self, parent)
        self.menuBar = tkinter.Menu(parent)
        parent.config(menu=self.menuBar)
        self.fillMenuBar()
        self.pack()

        # Liste der Optionen
        self.ver_options = ["001", "002"]
        self.charset_options = ["1", "2", "3", "4", "5", "6", "7", "8"]
        self.ident_options = ["SCT", "INST"]

        # Eingabefelder
        self.service_tag_var = tkinter.StringVar(value="BCD")
        self.version_var = tkinter.StringVar(value=self.ver_options[0])
        self.charset_var = tkinter.StringVar(value=self.charset_options[0])
        self.ident_var = tkinter.StringVar(value=self.ident_options[0])
        self.name_var = tkinter.StringVar(value="")
        self.iban_var = tkinter.StringVar(value="")
        self.bic_var = tkinter.StringVar(value="")
        self.verwendungszweck_var = tkinter.StringVar(value="")
        self.betrag_var = tkinter.StringVar(value="0.00")

        self.createWidgets()

    def fillMenuBar(self):
        # definiere Datei Menü
        self.menuFile = tkinter.Menu(self.menuBar, tearoff=False)
        self.menuFile.add_command(label="Info", command=self.show_info)
        self.menuFile.add_command(label="IBAN-Rechner", command=self.iban_calculator_dialog)
        self.menuFile.add_separator()
        self.menuFile.add_command(label=" Beenden", command=self.quit)
        self.menuBar.add_cascade(label="Datei", menu=self.menuFile)

        # definiere Vorlagen Menü
        self.menuTemplates = tkinter.Menu(self.menuBar, tearoff=False)
        self.menuBar.add_cascade(label="Vorlagen", menu=self.menuTemplates)
        # definier submenü für vorlage -> einträge
        self.menuTemplatesEntries = tkinter.Menu(self.menuBar, tearoff=False)
        self.menuTemplatesEntries.add_command(label="Entry1", command=self.handler)
        self.menuTemplatesEntries.add_command(label="Entry2", command=self.handler)
        self.menuTemplates.add_cascade(label="Letzte Vorlagen...", menu=self.menuTemplatesEntries)

        # definiere Settings Menü
        self.menuSettings = tkinter.Menu(self.menuBar, tearoff=False)
        self.menuBar.add_cascade(label="Settings", menu=self.menuSettings)

        # definier submenü für settings -> language
        self.menuSettingsLanguage = tkinter.Menu(self.menuBar, tearoff=False)
        self.menuSettingsLanguage.add_command(label="Deutsch", command=self.handler)
        self.menuSettingsLanguage.add_command(label="English", command=self.handler)
        self.menuSettings.add_cascade(label="Language", menu=self.menuSettingsLanguage)

    def show_info(self):
        message = (f"EPC-Generator 0.1\n"
                   f"Build on 2026-03-08 (Weltfrauentag!)\n"
                   f"Copyright © 2026 Marcel Berkholz"
                   )
        infobox = tkinter.messagebox.showinfo("Info", message)

    def iban_calculator_dialog(self):
        self.kto_number = tkinter.StringVar()
        self.blz = tkinter.StringVar()
        self.lang = tkinter.StringVar(value="DE")
        self.application_window = tkinter.Tk()
        self.application_window.title("IBAN-Rechner")

        groupIBANcalculator = tkinter.LabelFrame(self.application_window, text="Kontodaten")

        self.langLabel = tkinter.Label(groupIBANcalculator, text="Länderkennung:")
        self.langLabel.grid(row=0, column=0)
        self.langEntry = tkinter.Entry(groupIBANcalculator, textvariable=self.lang)
        self.langEntry.grid(row=0, column=1)
        self.ktoLabel = tkinter.Label(groupIBANcalculator, text="KTO:")
        self.ktoLabel.grid(row=1, column=0)
        self.ktoEntry = tkinter.Entry(groupIBANcalculator, textvariable=self.kto_number)
        self.ktoEntry.grid(row=1, column=1)
        self.blzLabel = tkinter.Label(groupIBANcalculator, text="BLZ:")
        self.blzLabel.grid(row=2, column=0)
        self.blzEntry = tkinter.Entry(groupIBANcalculator, textvariable=self.blz)
        self.blzEntry.grid(row=2, column=1)
        self.calcButton = tkinter.Button(groupIBANcalculator, text="Calculate", command=self.calculate_iban)
        self.calcButton.grid(row=3, column=1,sticky=tkinter.NW)
        self.okButton = tkinter.Button(groupIBANcalculator, text="OK", command=self.calculate_iban_close)
        self.okButton.grid(row=3, column=1,sticky=tkinter.SE)
        groupIBANcalculator.pack(expand=True,fill="x")

        groupCalcResult = tkinter.LabelFrame(self.application_window, text="IBAN")
        self.resultText = tkinter.Text(master=groupCalcResult, height=10)
        self.resultText.grid(row=0, column=0)
        groupCalcResult.pack(expand=True,fill="x")

    def _modulo97(self, number: object) -> int:
        return number % 97

    def calculate_iban_close(self):
        if self.ktoEntry.get() != "" and self.blzEntry.get() != "":
            self.calculate_iban()
            self.application_window.destroy()
        else:
            self.application_window.destroy()

    def calculate_iban(self):
        kto_as_string = str(self.ktoEntry.get())
        blz_as_string = str(self.blzEntry.get())
        langCode = str(self.langEntry.get())

        if kto_as_string != "" and blz_as_string != "":
            kto_blz_string = kto_as_string + blz_as_string
            modulo_result = self._modulo97(int(kto_blz_string))
            iban_tmp = f"{langCode}{modulo_result}{blz_as_string}{kto_as_string}"
            self.iban_var.set(iban_tmp)
            self.resultText.delete(1.0, 'end')
            self.resultText.insert('end', iban_tmp)
        else:
            tkinter.messagebox.showwarning("Warning", "KTO und BLZ fehlen!")

    def handler(self):
        print("handler called")

    def createWidgets(self):
        # frame for default components
        frameDefault = tkinter.Frame(self)

        # labelFrame for default components
        groupDefaultData = tkinter.LabelFrame(frameDefault, text="Defaults")

        # label for version
        self.versionLabel = tkinter.Label(groupDefaultData, text="Version:").grid(row=0, column=0)

        # combobox for version
        self.versionCombobox = ttk.Combobox(
            groupDefaultData,
            textvariable=self.version_var,
            values=["001", "002"],
            state="readonly"
        )
        self.versionCombobox.grid(row=0, column=1)

        # label for character set
        self.charsetLabel = tkinter.Label(groupDefaultData, text="Character Set:").grid(row=1, column=0)

        # combobox for character set
        self.charsetCombobox = ttk.Combobox(
            groupDefaultData,
            textvariable=self.charset_var,
            values=["1", "2", "3", "4", "5", "6", "7", "8"],
            state="readonly"
        )
        self.charsetCombobox.grid(row=1, column=1)

        # label for identification
        self.identLabel = tkinter.Label(groupDefaultData, text="Identification:").grid(row=2, column=0)

        # combobox for identification
        self.identCombobox = ttk.Combobox(
            groupDefaultData,
            textvariable=self.ident_var,
            values=["SCT", "INST"],
            state="readonly"
        )
        self.identCombobox.grid(row=2, column=1)

        # labelFrame End
        groupDefaultData.pack(fill="x")
        frameDefault.pack(fill="x", expand=True)

        # -----

        frameCustom = tkinter.Frame(self)
        groupCustomData = tkinter.LabelFrame(frameCustom, text="Custom")
        # name
        self.nameLabel = tkinter.Label(groupCustomData, text="Name:").grid(row=0, column=0)
        self.nameEntry = tkinter.Entry(groupCustomData, textvariable=self.name_var).grid(row=0, column=1)

        self.ibanLabel = tkinter.Label(groupCustomData, text="IBAN:").grid(row=1, column=0)
        self.ibanEntry = tkinter.Entry(groupCustomData, textvariable=self.iban_var).grid(row=1, column=1)

        # BIC
        ttk.Label(groupCustomData, text="BIC:").grid(row=2, column=0)
        ttk.Entry(groupCustomData, textvariable=self.bic_var).grid(row=2, column=1)

        # Verwendungszweck
        ttk.Label(groupCustomData, text="Verwendungszweck:").grid(row=3, column=0)
        ttk.Entry(groupCustomData, textvariable=self.verwendungszweck_var).grid(row=3, column=1)

        # Betrag
        ttk.Label(groupCustomData, text="Betrag (€):").grid(row=4, column=0)
        ttk.Entry(groupCustomData, textvariable=self.betrag_var).grid(row=4, column=1)

        groupCustomData.pack(expand=True, fill="x", side="left")
        frameCustom.pack(fill="x", expand=True)

        # generate button
        frameButtons = tkinter.Frame(self)
        groupButtonFrame = tkinter.Frame(frameButtons)
        self.generateButton = tkinter.Button(groupButtonFrame, text="Generate", command=self.refresh_output)
        self.generateButton.grid(row=0, column=0)
        self.quitButton = tkinter.Button(groupButtonFrame, text="Quit", command=self.quit)
        self.quitButton.grid(row=0, column=1)
        groupButtonFrame.pack(expand=True, fill="x", padx=5, pady=20)
        frameButtons.pack(fill="x", expand=True)

        groupOutputText = tkinter.LabelFrame(self, text="Output-Text")
        # Textfeld für Ausgabe
        self.outputText = tkinter.Text(master=groupOutputText, height=10)
        self.outputText.grid(row=0, column=0)
        groupOutputText.pack(expand=True, fill="x")

        groupOutputPicture = tkinter.LabelFrame(self, text="Output-Picture")
        # Bild-Label
        self.bild_label = ttk.Label(groupOutputPicture)
        self.bild_label.grid(row=0, column=1)
        groupOutputPicture.pack(fill="x", expand=True)

    def print_vars(self):
        service_tag = self.service_tag_var.get()
        print(service_tag)
        version = self.versionCombobox.get()
        print(version)
        charset = self.charsetCombobox.get()
        print(charset)
        ident = self.identCombobox.get()
        print(ident)
        bic = self.bic_var.get()
        print(bic)
        name = self.name_var.get()
        print(name)
        iban = self.iban_var.get()
        print(iban)
        betrag = self.betrag_var.get()
        print(betrag)
        verwendungszweck = self.verwendungszweck_var.get()
        print(verwendungszweck)


    def refresh_output(self):
        self.print_vars()
        """Generiert ein Textfeld und ein Bild aus den Eingaben."""
        try:
            # Werte holen
            service_tag = self.service_tag_var.get()
            version = self.versionCombobox.get()
            charset = self.charsetCombobox.get()
            ident = self.identCombobox.get()
            bic = self.bic_var.get()
            name = self.name_var.get()
            iban = self.iban_var.get()
            betrag = self.betrag_var.get()
            zweck = ""
            referenz = ""
            verwendungszweck = self.verwendungszweck_var.get()
            information = ""

            text2convert = (f"{service_tag}\n"
                            f"{version}\n"
                            f"{charset}\n"
                            f"{ident}\n"
                            f"{bic}\n"
                            f"{name}\n"
                            f"{iban}\n"
                            f"EUR{betrag}\n"
                            f"{zweck}\n"
                            f"{referenz}\n"
                            f"{verwendungszweck}\n"
                            f"{information}\n"
            )

            # Textfeld aktualisieren
            self.outputText.delete(1.0, 'end')
            self.outputText.insert('end',text2convert)

            # Bild generieren
            self._create_picture(text2convert)
        except Exception as e:
            messagebox.showerror("Fehler", str(e))

    def _create_picture(self, text):
        """Erstellt ein Bild mit den Eingabewerten."""

        # qr code genereieren
        qrcode = segno.make_qr(text, error='l')
        qrcode.save("qrcode.png", scale=5)

        # qrcode.png("QRCode.png", scale=8)
        img = Image.open('qrcode.png')

        # Bild in Tkinter-Format konvertieren
        photo = ImageTk.PhotoImage(img)
        self.bild_label.config(image=photo)
        self.bild_label.image = photo  # Verweis halten, um GC zu verhindern


root = tkinter.Tk()
app = EPCgenerator(parent=root)
root.title("EPC-Generator")
root.geometry("600x720")
root.mainloop()