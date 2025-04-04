import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from app.algorithms.crossovers import AVAILABLE_CROSSOVERS
from app.algorithms.mutation import AVAILABLE_MUTATIONS, Inversion
from app.components.config.method_config import MethodConfig
from app.components.config.population_config import PopulationConfig
from app.components.config.simulation_config import SimulationConfig
from app.components.labeled_combo import LabeledComboBox
from app.components.button import CustomButton
from app.algorithms.selections import AVAILABLE_SELECTIONS
from app.config import (
    COL_NUM,
    FIELDS_PADY,
    ROW_NUM,
    TITLE_FONT_SIZE,
    TITLE_TEXT,
)
from app.representation.population import Population
from app.simulation import Simulation


class ResultsPage(ctk.CTkFrame):
    def __init__(self, master, statistics, **kwargs):
        super().__init__(master, **kwargs)

        self.layout()
        self.param_entries = {}
        self.statistics, self.duration = statistics

        self.render()

    def layout(self):
        for i in range(COL_NUM):
            self.grid_columnconfigure(i, weight=1)

        for i in range(ROW_NUM):
            self.grid_rowconfigure(i, weight=1)

    def display_plot(self):
        fig, axs = plt.subplots(3, 1, sharex=True, figsize=(4, 6))
        epochs = [ind[0] for ind in self.statistics]
        best_values = [ind[2] for ind in self.statistics]
        axs[0].plot(epochs, best_values, label="Best Individual")
        axs[0].set_title("Najlepsza wartość funkcji a epoka")
        axs[0].set_xlabel("Epoki")
        axs[0].set_ylabel("Najlepsza wartość")

        avg_values = [ind[3] for ind in self.statistics]
        axs[1].plot(epochs, avg_values, label="Average Value", linestyle="--")
        axs[1].set_title("Średnia wartość funkcji a epoka")
        axs[1].set_xlabel("Epoki")
        axs[1].set_ylabel("Średnia wartość")

        std_values = [ind[4] for ind in self.statistics]
        axs[2].plot(epochs, std_values, label="Standard Deviation", linestyle=":")
        axs[2].set_title("Odchylenie standardowe a epoka")
        axs[2].set_xlabel("Epoki")
        axs[2].set_ylabel("Odchylenie standardowe")

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, self)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=2, column=0, columnspan=COL_NUM, rowspan=2, sticky="nsew", padx=20, pady=20)  # Use rowspan to fill space
        canvas.draw()

    def render(self):
        ctk.CTkLabel(
            self, text="📊 Wyniki symulacji", font=("Arial", 16, "bold")
        ).grid(row=0, column=0, columnspan=COL_NUM, pady=5)

        args = [round(arg, 4) for arg in self.statistics[0][1]]


        text_duration = (
            f"Czas trwania symulacji: {self.duration.total_seconds()}s \n"
        )
        formatted_args = ",\n".join(
            [", ".join([f"{arg:.4f}" for arg in args[i:i + 5]]) for i in range(0, len(args), 5)]
        )
        text_best_individual = (
            f"Najlepszy osobnik: {self.statistics[-1][2]} \n"
            f"dla argumentów:\n{formatted_args}"
        )

        best_value_label = ctk.CTkLabel(
            self,
            text=f"{text_duration} {text_best_individual}",
            font=("Arial", 14),
        )
        best_value_label.grid(row=1, column=0, columnspan=COL_NUM, pady=5)


        for i in range(1, 3):
            self.grid_rowconfigure(i, weight=1)

        self.display_plot()



