import datetime
from tkinter import messagebox
from typing import Dict
import customtkinter as ctk
from app.algorithms.crossovers import AVAILABLE_CROSSOVERS, REAL_REPRESENTATION_CROSSOVERS
from app.algorithms.mutation import AVAILABLE_MUTATIONS, Inversion, REAL_REPRESENTATION_MUTATIONS
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

        self.real_representation_value = False

        self.render()
        self.population_config.switch_var.trace_add("write", self.on_real_representation_change)

    def layout(self):
        for i in range(COL_NUM):
            self.grid_columnconfigure(i, weight=1)

        for i in range(ROW_NUM):
            self.grid_rowconfigure(i, weight=1)

    def destroy_widgets(self, config):
        if hasattr(self, 'crossover_config'):
            for widget in config.winfo_children():
                widget.destroy()
            config.destroy()

    def render(self):
        self.title_label = ctk.CTkLabel(
            self,
            text=TITLE_TEXT,
            font=("Arial", TITLE_FONT_SIZE, "bold"),
        )
        self.title_label.grid(
            row=0, column=0, columnspan=COL_NUM, pady=FIELDS_PADY, sticky="nsew"
        )

        if hasattr(self, 'simulation_config'):
            self.destroy_widgets(self.simulation_config)
        
        self.simulation_config = SimulationConfig(self, 1, 0)

        if hasattr(self, 'population_config'):
            self.destroy_widgets(self.population_config)    
        self.population_config = PopulationConfig(self, 2, 0)

        if hasattr(self, 'selection_config'):
            self.destroy_widgets(self.selection_config)
        self.selection_config = MethodConfig(self, "Metoda selekcji", self.selection_methods, 2, 3)

        if hasattr(self, 'crossover_config'):
            self.destroy_widgets(self.crossover_config)
        self.crossover_config = MethodConfig(self, "Metoda krzyżowania", self.crossover_methods, 3, 0)

        if hasattr(self, 'mutation_config'):
            self.destroy_widgets(self.mutation_config)
        
        self.mutation_config = LabeledComboBox(self, "Metoda mutacji", list(self.mutation_methods.keys()), 3, 3)

        self.start_button = CustomButton(self, "Start", command=self.start_simulation)
        self.start_button.grid(
            row=4,
            column=2,
            columnspan=int(COL_NUM / 3),
            pady=FIELDS_PADY * 2,
            sticky="ew",
        )
        
        self.population_config.switch_var.set("on" if self.real_representation_value else "off")

    def start_simulation(self):
        """Sprawdza wszystkie parametry i uruchamia symulację, jeśli są poprawne."""
        try:
            simulation = self.simulation_config.get_values()
            population = self.population_config.get_values()

            mutation_class = next(
                (
                    cls
                    for cls in AVAILABLE_MUTATIONS + REAL_REPRESENTATION_MUTATIONS
                    if cls.getName() == self.mutation_config.get_value()
                ),
                None,
            )
            if mutation_class:
                if self.real_representation_value:
                    population = Population(
                        simulation["Zakres (początek)"],
                        simulation["Zakres (koniec)"],
                        func=simulation["Funkcja celu"],
                        n_of_variables=simulation["Liczba argumentów"],
                        population_size=population["Liczność populacji"],
                        precision=population["Dokładność reprezentacji chromosomu"],
                        optimization_type=self.selection_config.get_method_instance().optimization_type,
                        best_indv_number=population["Liczba najlepszych osobników"],
                        real_representation=self.real_representation_value,
                    )
                else:
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
                        real_representation=self.real_representation_value,
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

            from copy import deepcopy

            function_targets = []
            all_times = []
            all_times.append(deepcopy(results[1].total_seconds()))
            function_targets.append(deepcopy(results[0][-1][2]))
            all_results = []
            all_results.append(deepcopy(results))

            for i in range(9):
                simulation.run()
                results = simulation.get_statistics()
                all_times.append(deepcopy(results[1].total_seconds()))
                all_results.append(deepcopy(results))
                function_targets.append(deepcopy(results[0][-1][2]))

            best_optimum = max(function_targets) if simulation.population.optimization_type == "max" else min(function_targets)
            idx = function_targets.index(best_optimum)
            best_time = all_times[idx]

            worst_function = min(function_targets) if simulation.population.optimization_type == "max" else max(function_targets)
            idx = function_targets.index(worst_function)
            worst_time = all_times[idx]

            print(f"Najlepszy wynik: {best_optimum} w czasie {best_time}")
            print(f"Najgorszy wynik: {worst_function} w czasie {worst_time}")
            print(f"Średni czas: {sum(all_times) / len(all_times)}")
            print(f"srdeni wynik: {sum(function_targets) / len(function_targets)}")

            best_results = all_results[idx]

            for i in range(1, ROW_NUM):
                self.grid_rowconfigure(i, weight=1)

            result_page = ResultsPage(self, best_results)
            result_page.grid(row=1, column=6, columnspan=COL_NUM, rowspan=ROW_NUM-2, sticky="nsew", padx=10, pady=10)

        except KeyError as e:
            messagebox.showerror("Brakujący parametr", e)
        except ValueError as e:
            messagebox.showerror("Niepoprawna wartość", e)
        except Exception as e:
            messagebox.showerror("Coś poszło nie tak", e)

    def on_real_representation_change(self, *args):
        self.real_representation_value = not self.real_representation_value
        if self.real_representation_value:
            self.mutation_methods = {
                mutation.getName(): mutation for mutation in REAL_REPRESENTATION_MUTATIONS
            }
            self.crossover_methods = {
                crossover.getName(): (
                crossover.getParamteres(),
                crossover.validateParameters,
            )
            for crossover in REAL_REPRESENTATION_CROSSOVERS
            }

        else:
            self.mutation_methods = {
                mutation.getName(): mutation for mutation in AVAILABLE_MUTATIONS
            }
            self.crossover_methods = {
                crossover.getName(): (
                crossover.getParamteres(),
                crossover.validateParameters,
            )
            for crossover in AVAILABLE_CROSSOVERS
            }


        self.render()
        self.population_config.switch_var.trace_add("write", self.on_real_representation_change)

