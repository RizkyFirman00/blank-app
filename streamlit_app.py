import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Load data
df = pd.read_csv("indo_sentiment_results.csv")

st.title("📊 Visualisasi Analisis Sentimen")

# 1️⃣ Bar Chart Sentimen
st.subheader("Distribusi Sentimen")
sentiment_counts = df['sentiment'].value_counts()

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, palette="coolwarm", ax=ax)
ax.set_xlabel("Sentimen")
ax.set_ylabel("Jumlah Komentar")
ax.set_title("Distribusi Sentimen dalam Dataset")
st.pyplot(fig)

# 2️⃣ Pie Chart Sentimen
st.subheader("Proporsi Sentimen")

fig, ax = plt.subplots()
ax.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', colors=['lightcoral', 'gold', 'lightblue'])
ax.set_title("Persentase Sentimen")
st.pyplot(fig)

# 3️⃣ Word Cloud untuk Setiap Sentimen
st.subheader("Word Cloud Berdasarkan Sentimen")
sentiment_types = df['sentiment'].unique()

for sentiment in sentiment_types:
    st.write(f"**{sentiment.capitalize()}**")
    text = " ".join(df[df['sentiment'] == sentiment]['clean_comment'].astype(str))
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)

# 4️⃣ Histogram Panjang Komentar
st.subheader("Distribusi Panjang Komentar")

df["comment_length"] = df["clean_comment"].astype(str).apply(len)

fig, ax = plt.subplots(figsize=(8, 5))
sns.histplot(df["comment_length"], bins=30, kde=True, color="purple")
ax.set_xlabel("Panjang Komentar")
ax.set_ylabel("Frekuensi")
ax.set_title("Histogram Panjang Komentar")
st.pyplot(fig)