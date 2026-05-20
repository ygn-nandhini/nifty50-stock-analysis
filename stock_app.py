import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Nifty 50 Stock Dashboard")
st.write("Welcome to Stock Performance Analysis!")

# Data Load
df = pd.read_csv(r"C:\Users\admin\Downloads\final_stock_data.csv")
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by=['Ticker', 'date'])
df['daily_return'] = df.groupby('Ticker')['close'].pct_change().fillna(0)

st.write("Total Rows:", df.shape[0])

st.header("Top 10 Most Volatile Stocks")

volatility = df.groupby('Ticker')['daily_return'].std().sort_values(ascending=False).head(10)

fig, ax = plt.subplots(figsize=(12,6))
volatility.plot(kind='bar', ax=ax, color='orange')
ax.set_title("Top 10 Most Volatile Stocks")
ax.set_xlabel("Ticker")
ax.set_ylabel("Volatility")
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)

#q2:
st.header("Cumulative Return - Top 5 Stocks")

df['cumulative_return'] = (1 + df['daily_return']).groupby(df['Ticker']).cumprod()
final = df.groupby('Ticker')['cumulative_return'].last()
top5_stocks = final.sort_values(ascending=False).head(5).index
df_top5 = df[df['Ticker'].isin(top5_stocks)]

fig, ax = plt.subplots(figsize=(10,5))
for stock in top5_stocks:
    data = df_top5[df_top5['Ticker'] == stock]
    ax.plot(data['date'], data['cumulative_return'], label=stock)
ax.set_title("Cumulative Return - Top 5 Stocks")
ax.set_xlabel("Date")
ax.set_ylabel("Cumulative Return")
ax.legend()
plt.tight_layout()

st.pyplot(fig)

#Q3:
st.header("Average Yearly Return by Sector")

yearly = df.groupby('Ticker')['close'].apply(
    lambda x: ((x.iloc[-1] - x.iloc[0]) / x.iloc[0]) * 100
).reset_index(name='Yearly_Return')

sector_data = {
    'Ticker': ['ADANIENT','ADANIPORTS','APOLLOHOSP','ASIANPAINT','AXISBANK',
               'BAJAJ-AUTO','BAJAJFINSV','BAJFINANCE','BEL','BHARTIARTL',
               'BPCL','BRITANNIA','CIPLA','COALINDIA','DRREDDY',
               'EICHERMOT','GRASIM','HCLTECH','HDFCBANK','HDFCLIFE',
               'HEROMOTOCO','HINDALCO','HINDUNILVR','ICICIBANK','INDUSINDBK',
               'INFY','ITC','JSWSTEEL','KOTAKBANK','LT',
               'M&M','MARUTI','NESTLEIND','NTPC','ONGC',
               'POWERGRID','RELIANCE','SBILIFE','SBIN','SHRIRAMFIN',
               'SUNPHARMA','TATACONSUM','TATAMOTORS','TATASTEEL','TCS',
               'TECHM','TITAN','TRENT','ULTRACEMCO','WIPRO'],
    'Sector': ['Energy','Infrastructure','Healthcare','Consumer Goods','Financials',
               'Automobile','Financials','Financials','Defence','Telecom',
               'Energy','Consumer Goods','Healthcare','Energy','Healthcare',
               'Automobile','Cement','IT','Financials','Financials',
               'Automobile','Metals','Consumer Goods','Financials','Financials',
               'IT','Consumer Goods','Metals','Financials','Infrastructure',
               'Automobile','Automobile','Consumer Goods','Energy','Energy',
               'Energy','Energy','Financials','Financials','Financials',
               'Healthcare','Consumer Goods','Automobile','Metals','IT',
               'IT','Consumer Goods','Retail','Cement','IT']
}
sector_df = pd.DataFrame(sector_data)
merged = pd.merge(yearly, sector_df, on='Ticker')
sector_avg = merged.groupby('Sector')['Yearly_Return'].mean().sort_values(ascending=False)

colors = ['green' if x > 0 else 'red' for x in sector_avg]

fig, ax = plt.subplots(figsize=(12,6))
sector_avg.plot(kind='bar', ax=ax, color=colors)
ax.set_title("Average Yearly Return by Sector")
ax.set_xlabel("Sector")
ax.set_ylabel("Return (%)")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

st.pyplot(fig)

#Q4:
st.header("Stock Price Correlation Heatmap")

pivot = df.pivot_table(index='date', columns='Ticker', values='close')
corr_matrix = pivot.corr()

fig, ax = plt.subplots(figsize=(20,15))
im = ax.imshow(corr_matrix, cmap='RdYlGn', aspect='auto')
plt.colorbar(im, ax=ax)
ax.set_xticks(range(len(corr_matrix.columns)))
ax.set_yticks(range(len(corr_matrix.columns)))
ax.set_xticklabels(corr_matrix.columns, rotation=90)
ax.set_yticklabels(corr_matrix.columns)
ax.set_title("Stock Price Correlation Heatmap")
plt.tight_layout()

st.pyplot(fig)

#Q5:
st.header("Top 5 Gainers & Losers - Month Wise")

df['month'] = df['date'].dt.month

monthly_return = df.groupby(['Ticker', 'month'])['close'].apply(
    lambda x: ((x.iloc[-1] - x.iloc[0]) / x.iloc[0]) * 100
).reset_index(name='Monthly_Return')

months = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun',
          7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}

for month in range(1, 13):
    gainers = monthly_return[monthly_return['month'] == month].nlargest(5, 'Monthly_Return')
    losers = monthly_return[monthly_return['month'] == month].nsmallest(5, 'Monthly_Return')
    
    combined = pd.concat([gainers, losers])
    colors = ['green' if x > 0 else 'red' for x in combined['Monthly_Return']]
    
    fig, ax = plt.subplots(figsize=(10,5))
    ax.bar(combined['Ticker'], combined['Monthly_Return'], color=colors)
    ax.set_title(f"{months[month]} - Top 5 Gainers & Losers")
    ax.set_xlabel("Stock")
    ax.set_ylabel("Return (%)")
    ax.axhline(y=0, color='black', linewidth=0.8)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    st.pyplot(fig)