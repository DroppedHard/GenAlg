import customtkinter as ctk
from app.components.labeled_entry import LabeledEntry
from app.components.labeled_combo import LabeledComboBox
from app.components.button import CustomButton
from app.algorithms.selections import AVAILABLE_SELECTIONS
from app.simulation import Simulation

TITLE_FONT_SIZE = 20
FIELDS_PADX = 5
FIELDS_PADY = 0


class HomePage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.layout()
        self.param_entries = {}

        # Definicje metod i ich parametrów
        self.selection_methods = {
            sel.getName(): (sel.getParamteres(), sel.validateParameters)
            for sel in AVAILABLE_SELECTIONS
        }

        # TODO te 2 analogicznie jak wyżej po poprawkach
        self.crossover_methods = {
            "Jednopunktowe": ([], lambda: True),
            "Jednorodne": ([("Prawdopodobieństwo wymiany", "0.7")], lambda x: True),
        }

        self.mutation_methods = {
            "Brzegowa": ([("Prawdopodobieństwo mutacji", "0.1")], lambda x: True),
            "Jednopunktowa": ([("Pozycja mutacji (0-1)", "0.5")], lambda x: True),
        }

        self.render()

    def layout(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        for i in range(8):
            self.grid_rowconfigure(i, weight=1)

    def render(self):
        # Tytuł
        self.title_label = ctk.CTkLabel(
            self,
            text="Ewolucyjny Algorytm Genetyczny",
            font=("Arial", TITLE_FONT_SIZE, "bold"),
        )
        self.title_label.grid(
            row=0, column=0, columnspan=3, pady=FIELDS_PADY, sticky="nsew"
        )

        # Selekcja
        self.selection_select = LabeledComboBox(
            self, "Metoda selekcji", list(self.selection_methods.keys())
        )
        self.selection_select.grid(
            row=1,
            column=0,
            columnspan=3,
            padx=FIELDS_PADX,
            pady=FIELDS_PADY,
            sticky="ew",
        )
        self.selection_select.combobox.configure(command=self.update_selection_params)

        self.selection_frame = ctk.CTkFrame(self)
        self.selection_frame.grid(
            row=2,
            column=0,
            columnspan=3,
            padx=FIELDS_PADX,
            pady=FIELDS_PADY,
            sticky="ew",
        )

        # Krzyżowanie
        self.crossover_select = LabeledComboBox(
            self, "Metoda krzyżowania", list(self.crossover_methods.keys())
        )
        self.crossover_select.grid(
            row=3,
            column=0,
            columnspan=3,
            padx=FIELDS_PADX,
            pady=FIELDS_PADY,
            sticky="ew",
        )
        self.crossover_select.combobox.configure(command=self.update_crossover_params)

        self.crossover_frame = ctk.CTkFrame(self)
        self.crossover_frame.grid(
            row=4,
            column=0,
            columnspan=3,
            padx=FIELDS_PADX,
            pady=FIELDS_PADY,
            sticky="ew",
        )

        # Mutacja
        self.mutation_select = LabeledComboBox(
            self, "Metoda mutacji", list(self.mutation_methods.keys())
        )
        self.mutation_select.grid(
            row=5,
            column=0,
            columnspan=3,
            padx=FIELDS_PADX,
            pady=FIELDS_PADY,
            sticky="ew",
        )
        self.mutation_select.combobox.configure(command=self.update_mutation_params)

        self.mutation_frame = ctk.CTkFrame(self)
        self.mutation_frame.grid(
            row=6,
            column=0,
            columnspan=3,
            padx=FIELDS_PADX,
            pady=FIELDS_PADY,
            sticky="ew",
        )

        # Przycisk startowy
        self.start_button = CustomButton(self, "Start", command=self.start_simulation)
        self.start_button.grid(row=7, column=1, pady=20, sticky="ew")

        self.update_selection_params()
        self.update_crossover_params()
        self.update_mutation_params()

    def update_selection_params(self, event=None):
        selected_method = self.selection_select.get_value()
        self.update_params(
            self.selection_frame, self.selection_methods, selected_method
        )

    def update_crossover_params(self, event=None):
        selected_method = self.crossover_select.get_value()
        self.update_params(
            self.crossover_frame, self.crossover_methods, selected_method
        )

    def update_mutation_params(self, event=None):
        selected_method = self.mutation_select.get_value()
        self.update_params(self.mutation_frame, self.mutation_methods, selected_method)

    def update_params(self, frame, methods_dict, selected_method):
        """Usuwa stare parametry i dodaje nowe w zależności od wyboru"""
        for widget in frame.winfo_children():
            widget.destroy()

        param_list, _ = methods_dict.get(selected_method, ([], None))
        self.param_entries[frame] = {}
        if not param_list:
            label = ctk.CTkLabel(
                frame, text="Brak parametrów", font=("Arial", 12, "italic")
            )
            label.pack(pady=5)
            return

        if selected_method in methods_dict:
            params, _ = methods_dict[selected_method]
            for label, default in params:
                input_field = LabeledEntry(frame, label, default)
                input_field.pack(pady=5, fill="x")
                self.param_entries[frame][label] = input_field

    def get_values_dict(self):
        """Zwraca słownik wartości wpisanych przez użytkownika"""
        values = {}
        for frame, entries in self.param_entries.items():
            for param_name, entry_widget in entries.items():
                values[param_name] = entry_widget.get_value()
        return values

    def verifyParameters(self) -> bool:
        """Sprawdza wszystkie parametry"""
        for frame, entries in self.param_entries.items():
            selected_method = None
            validation_function = None

            if frame == self.selection_frame:
                selected_method = self.selection_select.get_value()
                validation_function = self.selection_methods[selected_method][1]
            elif frame == self.crossover_frame:
                selected_method = self.crossover_select.get_value()
                validation_function = self.crossover_methods[selected_method][1]
            elif frame == self.mutation_frame:
                selected_method = self.mutation_select.get_value()
                validation_function = self.mutation_methods[selected_method][1]

            if selected_method and validation_function:
                param_values = {
                    name: entry.get_value() for name, entry in entries.items()
                }

                try:
                    param_values = [float(value) for value in param_values.values()]
                    print(*param_values)

                    if not validation_function(*param_values):
                        print(
                            f"Błąd walidacji dla metody {selected_method}: {param_values}"
                        )
                        for entry in entries.values():
                            entry.entry.configure(fg_color="red")
                        return False
                except TypeError as e:
                    print(
                        f"Błąd wywołania funkcji walidującej dla {selected_method}: {e}"
                    )
                    return False
        return True

    def start_simulation(self):
        """Sprawdza wszystkie parametry i uruchamia symulację, jeśli są poprawne."""

        method_instances = {}

        for method_type, select_widget, method_dict, frame in [
            (
                "selekcja",
                self.selection_select,
                self.selection_methods,
                self.selection_frame,
            ),
            (
                "krzyżowanie",
                self.crossover_select,
                self.crossover_methods,
                self.crossover_frame,
            ),
            (
                "mutacja",
                self.mutation_select,
                self.mutation_methods,
                self.mutation_frame,
            ),
        ]:
            selected_method = select_widget.get_value()

            if selected_method in method_dict:
                param_list, validation_function = method_dict[selected_method]

                param_values = [
                    entry_widget.get_value()
                    for label, entry_widget in self.param_entries.get(frame, {}).items()
                ]

                param_values = [float(v) if "." in v else int(v) for v in param_values]

                if not validation_function(*param_values):
                    print(f"Błąd walidacji dla metody {method_type}: {selected_method}")
                    return

                method_class = next(
                    (
                        cls
                        for cls in AVAILABLE_SELECTIONS
                        if cls.getName() == selected_method
                    ),
                    None,
                )

                if method_class:
                    method_instances[method_type] = method_class(*param_values)
                    print(
                        f"✅ Utworzono instancję {method_type}: {method_instances[method_type]}"
                    )

        if len(method_instances) == 3:
            simulation = Simulation(
                method_instances["selekcja"],
                method_instances["krzyżowanie"],
                method_instances["mutacja"],
            )
            simulation.run()
