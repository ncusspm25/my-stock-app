import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="即時股價", layout="centered")
st.title("📈 即時股價查詢")

# --- 股票清單 (我有保留你的瑞昱) ---
my_stocks = {
    "台積電": "2330.TW",
    "鴻海": "2317.TW",
    "瑞昱": "2379.TW",
    "聯發科": "2454.TW",
    "長榮": "2603.TW",
    "NVIDIA": "NVDA",
    "特斯拉": "TSLA",
    "自訂輸入": "CUSTOM"
}

# --- 側邊欄選單 ---
selected = st.selectbox("請選擇股票：", list(my_stocks.keys()))

if my_stocks[selected] == "CUSTOM":
    symbol = st.text_input("輸入代號 (如 2330.TW)", "2330.TW").upper()
else:
    symbol = my_stocks[selected]

# --- 抓取與計算邏輯 ---
if symbol:
    try:
        stock = yf.Ticker(symbol)
        info = stock.fast_info
        
        # 1. 取得價格數據
        current_price = info.last_price
        previous_close = info.previous_close  # 昨收價
        
        # 2. 計算漲跌
        change_price = current_price - previous_close
        change_pct = (change_price / previous_close) * 100
        
        # 3. 顯示數據 (使用 metric 元件)
        # delta_color="inverse" 會讓漲變成紅色，跌變成綠色 (符合台灣習慣)
        st.metric(
            label=f"{symbol} 現價",
            value=f"{current_price:.2f}",
            delta=f"{change_price:.2f} ({change_pct:.2f}%)",
            delta_color="inverse" 
        )
        
        # 4. 畫圖
        st.write("今日走勢圖：")
        hist = stock.history(period="1d", interval="1m")
        if not hist.empty:
            st.line_chart(hist['Close'])
        else:
            st.warning("目前無即時走勢數據 (可能是休市中)")
            
    except Exception as e:
        st.error(f"查無資料或代號錯誤: {e}")
        
    # 按鈕手動更新
    if st.button("🔄 立即更新"):
        st.rerun()
