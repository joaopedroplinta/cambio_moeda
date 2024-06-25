import tkinter as tk
from tkinter import ttk, messagebox
import requests

class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.setup_ui()

    def get_exchange_rate(self, api_key, from_currency, to_currency):
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{from_currency}"
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200 or 'error' in data:
            raise Exception("Erro ao obter a taxa de câmbio")

        rates = data['conversion_rates']
        return rates[to_currency]

    def convert_currency(self):
        api_key = "35431a1fc80d21e69834bd22"
        from_currency = self.from_currency_entry.get().upper()
        to_currency = self.to_currency_entry.get().upper()
        try:
            amount = float(self.amount_entry.get())
            rate = self.get_exchange_rate(api_key, from_currency, to_currency)
            converted_amount = amount * rate
            self.result_label.config(text=f"{amount} {from_currency} é igual a {converted_amount:.2f} {to_currency}")
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um valor numérico válido.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def center_window(self, width=400, height=250):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def setup_ui(self):
        self.root.title("Conversor de Moedas")
        self.center_window(400, 300)

        style = ttk.Style(self.root)
        try:
            self.root.tk.call('source', 'azure.tcl')
            style.theme_use('azure-dark')
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar o tema: {e}")

        font_label = ('Arial', 12)
        font_entry = ('Arial', 12)
        font_button = ('Arial', 12, 'bold')
        font_result = ('Arial', 14, 'bold')

        frame = ttk.Frame(self.root, padding="10 10 10 10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        ttk.Label(frame, text="Moeda de origem (ex: USD):", font=font_label).grid(row=0, column=0, sticky='e')
        self.from_currency_entry = ttk.Entry(frame, width=10, font=font_entry)
        self.from_currency_entry.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="Moeda de destino (ex: BRL):", font=font_label).grid(row=1, column=0, sticky='e')
        self.to_currency_entry = ttk.Entry(frame, width=10, font=font_entry)
        self.to_currency_entry.grid(row=1, column=1, pady=5)

        ttk.Label(frame, text="Valor a ser convertido:", font=font_label).grid(row=2, column=0, sticky='e')
        self.amount_entry = ttk.Entry(frame, width=10, font=font_entry)
        self.amount_entry.grid(row=2, column=1, pady=5)

        convert_button = ttk.Button(frame, text="Converter", command=self.convert_currency, style="TButton", padding=5)
        convert_button.grid(row=3, columnspan=2, pady=10)

        self.result_label = ttk.Label(frame, text="", font=font_result)
        self.result_label.grid(row=4, columnspan=2, pady=10)

        for child in frame.winfo_children():
            child.grid_configure(padx=5, pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()