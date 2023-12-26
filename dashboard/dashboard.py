import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st


def create_df_articles_top(df):
    articles_top = df.groupby('article').agg({'quantity': 'sum'}).sort_values(
        by='quantity', ascending=False).reset_index().head(10)
    return articles_top


def create_df_articles_bottom(df):
    articles_bottom = df.groupby('article').agg({'quantity': 'sum'}).sort_values(
        by='quantity', ascending=True).reset_index().head(10)
    return articles_bottom


def create_df_hours_order(df):
    hours_sales = df.groupby('hour').agg({'quantity': 'sum'}).reset_index()
    return hours_sales


def create_df_daily_order(df):
    daily = df.groupby(pd.to_datetime(df['date']).dt.strftime('%A'))[
        'quantity'].sum().sort_values(ascending=False)
    return daily


def create_df_monthly_order(df):
    monthly = df.groupby("M", as_index=False).agg(
        total_sales_volume=("quantity", "sum"))
    return monthly


def create_df_daily_sales(df):
    daily_sales = df.groupby('date').agg({'total': 'sum'}).reset_index()
    return daily_sales


all_df = pd.read_csv('df.csv')

st.set_page_config(
    page_title="Forecasting",
    layout="wide"

)


df_articles_top = create_df_articles_top(all_df)
df_articles_bottom = create_df_articles_bottom(all_df)
df_hours_order = create_df_hours_order(all_df)
df_daily_order = create_df_daily_order(all_df)
df_monthly_order = create_df_monthly_order(all_df)
df_daily_sales = create_df_daily_sales(all_df)

st.title("Forecasting Penjualan Roti")


col1, col2 = st.columns(2)


with col1:
    fig, ax = plt.subplots(figsize=(10, 6))
    # colors = ["#DAA520",  "#B0C4DE", "#B0C4DE", "#B0C4DE", "#B0C4DE",
    #           "#B0C4DE", "#B0C4DE", "#B0C4DE", "#B0C4DE", "#B0C4DE"]
    colors = ["#398cfe", "#7FB5FF", "#7FB5FF", "#7FB5FF", "#7FB5FF",
              "#7FB5FF", "#7FB5FF", "#7FB5FF", "#7FB5FF", "#7FB5FF"]
    sns.barplot(x="quantity", y="article",
                data=df_articles_top, palette=colors)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.set_title("10 Roti Terlaris", fontsize=30)
    ax.tick_params(axis='y', labelsize=10)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ["#F98404", "#F98404", "#F98404", "#F98404", "#F98404",
              "#F98404", "#F98404", "#F98404", "#ffbe78", "#ffbe78"]
    sns.barplot(x="quantity", y="article",
                data=df_articles_bottom, palette=colors)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.set_title("10 Roti Tidak Laris", fontsize=30)
    ax.tick_params(axis='y', labelsize=10)
    st.pyplot(fig)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
col3, col4 = st.columns(2)

with col3:
    fig = px.pie(df_hours_order, names="hour",
                 values=df_hours_order['quantity'], hole=0.6, title="Total Roti Terjual Per Jam")
    fig.update_traces(textposition='inside',
                      textinfo='percent+label', sort=False)
    fig.update_layout(height=500, width=500)
    fig.update_layout(title_font=dict(size=30))
    fig.update_layout(title_x=0.2)
    st.plotly_chart(fig)

with col4:
    fig = px.pie(df_daily_order, df_daily_order.index, values=df_daily_order.values,
                 hole=0.6, title="Total Roti Terjual Per Hari")
    fig.update_traces(textposition='outside',
                      textinfo='percent+label', sort=False)
    fig.update_layout(height=500, width=500)
    fig.update_layout(title_font=dict(size=30))
    fig.update_layout(title_x=0.2)
    st.plotly_chart(fig)

st.markdown("<br>", unsafe_allow_html=True)


col5, col6 = st.columns(2)

with col5:
    fig = px.pie(df_monthly_order, names="M", values="total_sales_volume",
                 hole=0.6, title="Total Roti Terjual Per Bulan")
    fig.update_traces(textposition='outside',
                      textinfo='percent+label', sort=False)
    fig.update_layout(height=500, width=500)
    fig.update_layout(title_font=dict(size=30))
    fig.update_layout(title_x=0.2)
    st.plotly_chart(fig)

with col6:
    df_daily_sales['date'] = pd.to_datetime(df_daily_sales['date'])
    df_daily_sales.set_index('date', inplace=True)
    weekly_sales = df_daily_sales.resample('W').sum()
    fig, ax = plt.subplots(figsize=(15, 8))
    ax.plot(weekly_sales.index, weekly_sales['total'])
    ax.set_title('Penjualan Mingguan', fontsize=30)
    st.pyplot(fig)


fig, ax = plt.subplots(figsize=(15, 5))
ax.plot(df_daily_sales.index, df_daily_sales['total'])
ax.set_title('Penjualan Harian', fontsize=20)
st.pyplot(fig)
