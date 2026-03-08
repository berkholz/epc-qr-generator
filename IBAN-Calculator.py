import tkinter
from tkinter import ttk, messagebox, simpledialog
import segno  # qr code generation
import tk
from PIL import Image, ImageTk

class IBANCalculator(tkinter.Frame):

    def __init__(self, parent=None):
        ttk.Frame.__init__(self, parent)
        self.pack()
        self.iban_calculator_dialog()

    def iban_calculator_dialog(self):
        self.kto_number = tkinter.StringVar()
        self.blz = tkinter.StringVar()
        self.lang = tkinter.StringVar(value="DE")

        groupIBANcalculator = tkinter.LabelFrame(self, text="Kontodaten")

        self.langLabel = tkinter.Label(groupIBANcalculator, text="Länderkennung:")
        self.langLabel.grid(row=0, column=0)
        self.langEntry = tkinter.Entry(groupIBANcalculator, textvariable="DE", name="lang")
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

        groupCalcResult = tkinter.LabelFrame(self, text="IBAN")
        self.resultText = tkinter.Text(master=groupCalcResult, height=2)
        self.resultText.grid(row=0, column=0)
        groupCalcResult.pack(expand=True,fill="x")

    def _modulo97(self, number: object) -> int:
        return number % 97

    def calculate_iban_close(self):
        if self.ktoEntry.get() != "" and self.blzEntry.get() != "":
            self.calculate_iban()
            self.quit()
        else:
            self.quit()

    def calculate_iban(self):
        kto_as_string = str(self.ktoEntry.get())
        blz_as_string = str(self.blzEntry.get())
        langCode = str(self.langEntry.get())

        if kto_as_string != "" and blz_as_string != "":
            kto_blz_string = kto_as_string + blz_as_string
            modulo_result = self._modulo97(int(kto_blz_string))

            iban_tmp = f"{langCode}{modulo_result}{blz_as_string}{kto_as_string}"
            self.resultText.delete(1.0, 'end')
            self.resultText.insert('end', iban_tmp)
        else:
            tkinter.messagebox.showwarning("Warning", "KTO und BLZ fehlen!")


root = tkinter.Tk()
app = IBANCalculator(parent=root)
root.title("IBAN-Generator")
root.geometry("600x200")
root.mainloop()