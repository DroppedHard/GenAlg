from typing import Dict
import customtkinter as ctk
from matplotlib import pyplot as plt
import numpy as np
from app.components.labeled_combo import LabeledComboBox
from app.components.labeled_entry import LabeledEntry
from app.config import COL_NUM
import benchmark_functions as bf
from PIL import Image

AVAILABLE_FUNCTIONS = [
    (bf.Hypersphere, (-10, 10)),
    (bf.Hyperellipsoid, (-60, 60)),
    (bf.Schwefel, (-400, 400)),
    (bf.Ackley, (-30, 30)),
    (bf.Michalewicz, (0, 3)),
    (bf.Rastrigin, (-6, 6)),
    (bf.Rosenbrock, (-3, 3)),
    (bf.DeJong3, (-5, 5)),
    (bf.DeJong5, (-70, 70)),
    # (bf.MartinGaddy, (-25, 25)), # TODO n_dimensioons tutaj nie przyjmuje
    (bf.Griewank, (-700, 700)),
    # (bf.Easom, (-100, 100)), # TODO ta funkcja tylko 2 wymiarowa
    (bf.GoldsteinAndPrice, (-2, 2)),
    (bf.PichenyGoldsteinAndPrice, (-2, 2)),
    (bf.StyblinskiTang, (-5, 5)),
    (bf.McCormick, (-5, 5)),
    (bf.Rana, (-500, 500)),
    (bf.EggHolder, (-500, 500)),
    (bf.Keane, (0, 10)),
    (bf.Schaffer2, (-100, 100)),
    (bf.Himmelblau, (-5, 5)),
    (bf.PitsAndHoles, (-25, 25)),
]


class SimulationConfig(ctk.CTkFrame):
    def __init__(self, master, row=1, col=0):
        super().__init__(master)
        self.simulation_entries: Dict[str, str] = {}
        self.current_function = None
        self.image_path = "assets/tmp/function_plot.png"

        self.available_functions = {fn[0].__name__: fn for fn in AVAILABLE_FUNCTIONS}

        self.config_values = {
            "Liczba argumentów": "2",
            "Liczba epok": "1000",
            "Zakres (początek)": "-10",
            "Zakres (koniec)": "10",
            "Prawdopodobieństwo inwersji": "0.2",
            "Prawdopodobieństwo mutacji": "0.1",
            "Prawdopodobieństwo krzyżowania (?)": "0.8",
        }
        self.frame_position = {
            "row": row,
            "column": col,
            "columnspan": COL_NUM,
            "padx": 10,
            "pady": 5,
            "sticky": "ew",
        }
        self.image = {
            "width": 300,
            "height": 300,
        }
        self.image_view = {
            "elev": 30,
            "azim": 45,
        }
        self.grid_columnconfigure(0, weight=1, uniform="equal")
        self.grid_columnconfigure(1, weight=1, uniform="equal")

        self.render()
        self.update_function_display()

    def render(self):
        self.grid(**self.frame_position)
        ctk.CTkLabel(
            self, text="⚙️ Konfiguracja symulacji", font=("Arial", 16, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=5)

        # Dropdown do wyboru funkcji celu
        self.function_combo = LabeledComboBox(
            self, "Funkcja celu", list(self.available_functions.keys())
        )
        self.function_combo.grid(row=1, column=0, pady=5, sticky="ew")
        self.function_combo.combobox.configure(command=self.update_function_display)

        self.image_label = ctk.CTkLabel(self, text="Podgląd funkcji", **self.image)
        self.image_label.grid(row=1, column=1, rowspan=8, pady=5, sticky="ew")

        for i, (label, default) in enumerate(self.config_values.items()):
            entry = LabeledEntry(self, label, default)
            entry.grid(row=2 + i, column=0, pady=2, padx=5, sticky="ew")

            self.simulation_entries[label] = entry

    def update_function_display(self, event=None):
        """Generuje i wyświetla wykres dla wybranej funkcji celu."""
        selected_function_name = self.function_combo.get_value()

        if selected_function_name in self.available_functions:
            (func, limit) = self.available_functions[selected_function_name]
            self.current_function = func(n_dimensions=2)

            try:
                fig = plt.figure(figsize=(4, 4))
                ax = fig.add_subplot(111, projection="3d")

                x = np.linspace(*limit, 100)
                y = np.linspace(*limit, 100)
                X, Y = np.meshgrid(x, y)

                Z = np.array(
                    [
                        [
                            self.current_function(np.array([xi, yi]))
                            for xi, yi in zip(x_row, y_row)
                        ]
                        for x_row, y_row in zip(X, Y)
                    ]
                )

                ax.plot_surface(X, Y, Z, cmap="viridis")
                if selected_function_name == "DeJong3":
                    ax.view_init(elev=30, azim=-135)
                else:
                    ax.view_init(**self.image_view)

                fig.savefig(self.image_path, bbox_inches="tight")
                plt.close(fig)

                pil_image = Image.open(self.image_path)
                function_image = ctk.CTkImage(
                    light_image=pil_image,
                    size=tuple(self.image.values()),
                )
                self.image_label.configure(image=function_image, text="")
                self.image_label.image = function_image
            except Exception as e:
                self.image_label.configure(text=f"Błąd generowania: {e}")

    def get_selected_function(self):
        """Zwraca wybraną funkcję celu"""
        function_name = self.function_combo.get_value()

        if function_name in self.available_functions:
            return self.available_functions[function_name][0]
        else:
            raise ValueError("Nieprawidłowa funkcja celu")

    def get_values(self):
        values = {}
        for key, entry in self.simulation_entries.items():
            if key in ["Liczba argumentów", "Liczba epok"]:
                values[key] = int(entry.get_value())
            else:
                values[key] = float(entry.get_value())
        values["Funkcja celu"] = self.get_selected_function()(
            n_dimensions=values["Liczba argumentów"]
        )
        return values
