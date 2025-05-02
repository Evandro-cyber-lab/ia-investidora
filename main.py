import yfinance as yf
import time
from datetime import datetime

# Lista de ativos que você quer analisar
ativos = ['PETR4.SA', 'ITUB4.SA', 'VALE3.SA']

# Função para analisar um ativo
def analisar_ativo(ticker):
    try:
        print(f"\n⏳ Analisando {ticker} em {datetime.now().strftime('%d/%m %H:%M:%S')}")
        dados = yf.download(ticker, period="5d", interval="1h")
        if dados.empty:
            print(f"⚠️ Dados não encontrados para {ticker}")
            return
        
        fechamento = dados["Close"]
        if len(fechamento) < 2:
            print(f"⚠️ Dados insuficientes para {ticker}")
            return

        atual = fechamento.iloc[-1]
        anterior = fechamento.iloc[-2]
        variacao = ((atual - anterior) / anterior) * 100

        print(f"📈 {ticker} - Último: R${atual:.2f} | Anterior: R${anterior:.2f} | Variação: {variacao:.2f}%")

        if variacao > 2:
            print(f"🚀 {ticker} está subindo forte! Possível compra.")
        elif variacao < -2:
            print(f"📉 {ticker} está caindo forte! Possível venda.")
        else:
            print(f"🟡 {ticker} está estável.")

    except Exception as e:
        print(f"❌ Erro ao analisar {ticker}: {e}")

# Loop infinito
while True:
    for ativo in ativos:
        analisar_ativo(ativo)
        time.sleep(30)  # Espera 30 segundos entre ativos

    print("\n⏳ Esperando 2 minutos para nova rodada de análises...\n")
    time.sleep(120)  # Espera 2 minutos antes de começar tudo de novo
