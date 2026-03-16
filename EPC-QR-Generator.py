import tkinter
from tkinter import ttk, messagebox, simpledialog
import segno  # qr code generation
import tk
from PIL import Image, ImageTk

class EPCgenerator(tkinter.Frame):

    # constructor
    def __init__(self, parent=None):
        ttk.Frame.__init__(self, parent)
        # create menu
        self.menuBar = tkinter.Menu(parent)
        parent.config(menu=self.menuBar)
        self.fillMenuBar()
        self.pack()

        # options for basic epc settings
        self.ver_options = ["001", "002"]
        self.charset_options = ["1", "2", "3", "4", "5", "6", "7", "8"]
        self.ident_options = ["SCT", "INST"]

        # -- input variable for entry elements
        # service tag has to be "BCD", other values are yet not allowed
        self.service_tag_var = tkinter.StringVar(value="BCD")
        # define default value from ver_options
        self.version_var = tkinter.StringVar(value=self.ver_options[0])
        # define default value from charset_options
        self.charset_var = tkinter.StringVar(value=self.charset_options[0])
        # define default value from ident_options
        self.ident_var = tkinter.StringVar(value=self.ident_options[0])
        self.name_var = tkinter.StringVar(value="")
        self.iban_var = tkinter.StringVar(value="")
        self.bic_var = tkinter.StringVar(value="")
        self.verwendungszweck_var = tkinter.StringVar(value="")
        self.betrag_var = tkinter.StringVar(value="0.00")

        self.text_var = tkinter.StringVar(value="")
        self.amount_var = tkinter.StringVar(value="0.00")
        self.createWidgets()

    def fillMenuBar(self):
        # define menu -> file
        self.menuFile = tkinter.Menu(self.menuBar, tearoff=False)
        self.menuFile.add_command(label="Info", command=self.show_info)
        self.menuFile.add_command(label="IBAN-Rechner", command=self.iban_calculator_dialog)
        self.menuFile.add_separator()
        self.menuFile.add_command(label=" Beenden", command=self.quit)
        self.menuBar.add_cascade(label="Datei", menu=self.menuFile)

        # define menu -> templates
        self.menuTemplates = tkinter.Menu(self.menuBar, tearoff=False)
        self.menuBar.add_cascade(label="Vorlagen", menu=self.menuTemplates)

        # define sub menu for templates -> entries
        self.menuTemplatesEntries = tkinter.Menu(self.menuBar, tearoff=False)
        self.menuTemplatesEntries.add_command(label="Entry1", command=self.handler)
        self.menuTemplatesEntries.add_command(label="Entry2", command=self.handler)
        self.menuTemplates.add_cascade(label="Letzte Vorlagen...", menu=self.menuTemplatesEntries)

        # define menu -> settings
        self.menuSettings = tkinter.Menu(self.menuBar, tearoff=False)
        self.menuBar.add_cascade(label="Settings", menu=self.menuSettings)

        # define sub menu for setting -> language
        self.menuSettingsLanguage = tkinter.Menu(self.menuBar, tearoff=False)
        self.menuSettingsLanguage.add_command(label="Deutsch", command=self.handler)
        self.menuSettingsLanguage.add_command(label="English", command=self.handler)
        self.menuSettings.add_cascade(label="Language", menu=self.menuSettingsLanguage)

    def show_info(self):
        """Function for showing an info dialog."""
        message = (f"EPC-Generator 0.1\n"
                   f"Build on 2026-03-08 (Weltfrauentag!)\n"
                   f"Copyright © 2026 Marcel Berkholz"
                   )
        infobox = tkinter.messagebox.showinfo("Info", message)

    def iban_calculator_dialog(self):
        """Function for showing the IBAN-calulator dialog."""
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
        self.accountLabel = tkinter.Label(groupIBANcalculator, text="KTO:")
        self.accountLabel.grid(row=1, column=0)

        groupCalcResult = tkinter.LabelFrame(self.application_window, text="IBAN")
        self.resultText = tkinter.Text(master=groupCalcResult, height=10)
        self.resultText.grid(row=0, column=0)
        groupCalcResult.pack(expand=True,fill="x")

    def _modulo97(self, number: object) -> int:
        """Function for calculating the modulo 97."""
        return number % 97

    def calculate_iban_close(self):
        """Wrapper function for calculating the IBAN and
        closing the dialog (IBAN-calculator)."""
        # only calculate if both (account number and bank code number) is given
        if self.accountEntry.get() != "" and self.bankcodeEntry.get() != "":
            self.calculate_iban()
            self.application_window.destroy()
        # otherwise close dialog
        else:
            self.application_window.destroy()

    def calculate_iban(self):
        kto_as_string = str(self.ktoEntry.get())
        blz_as_string = str(self.blzEntry.get())
        """Function for calculating the IBAN."""
        account_number_as_string = str(self.accountEntry.get())
        bankcode_as_string = str(self.bankcodeEntry.get())
        langCode = str(self.langEntry.get())

        if kto_as_string != "" and blz_as_string != "":
            kto_blz_string = kto_as_string + blz_as_string
            modulo_result = self._modulo97(int(kto_blz_string))
            iban_tmp = f"{langCode}{modulo_result}{blz_as_string}{kto_as_string}"
        # only calculate if both (account number and bank code number) is given
        if account_number_as_string != "" and bankcode_as_string != "":
            account_bankcode_string = account_number_as_string + bankcode_as_string
            modulo_result = self._modulo97(int(account_bankcode_string))
            iban_tmp = (f"{langCode}"
                        f"{modulo_result}"
                        f"{bankcode_as_string}"
                        f"{account_number_as_string}")
            self.iban_var.set(iban_tmp)
            self.resultText.delete(1.0, 'end')
            self.resultText.insert('end', iban_tmp)
        else:
            tkinter.messagebox.showwarning("Warning", "KTO und BLZ fehlen!")

    def handler(self):
        print("handler called")
        """Dummy function."""

    def createWidgets(self):
        """Function for creating widgets."""
        # frame for default components
        frameDefault = tkinter.Frame(self)

        # labelFrame for default components
        groupDefaultData = tkinter.LabelFrame(frameDefault, text="Defaults")

        # label for version
        self.versionLabel = tkinter.Label(groupDefaultData, text="Version:")
        self.versionLabel.grid(row=0, column=0)

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
        # Text
        textLabel = ttk.Label(groupCustomData, text="Verwendungszweck:")
        textLabel.grid(row=3, column=0)
        textEntry = ttk.Entry(groupCustomData, textvariable=self.text_var)
        textEntry.grid(row=3, column=1)

        # Betrag
        ttk.Label(groupCustomData, text="Betrag (€):").grid(row=4, column=0)
        ttk.Entry(groupCustomData, textvariable=self.betrag_var).grid(row=4, column=1)
        # amount
        amountLabel = ttk.Label(groupCustomData, text="Betrag (€):")
        amountLabel.grid(row=4, column=0)
        amountEntry = ttk.Entry(groupCustomData, textvariable=self.amount_var)
        amountEntry.grid(row=4, column=1)

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
        # text field for printing the text, which is used for qr code
        self.outputText = tkinter.Text(master=groupOutputText, height=10)
        self.outputText.grid(row=0, column=0)
        groupOutputText.pack(expand=True, fill="x")

        groupOutputPicture = tkinter.LabelFrame(self, text="Output-Picture")
        # label for the qr code
        self.picture_label = ttk.Label(groupOutputPicture)
        self.picture_label.grid(row=0, column=1)
        groupOutputPicture.pack(fill="x", expand=True)

    def print_vars(self):
        """Print all variables for the barcode."""
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
        amount = self.amount_var.get()
        print(amount)
        text = self.text_var.get()
        print(text)

    def refresh_output(self):
        """Refresh the output text and generate and show the qr code picture."""
        self.print_vars()
        try:
            # get all values from input mask
            service_tag = self.service_tag_var.get()
            version = self.versionCombobox.get()
            charset = self.charsetCombobox.get()
            ident = self.identCombobox.get()
            bic = self.bic_var.get()
            name = self.name_var.get()
            iban = self.iban_var.get()
            amount = self.amount_var.get()
            purpose = ""
            reference = ""
            text = self.text_var.get()
            information = ""

            text2convert = (f"{service_tag}\n"
                            f"{version}\n"
                            f"{charset}\n"
                            f"{ident}\n"
                            f"{bic}\n"
                            f"{name}\n"
                            f"{iban}\n"
                            f"EUR{amount}\n"
                            f"{purpose}\n"
                            f"{reference}\n"
                            f"{text}\n"
                            f"{information}\n")

            # refresh text field with qr code information
            self.outputText.delete(1.0, 'end')
            self.outputText.insert('end',text2convert)

            # generate and show qr code picture
            self._create_picture(text2convert)
        except Exception as e:
            messagebox.showerror("Fehler", str(e))

    def _create_picture(self, text):
        """Generate and display the picture."""

        # generate the qr code
        qrcode = segno.make_qr(text, error='l')
        qrcode.save("qrcode.png", scale=5)

        # qrcode.png("QRCode.png", scale=8)
        img = Image.open('qrcode.png')

        # show qr code picture
        photo = ImageTk.PhotoImage(img)
        self.picture_label.config(image=photo)
        self.picture_label.image = photo


root = tkinter.Tk()
app = EPCgenerator(parent=root)
root.title("EPC-Generator")
root.geometry("600x720")
root.mainloop()