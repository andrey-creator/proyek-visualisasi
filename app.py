import pandas as pd
import streamlit as st
import yfinance as yf
import time
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard Saham King", layout="wide")

st.title("📊 Monitor Harga Saham Real-time")

st.sidebar.header("Konfigurasi")
ticker_symbol = st.sidebar.text_input("Simbol Saham", "BBCA.JK")
refresh_rate = st.sidebar.slider("Refresh (Detik)", 5, 60, 10)

placeholder = st.empty()

def ambil_data(simbol):
    try:
        df = yf.download(tickers=simbol, period='1d', interval='1m', progress=False)
        return df
    except:
        return None

while True:
    df = ambil_data(ticker_symbol)
    
    if df is not None and not df.empty:
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        harga_sekarang = float(df['Close'].iloc[-1])
        harga_buka = float(df['Open'].iloc[0])
        perubahan = harga_sekarang - harga_buka
        persen = (perubahan / harga_buka) * 100

        with placeholder.container():
            k1, k2, k3 = st.columns(3)
            fmt = "Rp {:,.0f}" if ".JK" in ticker_symbol else "${:,.2f}"
            
            k1.metric(label=f"Harga {ticker_symbol}", value=fmt.format(harga_sekarang), 
                      delta=f"{perubahan:,.2f} ({persen:.2f}%)")
            k2.metric("Tertinggi", fmt.format(df['High'].max()))
            k3.metric("Volume", f"{int(df['Volume'].iloc[-1]):,}")

            fig = go.Figure(data=[go.Candlestick(
                x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close']
            )])
            fig.update_layout(template="plotly_dark", height=400, margin=dict(l=10, r=10, t=10, b=10), xaxis_rangeslider_visible=False)
            
            # KUNCI PERBAIKAN: Gunakan key unik dengan time.time()
            st.plotly_chart(fig, use_container_width=True, key=f"chart_{time.time()}")
            
            st.caption(f"Update terakhir: {time.strftime('%H:%M:%S')}")

    time.sleep(refresh_rate)