import customtkinter as ctk
from app.components.labeled_entry import LabeledEntry
from app.components.labeled_combo import LabeledComboBox
from app.components.button import CustomButton

TITLE_FONT_SIZE = 20
FIELDS_PADX = 5
FIELDS_PADY = 0

class HomePage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.layout()

        # Definicje metod i ich parametrów - TODO tutaj będą buildery klas?
        self.selection_methods = {
            "Procent najlepszych": [("Procent najlepszych (%)", "50")],
            "Turniejowa": [("Rozmiar turnieju", "3")],
            "Rankingowa": [("Współczynnik selekcji", "1.5")],
        }

        self.crossover_methods = {
            "Jednopunktowe": [("Punkt podziału (0-1)", "0.5")],
            "Jednorodne": [("Prawdopodobieństwo wymiany", "0.7")],
        }

        self.mutation_methods = {
            "Brzegowa": [("Prawdopodobieństwo mutacji", "0.1")],
            "Jednopunktowa": [("Pozycja mutacji (0-1)", "0.5")],
        }

        self.render()

    def layout(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        for i in range(8):  # Konfiguracja wierszy
            self.grid_rowconfigure(i, weight=1)

    def render(self):
        # Tytuł
        self.title_label = ctk.CTkLabel(
            self, text="Ewolucyjny Algorytm Genetyczny", font=("Arial", TITLE_FONT_SIZE, "bold")
        )
        self.title_label.grid(row=0, column=0, columnspan=3, pady=10, sticky="nsew")

        # Selekcja
        self.selection_select = LabeledComboBox(
            self, "Metoda selekcji", list(self.selection_methods.keys())
        )
        self.selection_select.grid(
            row=1, column=0, columnspan=3, padx=FIELDS_PADX, pady=FIELDS_PADY, sticky="ew"
        )
        self.selection_select.combobox.configure(command=self.update_selection_params)

        self.selection_frame = ctk.CTkFrame(self)
        self.selection_frame.grid(
            row=2, column=0, columnspan=3, padx=FIELDS_PADX, pady=FIELDS_PADY, sticky="ew"
        )

        # Krzyżowanie
        self.crossover_select = LabeledComboBox(
            self, "Metoda krzyżowania", list(self.crossover_methods.keys())
        )
        self.crossover_select.grid(
            row=3, column=0, columnspan=3, padx=FIELDS_PADX, pady=FIELDS_PADY, sticky="ew"
        )
        self.crossover_select.combobox.configure(command=self.update_crossover_params)

        self.crossover_frame = ctk.CTkFrame(self)
        self.crossover_frame.grid(
            row=4, column=0, columnspan=3, padx=FIELDS_PADX, pady=FIELDS_PADY, sticky="ew"
        )

        # Mutacja
        self.mutation_select = LabeledComboBox(
            self, "Metoda mutacji", list(self.mutation_methods.keys())
        )
        self.mutation_select.grid(
            row=5, column=0, columnspan=3, padx=FIELDS_PADX, pady=FIELDS_PADY, sticky="ew"
        )
        self.mutation_select.combobox.configure(command=self.update_mutation_params)

        self.mutation_frame = ctk.CTkFrame(self)
        self.mutation_frame.grid(
            row=6, column=0, columnspan=3, padx=FIELDS_PADX, pady=FIELDS_PADY, sticky="ew"
        )

        # Przycisk startowy
        self.start_button = CustomButton(self, "Start", command=self.start_simulation)
        self.start_button.grid(row=7, column=1, pady=20, sticky="ew")

        self.update_selection_params()
        self.update_crossover_params()
        self.update_mutation_params()

    def update_selection_params(self, event=None):
        """Aktualizuje parametry dla metody selekcji"""
        selected_method = self.selection_select.get_value()
        print(f"Wybrana metoda selekcji: {selected_method}")
        self.update_params(self.selection_frame, self.selection_methods, selected_method)

    def update_crossover_params(self, event=None):
        """Aktualizuje parametry dla metody krzyżowania"""
        selected_method = self.crossover_select.get_value()
        print(f"Wybrana metoda krzyżowania: {selected_method}")
        self.update_params(self.crossover_frame, self.crossover_methods, selected_method)

    def update_mutation_params(self, event=None):
        """Aktualizuje parametry dla metody mutacji"""
        selected_method = self.mutation_select.get_value()
        print(f"Wybrana metoda mutacji: {selected_method}")
        self.update_params(self.mutation_frame, self.mutation_methods, selected_method)

    def update_params(self, frame, methods_dict, selected_method):
        """Usuwa stare parametry i dodaje nowe w zależności od wyboru"""
        for widget in frame.winfo_children():
            widget.destroy()

        if selected_method in methods_dict:
            for label, default in methods_dict[selected_method]:
                input_field = LabeledEntry(frame, label, default)
                input_field.pack(pady=5, fill="x")

    def start_simulation(self):
        print("Symulacja uruchomiona!")
