import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="即時股價", layout="centered")
st.title("📈 即時股價查詢")

# 常用股票清單
my_stocks = {
    "台積電": "2330.TW",
    "鴻海": "2317.TW",
    "聯發科": "2454.TW",
    "長榮": "2603.TW",
    "NVIDIA": "NVDA",
    "自訂輸入": "CUSTOM"
}

selected = st.selectbox("請選擇股票：", list(my_stocks.keys()))

if my_stocks[selected] == "CUSTOM":
    symbol = st.text_input("輸入代號 (如 2330.TW)", "2330.TW").upper()
else:
    symbol = my_stocks[selected]

if st.button("查看股價") or symbol:
    try:
        stock = yf.Ticker(symbol)
        info = stock.fast_info
        st.metric(f"{symbol} 現價", f"{info.last_price:.2f}")
        
        hist = stock.history(period="1d", interval="1m")
        if not hist.empty:
            st.line_chart(hist['Close'])
        else:
            st.warning("目前無即時走勢數據")
    except:
        st.error("查無資料，請確認代號")
