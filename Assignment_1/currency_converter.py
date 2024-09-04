import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage

exchange_rates = {
    "USD": {"EUR": 0.93, "GEL": 2.62},
    "EUR": {"USD": 1.08, "GEL": 2.81},
    "GEL": {"USD": 0.38, "EUR": 0.36},
}

class CurrencyConverterApp:
    WINDOW_TITLE = "ვალუტის კონვერტაციის აპლიკაცია"
    WINDOW_WIDTH = 500
    WINDOW_HEIGHT = 500
    
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.x = (self.screen_width - self.WINDOW_WIDTH) / 2
        self.y = (self.screen_height - self.WINDOW_HEIGHT) / 2
        
        self.bg = PhotoImage(file="Assignment_1/currency_exchange.png")
        self.result_var = tk.StringVar()
        
        self.amount_entry = tk.Entry(self.root, width=20)
        
        self.from_currency_var = tk.StringVar()
        self.from_currency_var.set("USD")
        self.to_currency_var = tk.StringVar()
        self.to_currency_var.set("EUR")
        
        self.create_window()
    
    def create_window(self):
        self.root.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}+{int(self.x)}+{int(self.y)}")
        self.root.minsize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.root.title(self.WINDOW_TITLE)
        
        background_label = tk.Label(self.root, image=self.bg)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        amount_frame = tk.Frame(self.root, bg="#f0f0f0")
        amount_frame.pack(fill="x", padx=20, pady=10, expand=True)
        tk.Label(amount_frame, text="შეიყვანეთ თანხა:", font=("Arial", 12), bg="#f0f0f0").pack(side="left", anchor="w")
        self.amount_entry = tk.Entry(amount_frame, width=20, font=("Arial", 12), bd=2)
        self.amount_entry.pack(side="left", anchor="e", padx=130)

        from_currency_frame = tk.Frame(self.root, bg="#f0f0f0")
        from_currency_frame.pack(fill="x", padx=20, pady=5, expand=True)
        tk.Label(from_currency_frame, text="საწყისი ვალუტა:", font=("Arial", 12), bg="#f0f0f0").pack(side="left", anchor="w")
        from_currency_menu = ttk.Combobox(from_currency_frame, textvariable=self.from_currency_var, values=["USD", "EUR", "GEL"], font=("Arial", 12))
        from_currency_menu.pack(side="left", anchor="e", padx=80)

        to_currency_frame = tk.Frame(self.root, bg="#f0f0f0")
        to_currency_frame.pack(fill="x", padx=20, pady=5, expand=True)
        tk.Label(to_currency_frame, text="ვალუტა კონვერტაციისთვის:", font=("Arial", 12), bg="#f0f0f0").pack(side="left", anchor="w")
        to_currency_menu = ttk.Combobox(to_currency_frame, textvariable=self.to_currency_var, values=["USD", "EUR", "GEL"], font=("Arial", 12))
        to_currency_menu.pack(side="left", anchor="e", padx=10)

        buttons_frame = tk.Frame(self.root, bg="#f0f0f0")
        buttons_frame.pack(fill="x", padx=20, pady=5, expand=True)
        convert_button = tk.Button(buttons_frame, text="კონვერტაცია", command=self.convert_currency, font=("Arial", 12), bg="#4CAF50", fg="white", padx=10, pady=5)
        convert_button.pack(side="left", padx=5, pady=10)
        clear_button = tk.Button(buttons_frame, text="გასუფთავება", command=self.clear_entries, font=("Arial", 12), bg="#f44336", fg="white", padx=10, pady=5)
        clear_button.pack(side="left", padx=5, pady=10)

        result_frame = tk.Frame(self.root, bg="#f0f0f0")
        result_frame.pack(fill="x", padx=20, pady=20, expand=True)
        tk.Label(result_frame, textvariable=self.result_var, font=("Arial", 14), bg="#f0f0f0").pack()

        self.root.mainloop()
    
    def convert_currency(self):
        error_message = "გთხოვთ შეიყვანოთ ვალიდური რიცხვი."
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                self.result_var.set(error_message)
                return
            elif amount > 1_000_000_000:
                self.result_var.set("შეიყვანეთ მცირე რიცხვი.")
                return
        except ValueError:
            self.result_var.set(error_message)
            return

        from_currency = self.from_currency_var.get()
        to_currency = self.to_currency_var.get()

        if from_currency == to_currency:
            result = amount
        else:
            result = amount * exchange_rates[from_currency][to_currency]

        self.result_var.set(f"{result:.2f} {to_currency}")
    
    def clear_entries(self):
        self.amount_entry.delete(0, tk.END)
        self.result_var.set("")

converter_app = CurrencyConverterApp()
