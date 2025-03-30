import customtkinter as ctk
from app.components.labeled_entry import LabeledEntry
from app.config import COL_NUM


class SimulationConfig(ctk.CTkFrame):
    def __init__(self, master, row=1, col=0):
        super().__init__(master)
        self.simulation_entries = {}

        self.config_values = {
            "Funkcja celu": "x**2",
            "Liczba epok": "1000",
            "Zakres (początek)": "-10",
            "Zakres (koniec)": "10",
            "Prawdopodobieństwo inwersji": "0.2",
            "Prawdopodobieństwo mutacji": "0.1",
            # "Prawdopodobieństwo krzyżowania (?)": "0.8",
        }
        self.frame_position = {
            "row": row,
            "column": col,
            "columnspan": COL_NUM,
            "padx": 10,
            "pady": 5,
            "sticky": "ew",
        }

        self.grid_columnconfigure(0, weight=1, uniform="equal")
        self.grid_columnconfigure(1, weight=1, uniform="equal")

        self.render()

    def render(self):
        self.grid(**self.frame_position)
        ctk.CTkLabel(
            self, text="⚙️ Konfiguracja symulacji", font=("Arial", 16, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=5)

        row = 1
        col = 0

        for i, (label, default) in enumerate(self.config_values.items()):
            entry = LabeledEntry(self, label, default)
            entry.grid(row=row, column=col, pady=2, padx=5, sticky="ew")

            if (i + 1) % 2 == 0:
                col = 0
                row += 1
            else:
                col += 1

            self.simulation_entries[label] = entry

    def get_values(self):
        return {
            key: entry.get_value() for key, entry in self.simulation_entries.items()
        }
