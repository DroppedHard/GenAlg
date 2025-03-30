import customtkinter as ctk
import tkinter as tk
from app.home_page import HomePage


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Ewolucyjny Algorytm Genetyczny")
        self.geometry("1000x750")
        self.iconphoto(False, tk.PhotoImage(file="assets/title_icon.png"))

        self.home_page = HomePage(self)
        self.home_page.pack(fill="both", expand=True)
