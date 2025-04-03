import customtkinter as ctk
from matplotlib.figure import Figure
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
        self.statistics = statistics

        self.render()

    def layout(self):
        for i in range(COL_NUM):
            self.grid_columnconfigure(i, weight=1)

        for i in range(ROW_NUM):
            self.grid_rowconfigure(i, weight=1)

    def render(self):
        self.title_label = ctk.CTkLabel(
            self,
            text=TITLE_TEXT,
            font=("Arial", TITLE_FONT_SIZE, "bold"),
        )
        self.title_label.grid(
            row=0, column=0, columnspan=COL_NUM, pady=FIELDS_PADY, sticky="nsew"
        )

        # print a plot of the statistics
        fig = Figure()
        
        

   