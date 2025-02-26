import streamlit as st
import FinanceDataReader as fdr
import pandas as pd
import datetime

# Streamlit title
st.title('주가 데이터 시각화')
st.header('')

st.divider()
st.subheader('설정창')
st.title('')

# User inputs for stock code and date range
stock_code = st.text_input("종목 코드 입력 :", '005930')
st.subheader('')

today = datetime.date.today()
one_year_ago = today - datetime.timedelta(days=365)

date_range = st.date_input("조회일 설정 :", [one_year_ago, today])


st.divider()
st.subheader('데이터 차트')
st.title('')

# Convert dates to string
start_date = date_range[0].strftime("%Y-%m-%d")
end_date = date_range[1].strftime("%Y-%m-%d")

# DataFrame with KRX listing
df_krx = fdr.StockListing('KRX')

def codeFromName(name):
    nameList = list(df_krx['Name'])
    return df_krx['Symbol'][nameList.index(name)]

# Fetch the stock data
df = fdr.DataReader(stock_code, start_date, end_date)

# Calculations for moving averages
ma5 = pd.DataFrame(df['Close'].rolling(window=5).mean())
ma20 = pd.DataFrame(df['Close'].rolling(window=20).mean())
ma60 = pd.DataFrame(df['Close'].rolling(window=60).mean())
ma120 = pd.DataFrame(df['Close'].rolling(window=120).mean())
ma240 = pd.DataFrame(df['Close'].rolling(window=240).mean())

df.insert(len(df.columns), '5일', ma5)
df.insert(len(df.columns), '20일', ma20)
df.insert(len(df.columns), '60일', ma60)
df.insert(len(df.columns), '120일', ma120)
df.insert(len(df.columns), '240일', ma240)

# Display the data
st.dataframe(df)

# Plot the data using Streamlit's line_chart and bar_chart
st.divider()
st.title('')

st.line_chart(df[['5일', '20일', '60일', '120일', '240일']])
st.header('')
st.bar_chart(df['Volume'])

