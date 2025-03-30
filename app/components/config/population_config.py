import customtkinter as ctk
from app.components.labeled_entry import LabeledEntry
from app.config import COL_NUM


class PopulationConfig(ctk.CTkFrame):
    def __init__(self, master, row=2, col=0):
        super().__init__(master)
        self.population_entries = {}

        self.config_values = {
            "Liczność populacji": "50",
            "Dokładność reprezentacji chromosomu": "4",
            "Długość chromosomu": "10",
            "Liczba najlepszych osobników": "5",
        }

        self.frame_position = {
            "row": row,
            "column": col,
            "columnspan": int(COL_NUM / 2),
            "padx": 10,
            "pady": 5,
            "sticky": "ew",
        }

        self.render()

    def render(self):
        self.grid(**self.frame_position)
        ctk.CTkLabel(
            self, text="🧬 Konfiguracja populacji", font=("Arial", 16, "bold")
        ).pack(pady=5)

        for label, default in self.config_values.items():
            entry = LabeledEntry(self, label, default)
            entry.pack(pady=2, fill="x")
            self.population_entries[label] = entry

    def get_values(self):
        return {
            key: entry.get_value() for key, entry in self.population_entries.items()
        }
