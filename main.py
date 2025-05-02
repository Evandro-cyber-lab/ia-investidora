import yfinance as yf
import pandas as pd
import time
from ta.trend import EMAIndicator

# Lista de ativos
ativos = ['PETR4.SA', 'VALE3.SA', 'ITUB4.SA']

def obter_dados(ativos):
    try:
        dados = yf.download(ativos, period='7d', interval='1h', group_by='ticker', threads=True)
        return dados
    except Exception as e:
        print(f"Erro ao baixar dados: {e}")
        return None

def aplicar_estrategia(df):
    if df is None or df.empty:
        return None
    df['EMA20'] = EMAIndicator(close=df['Close'], window=20).ema_indicator()
    df['EMA50'] = EMAIndicator(close=df['Close'], window=50).ema_indicator()
    if df['EMA20'].iloc[-1] > df['EMA50'].iloc[-1]:
        return "Comprar"
    elif df['EMA20'].iloc[-1] < df['EMA50'].iloc[-1]:
        return "Vender"
    else:
        return "Aguardar"

def executar():
    print("Iniciando IA Investidora...")
    while True:
        print("\nVerificando ativos...")
        dados = obter_dados(ativos)
        for ativo in ativos:
            print(f"\nAnalisando {ativo}...")
            try:
                df = dados[ativo] if ativo in dados.columns.levels[0] else None
                if df is not None:
                    df = df.dropna()
                    resultado = aplicar_estrategia(df)
                    print(f"{ativo}: {resultado}")
                else:
                    print(f"Dados não disponíveis para {ativo}")
            except Exception as e:
                print(f"Erro ao analisar {ativo}: {e}")
            time.sleep(2)  # Espera entre ativos para evitar bloqueio
        print("\nAguardando 10 minutos para nova verificação...\n")
        time.sleep(600)  # Espera 10 minutos entre ciclos

if __name__ == '__main__':
    executar()
