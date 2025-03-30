import customtkinter as ctk
from app.algorithms.selections import AVAILABLE_SELECTIONS
from app.components.labeled_combo import LabeledComboBox
from app.components.labeled_entry import LabeledEntry
from app.config import FIELDS_PADX, FIELDS_PADY


class SelectionConfig(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.simulation_entries = {}

        self.selection_methods = {
            sel.getName(): (sel.getParamteres(), sel.validateParameters)
            for sel in AVAILABLE_SELECTIONS
        }

        self.param_entries = {}

        self.combo_position = {
            "row": 3,
            "column": 0,
            "columnspan": 3,
            "padx": FIELDS_PADX,
            "pady": FIELDS_PADY,
            "sticky": "ew",
        }
        self.frame_position = {
            "row": 4,
            "column": 0,
            "columnspan": 3,
            "padx": FIELDS_PADX,
            "pady": FIELDS_PADY,
            "sticky": "ew",
        }

        self.render()
        self.update_selection_params()

    def render(self):
        self.combo = LabeledComboBox(
            self, "Metoda selekcji", list(self.selection_methods.keys())
        )
        self.combo.grid(**self.combo_position)
        self.combo.combobox.configure(command=self.update_selection_params)

        self.frame = ctk.CTkFrame(self)
        self.frame.grid(**self.frame_position)

    def update_selection_params(self, event=None):
        """Aktualizuje dynamiczne pola w zależności od wybranej metody selekcji"""
        selected_method = self.combo.get_value()

        for widget in self.frame.winfo_children():
            widget.destroy()

        self.param_entries.clear()

        if selected_method in self.selection_methods:
            params, _ = self.selection_methods[selected_method]

            if not params:
                no_params_label = ctk.CTkLabel(self.frame, text="Brak parametrów")
                no_params_label.pack(pady=5)
                return

            for label, default in params:
                input_field = LabeledEntry(self.frame, label, default)
                input_field.pack(pady=5, fill="x")
                self.param_entries[label] = input_field

    def get_selected_method(self):
        """Zwraca wybraną metodę selekcji"""
        return self.combo.get_value()

    def get_params(self):
        """Zwraca wartości parametrów jako słownik"""
        return {name: entry.get_value() for name, entry in self.param_entries.items()}
