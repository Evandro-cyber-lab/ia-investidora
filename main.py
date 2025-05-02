from flask import Flask
import yfinance as yf
import ta
from datetime import datetime
import time

app = Flask(__name__)

@app.route('/')
def home():
    return "A IA está funcionando!"

def analisar_ativo(ativo="VALE3.SA"):
    print(f"⏳ Analisando {ativo} em {datetime.now().strftime('%d/%m %H:%M')}")
    try:
        df = yf.download(ativo, period="30d", interval="1d", progress=False)
        if df.empty:
            print("⚠️ Nenhum dado encontrado.")
            return

        df['rsi'] = ta.momentum.RSIIndicator(df['Close']).rsi()
        df['ema20'] = ta.trend.EMAIndicator(df['Close'], window=20).ema_indicator()
        macd = ta.trend.MACD(df['Close'])
        df['macd'] = macd.macd()
        df['macd_signal'] = macd.macd_signal()

        ult = df.iloc[-1]
        sinais = []

        if ult['rsi'] < 30:
            sinais.append("RSI indica COMPRA")
        if ult['macd'] > ult['macd_signal']:
            sinais.append("MACD cruzou = COMPRA")
        if ult['Close'] > ult['ema20']:
            sinais.append("Acima da média de 20 = COMPRA")

        if sinais:
            print("📈 Sinais detectados:")
            for s in sinais:
                print("✅", s)
        else:
            print("📉 Nenhum sinal agora.")
    except Exception as e:
        print("❌ Erro:", e)

# Loop para análise
def run_analysis():
    while True:
        analisar_ativo()
        time.sleep(3600)  # roda a cada 1 hora

# Iniciar servidor Flask e análise em segundo plano
if __name__ == '__main__':
    from threading import Thread
    # Iniciar o Flask app em uma thread separada
    thread = Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 5000})
    thread.start()

    # Iniciar a análise em segundo plano
    run_analysis()


# Loop 24/7
while True:
    analisar_ativo()
    time.sleep(3600)  # roda a cada 1 hora
