import customtkinter as ctk
from tkinter import messagebox

from app.config import COL_NUM, FIELDS_PADX, FIELDS_PADY


class LabeledComboBox(ctk.CTkFrame):
    def __init__(self, master, label_text, values, row=None, col=0, **kwargs):
        super().__init__(master, **kwargs)
        if row is not None:
            self.position = {
                "row": row,
                "column": col,
                "columnspan": int(COL_NUM / 2),
                "padx": FIELDS_PADX,
                "pady": FIELDS_PADY,
                "sticky": "ew",
            }
            self.grid(**self.position)

        self.values = values
        self.prev_value = values[0]

        self.label = ctk.CTkLabel(self, text=label_text)
        self.label.pack(side="left", padx=5)

        self.combobox = ctk.CTkComboBox(self, values=values)
        self.combobox.set(self.prev_value)
        self.combobox.pack(side="right", fill="x", expand=True)

    def get_value(self):
        return self.combobox.get()
