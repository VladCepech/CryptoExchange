import requests
import json
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb


class CryptoInfo:
    def __init__(self, crypto_code):
        self.crypto_code = crypto_code
        self.rate_usd = self.get_info('USD')
        self.rate_eur = self.get_info('EUR')
        self.rate_rub = self.get_info('RUB')

    def get_info(self, curr_code):
        try:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={self.crypto_code}&vs_currencies={curr_code}"
            response = requests.get(url)
            if response.status_code == 429:
                mb.showerror('Error', f'Слишком много запросов\nПопробуйте еще раз позже!')
            data = json.loads(response.text)
            return data[self.crypto_code][curr_code.lower()]
        except Exception as e:
            mb.showerror('Error!', f'Error: {e}')


def refresh_rate():
    global btc
    crypt = combo_from.get()
    btc = CryptoInfo(crypto_list[crypt])
    rate_usd.config(text=f'1 {btc.crypto_code.capitalize()} = {btc.rate_usd:,} USD')
    rate_eur.config(text=f'1 {btc.crypto_code.capitalize()} = {btc.rate_eur:,} EUR')
    rate_rub.config(text=f'1 {btc.crypto_code.capitalize()} = {btc.rate_rub:,} RUB')


crypto_list = {
    "BTC": 'bitcoin',
    'LTC': 'litecoin',
    'ETH': 'ethereum',
    'XRP': 'ripple',
    'ADA': 'cardano'
}

crypto_codes = list(crypto_list.keys())

btc = CryptoInfo('bitcoin')

window = Tk()
window.title('Crypto-to-Currency Exchange Rates')
window.geometry(f'450x300+{window.winfo_screenwidth() // 2 - 200}+{window.winfo_screenheight() // 2 - 150}')
window.iconbitmap('btc.ico')

rate_usd = Label(window, text=f'1 Bitcoin = {btc.rate_usd:,} USD', width=25, font='Arial 20', anchor="w")
rate_usd.grid(row=0, column=0, columnspan=4, sticky='ew', pady=(15, 10), padx=20)

rate_eur = Label(window, text=f'1 Bitcoin = {btc.rate_eur:,} EUR', width=25, font='Arial 20', anchor="w")
rate_eur.grid(row=1, column=0, columnspan=4, sticky='ew', pady=(10, 20), padx=20)

rate_rub = Label(window, text=f'1 Bitcoin = {btc.rate_rub:,} RUB', width=25, font='Arial 20', anchor="w")
rate_rub.grid(row=2, column=0, columnspan=4, sticky='ew', pady=(10, 20), padx=20)

cripto_from = Label(window, text='Choose : ', font='Arial 20')
cripto_from.grid(row=3, column=0, padx=(10, 0))

combo_from = ttk.Combobox(window, width=4, font='Arial 14', values=crypto_codes)
combo_from.current(0)
combo_from.grid(row=3, column=1)

Button(window, text='Refresh', font='Arial 20', command=refresh_rate).grid(row=3, column=2, pady=15)

window.mainloop()
