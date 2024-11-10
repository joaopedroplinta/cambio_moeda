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
            self.result_label.config(text=f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}", foreground="white")
            self.status_label.config(text="Conversão realizada com sucesso!", foreground="lightgreen")
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um valor numérico válido.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
            self.status_label.config(text="Erro na conversão.", foreground="lightcoral")

    def clear_fields(self):
        self.from_currency_entry.delete(0, tk.END)
        self.to_currency_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.result_label.config(text="")
        self.status_label.config(text="")

    def center_window(self, width=400, height=350):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def setup_ui(self):
        self.root.title("Conversor de Moedas")
        self.center_window(500, 400)
        self.root.config(bg="#2e3b4e")

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
        font_status = ('Arial', 10)

        frame = ttk.Frame(self.root, padding="20", style="TFrame", relief="solid", borderwidth=2)
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=20, pady=20)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        title_label = ttk.Label(frame, text="Conversor de Moedas", font=('Arial', 18, 'bold'), foreground="white", background="#2e3b4e")
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(frame, text="Moeda de origem (ex: USD):", font=font_label, background="#2e3b4e", foreground="white").grid(row=1, column=0, sticky='e')
        self.from_currency_entry = ttk.Entry(frame, width=20, font=font_entry)
        self.from_currency_entry.grid(row=1, column=1, pady=10)

        ttk.Label(frame, text="Moeda de destino (ex: BRL):", font=font_label, background="#2e3b4e", foreground="white").grid(row=2, column=0, sticky='e')
        self.to_currency_entry = ttk.Entry(frame, width=20, font=font_entry)
        self.to_currency_entry.grid(row=2, column=1, pady=10)

        ttk.Label(frame, text="Valor a ser convertido:", font=font_label, background="#2e3b4e", foreground="white").grid(row=3, column=0, sticky='e')
        self.amount_entry = ttk.Entry(frame, width=20, font=font_entry)
        self.amount_entry.grid(row=3, column=1, pady=10)

        convert_button = ttk.Button(frame, text="Converter", command=self.convert_currency, style="TButton", padding=10)
        convert_button.grid(row=4, column=0, pady=15)

        clear_button = ttk.Button(frame, text="Limpar", command=self.clear_fields, style="TButton", padding=10)
        clear_button.grid(row=4, column=1, pady=15)

        self.result_label = ttk.Label(frame, text="", font=font_result, background="#2e3b4e", foreground="white")
        self.result_label.grid(row=5, columnspan=2, pady=10)

        self.status_label = ttk.Label(frame, text="", font=font_status, background="#2e3b4e", foreground="lightgray")
        self.status_label.grid(row=6, columnspan=2, pady=5)

        for child in frame.winfo_children():
            child.grid_configure(padx=10, pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()