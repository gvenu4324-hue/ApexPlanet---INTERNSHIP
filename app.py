import pandas as pd
import streamlit as st
import plotly.express as px
from scipy.stats import chisquare
from pathlib import Path

st.set_page_config(page_title="Netflix Content Analysis", page_icon="🎬", layout="wide")

DATA = Path(__file__).parent / "data" / "cleaned_dataset.csv"
CERT = Path(__file__).parent / "assets" / "certificate.png"

@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\Users\David Chua\Desktop\ApexPlanet - INTERNSHIP\Task-1-DATA IMMERSION AND WRANGLING\netflix_titles_cleaned.csv")
    df["country"] = df["country"].fillna("Unknown").apply(lambda x: x.split(",")[0].strip())
    df["genre"] = df["listed_in"].apply(lambda x: x.split(",")[0].strip())
    df["rating"] = df["rating"].fillna(df["rating"].mode()[0])
    return df

df = load_data()

# ---------- Sidebar ----------
st.sidebar.title("🎬 Netflix Analysis")
page = st.sidebar.radio("Go to", ["Overview", "Dashboard", "Explorer", "Hypothesis Test", "Certificate"])
types = st.sidebar.multiselect("Type", df["type"].unique(), default=df["type"].unique())
years = st.sidebar.slider("Release Year", int(df.release_year.min()), int(df.release_year.max()), (2015, 2021))
f = df[df["type"].isin(types) & df["release_year"].between(*years)]

# ---------- Overview ----------
if page == "Overview":
    st.title("Netflix Movies & TV Shows Analysis")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Titles", len(df))
    c2.metric("Movies", (df.type == "Movie").sum())
    c3.metric("TV Shows", (df.type == "TV Show").sum())
    st.markdown("""
    - 🎥 Movies make up ~70% of all content  
    - 🇺🇸 USA leads content production, followed by India  
    - 🔞 TV-MA is the most common rating  
    - 📈 Content additions peaked around 2018–2019  
    """)
    st.dataframe(df.head(10), use_container_width=True)

# ---------- Dashboard ----------
elif page == "Dashboard":
    st.title("📊 Dashboard")
    col1, col2 = st.columns(2)
    col1.plotly_chart(px.bar(f.type.value_counts(), title="Movies vs TV Shows"), use_container_width=True)
    col2.plotly_chart(px.bar(f.country.value_counts().head(10), title="Top 10 Countries"), use_container_width=True)

    col3, col4 = st.columns(2)
    col3.plotly_chart(px.bar(f.rating.value_counts(), title="Ratings Distribution"), use_container_width=True)
    col4.plotly_chart(px.histogram(f, x="release_year", nbins=30, title="Release Year Trend"), use_container_width=True)

    st.plotly_chart(px.bar(f.genre.value_counts().head(10), orientation="h", title="Top Genres"), use_container_width=True)

# ---------- Explorer ----------
elif page == "Explorer":
    st.title("🔎 Data Explorer")
    q = st.text_input("Search title / director / cast")
    d = f[f.title.str.contains(q, case=False, na=False) |
          f.director.astype(str).str.contains(q, case=False, na=False)] if q else f
    st.write(f"{len(d)} results")
    st.dataframe(d[["title", "type", "director", "country", "release_year", "rating"]], use_container_width=True)
    st.download_button("⬇️ Download CSV", d.to_csv(index=False), "netflix_filtered.csv")

# ---------- Hypothesis Test ----------
elif page == "Hypothesis Test":
    st.title("🧪 Hypothesis Testing")
    st.write("**H₀:** Movies and TV Shows are equally represented on Netflix.")
    obs = df.type.value_counts().values
    stat, p = chisquare(obs, f_exp=[obs.sum() / 2] * 2)
    c1, c2 = st.columns(2)
    c1.metric("Chi-square", f"{stat:,.2f}")
    c2.metric("P-value", f"{p:.2e}")
    st.success("Reject H₀ — Movies and TV Shows are NOT equally represented.") if p < 0.05 else st.info("Fail to reject H₀.")
    st.plotly_chart(px.bar(df.type.value_counts(), title="Observed Counts"), use_container_width=True)

# ---------- Certificate ----------
elif page == "Certificate":
    st.title("🎓 Internship Certificate")
    st.write("ApexPlanet Software Pvt. Ltd. - Data Analytics Internship")

    CERT = Path(r"C:\Users\David Chua\Desktop\ApexPlanet - INTERNSHIP\apex_planet_certificate.png")

    if CERT.exists():
        st.image(str(CERT), width="stretch")
    else:
        st.error("Certificate image not found!")