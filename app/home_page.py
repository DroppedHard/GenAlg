from tkinter import messagebox
from typing import Dict
import customtkinter as ctk
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
from app.result_page import ResultsPage


class HomePage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.layout()
        self.param_entries = {}

        self.selection_methods = {
            sel.getName(): (sel.getParamteres(), sel.validateParameters)
            for sel in AVAILABLE_SELECTIONS
        }

        self.crossover_methods = {
            crossover.getName(): (
                crossover.getParamteres(),
                crossover.validateParameters,
            )
            for crossover in AVAILABLE_CROSSOVERS
        }

        self.mutation_methods = {
            mutation.getName(): mutation for mutation in AVAILABLE_MUTATIONS
        }

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

        self.simulation_config = SimulationConfig(self, 1, 0)

        self.population_config = PopulationConfig(self, 2, 0)

        self.selection_config = MethodConfig(
            self, "Metoda selekcji", self.selection_methods, 2, 3
        )

        self.crossover_config = MethodConfig(
            self, "Metoda krzyżowania", self.crossover_methods, 3, 0
        )
        self.mutation_config = LabeledComboBox(
            self, "Metoda mutacji", list(self.mutation_methods.keys()), 3, 3
        )

        self.start_button = CustomButton(self, "Start", command=self.start_simulation)
        self.start_button.grid(
            row=4,
            column=2,
            columnspan=int(COL_NUM / 3),
            pady=FIELDS_PADY * 2,
            sticky="ew",
        )

    def start_simulation(self):
        """Sprawdza wszystkie parametry i uruchamia symulację, jeśli są poprawne."""
        try:
            simulation = self.simulation_config.get_values()
            population = self.population_config.get_values()

            mutation_class = next(
                (
                    cls
                    for cls in AVAILABLE_MUTATIONS
                    if cls.getName() == self.mutation_config.get_value()
                ),
                None,
            )
            if mutation_class:
                population = Population(
                    simulation["Zakres (początek)"],
                    simulation["Zakres (koniec)"],
                    func=simulation["Funkcja celu"],
                    n_of_variables=simulation["Liczba argumentów"],
                    chrom_length=population["Długość chromosomu"],
                    population_size=population["Liczność populacji"],
                    precision=population["Dokładność reprezentacji chromosomu"],
                    optimization_type=self.selection_config.get_method_instance().optimization_type,
                    best_indv_number=population["Liczba najlepszych osobników"],
                )
                simulation = Simulation(
                    epochs=simulation["Liczba epok"],
                    population=population,
                    inversion=Inversion(simulation["Prawdopodobieństwo inwersji"]),
                    selection=self.selection_config.get_method_instance(),
                    crossover=self.crossover_config.get_method_instance(),
                    mutation=mutation_class(simulation["Prawdopodobieństwo mutacji"]),
                )
                simulation.run()
                
            results = simulation.get_statistics()

            for i in range(1, ROW_NUM):
                self.grid_rowconfigure(i, weight=1)

            result_page = ResultsPage(self, results)
            result_page.grid(row=1, column=6, columnspan=COL_NUM, rowspan=ROW_NUM-2, sticky="nsew", padx=10, pady=10)

        except KeyError as e:
            messagebox.showerror("Brakujący parametr", e)
        except ValueError as e:
            messagebox.showerror("Niepoprawna wartość", e)
        except Exception as e:
            messagebox.showerror("Coś poszło nie tak", e)
