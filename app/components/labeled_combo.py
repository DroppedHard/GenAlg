import customtkinter as ctk
from tkinter import messagebox


class LabeledComboBox(ctk.CTkFrame):
    def __init__(self, master, label_text, values, **kwargs):
        super().__init__(master, **kwargs)

        self.values = values
        self.prev_value = values[0]

        self.label = ctk.CTkLabel(self, text=label_text)
        self.label.pack(side="left", padx=5)

        self.combobox = ctk.CTkComboBox(self, values=values)
        self.combobox.set(self.prev_value)
        self.combobox.pack(side="right", fill="x", expand=True)

    def get_value(self):
        return self.combobox.get()
