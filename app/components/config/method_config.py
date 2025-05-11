from typing import Dict, ClassVar
import customtkinter as ctk
from app.algorithms.crossovers import AVAILABLE_CROSSOVERS, REAL_REPRESENTATION_CROSSOVERS
from app.algorithms.selections import AVAILABLE_SELECTIONS
from app.components.labeled_entry import LabeledEntry
from app.components.labeled_combo import LabeledComboBox
from app.config import COL_NUM, FIELDS_PADX, FIELDS_PADY


class MethodConfig(ctk.CTkFrame):
    def __init__(self, master, title, methods_dict: Dict, row, col=0, **kwargs):
        """
        Klasa bazowa dla konfiguracji metod selekcji, mutacji i krzyżowania.

        :param master: Rodzic (np. HomePage)
        :param title: Tytuł sekcji (np. "Metoda selekcji")
        :param methods_dict: Słownik z metodami {nazwa: (parametry, funkcja_walidacji)}
        :param row, col - row and column where to put in grid
        """
        super().__init__(master, **kwargs)
        self.methods_dict = methods_dict
        self.param_entries = {}
        self.hidden_entries = {}

        self.position = {
            "row": row,
            "column": col,
            "columnspan": int(COL_NUM / 2),
            "padx": FIELDS_PADX,
            "pady": FIELDS_PADY,
            "sticky": "ew",
        }

        self.render(title)

    def render(self, title):
        """Tworzy interfejs wyboru metody i dynamicznych parametrów."""
        self.grid(**self.position)
        self.combo = LabeledComboBox(self, title, list(self.methods_dict.keys()))
        self.combo.pack(pady=5, fill="x")
        self.combo.combobox.configure(command=self.update_params)

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=5, fill="x")

        self.update_params()

    def add_hidden_entry(self, label, value):
        print("Added entry")
        print(label, value)
        self.hidden_entries[label] = value

    def update_params(self, event=None):
        """Aktualizuje dynamiczne pola na podstawie wybranej metody."""
        selected_method = self.combo.get_value()

        for widget in self.frame.winfo_children():
            widget.destroy()
        self.param_entries.clear()

        if selected_method in self.methods_dict:
            params, _ = self.methods_dict[selected_method]

            if not params:
                label = ctk.CTkLabel(
                    self.frame,
                    text="Brak parametrów",
                    font=("Arial", 12, "italic"),
                )
                label.pack(pady=5)
                return

            for label, default in params:
                if label == "Typ optymalizacji":
                    min_label = ctk.CTkLabel(self.frame, text="min", font=("Arial", 12))
                    min_label.pack(side="left", padx=5)

                    toggle = ctk.CTkSwitch(
                        self.frame, text="max", onvalue="max", offvalue="min"
                    )
                    toggle.pack(side="left", padx=5)

                    max_label = ctk.CTkLabel(self.frame, text=label, font=("Arial", 12))
                    max_label.pack(side="left", padx=5)

                    self.param_entries[label] = toggle
                else:
                    entry = LabeledEntry(self.frame, label, default)
                    entry.pack(pady=5, fill="x")
                    self.param_entries[label] = entry

    def get_selected_method(self):
        """Zwraca wybraną metodę."""
        return self.combo.get_value()

    def get_params(self):
        """Zwraca słownik parametrów wybranej metody."""
        params = {}
        for label, value in self.hidden_entries.items():
            params[label] = value.get()

        print("Hidden entries:", params)

        for name, entry in self.param_entries.items():
            if isinstance(entry, ctk.CTkSwitch):
                params[name] = entry.get()
            else:
                if "." in entry.get_value():
                    params[name] = float(entry.get_value())
                else:
                    params[name] = int(entry.get_value())
        print(params)
        return params

    def get_method_instance(self):
        """
        Zwraca instancję wybranej metody (selekcji lub krzyżowania) z parametrami.
        """
        selected_method = self.get_selected_method()
        params = self.get_params()

        if selected_method in self.methods_dict:
            _, validate_func = self.methods_dict[selected_method]
            if not validate_func(*params.values()):
                raise ValueError(
                    f"Parametry dla metody {selected_method} są niepoprawne:{params}"
                )
            method_class = next(
                (
                    cls
                    for cls in AVAILABLE_SELECTIONS + AVAILABLE_CROSSOVERS + REAL_REPRESENTATION_CROSSOVERS
                    if cls.getName() == selected_method
                ),
                None,
            )
            if method_class:
                print(f"Tworzenie instancji metody: {selected_method} z parametrami: {params}")
                return method_class(*params.values())
            else:
                raise ValueError(f"Nieznana klasa dla metody: {selected_method}")
        else:
            raise ValueError(f"Nieznana metoda: {selected_method}")
