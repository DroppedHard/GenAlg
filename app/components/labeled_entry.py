import customtkinter as ctk


class LabeledEntry(ctk.CTkFrame):
    def __init__(self, master, label_text, default_value="", **kwargs):
        super().__init__(master, **kwargs)

        self.label = ctk.CTkLabel(self, text=label_text)
        self.label.pack(side="left", padx=5)

        self.entry = ctk.CTkEntry(self)
        self.entry.insert(0, default_value)
        self.entry.pack(side="right", fill="x", expand=True)

    def get_value(self):
        return self.entry.get()
