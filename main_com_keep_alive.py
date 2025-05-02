import yfinance as yf
import time
from datetime import datetime
from keep_alive import iniciar

def analisar_mercado(ticker):
    dados = yf.download(ticker, period="1d", interval="1m")
    if dados.empty:
        print(f"[{datetime.now()}] Nenhum dado encontrado para {ticker}.")
        return "aguardando"

    ultima_linha = dados.iloc[-1]
    preco_atual = ultima_linha["Close"]
    media_20 = dados["Close"].rolling(window=20).mean().iloc[-1]

    if preco_atual > media_20:
        return "comprar"
    elif preco_atual < media_20:
        return "vender"
    else:
        return "aguardando"

iniciar()

def executar():
    while True:
        acao = analisar_mercado("AAPL")
        print(f"[{datetime.now()}] Sinal para AAPL: {acao}")
        time.sleep(60)

executar()
