import pandas as pd
import streamlit as st
import plotly.express as px
from scipy.stats import chisquare
from pathlib import Path

st.set_page_config(
    page_title="Netflix Content Analysis | Yeturi Venu Gopal",
    page_icon="🎬",
    layout="wide"
)

# Created by
st.markdown(
    """
    <div style="text-align:center;">
        <h3>Created by — Yeturi Venu Gopal</h3>
    </div>
    """,
    unsafe_allow_html=True
)

DATA = Path(__file__).parent / "data" / "cleaned_dataset.csv"
CERT = Path(__file__).parent / "assets" / "certificate.png"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA)

    df["country"] = (
        df["country"]
        .fillna("Unknown")
        .astype(str)
        .apply(lambda x: x.split(",")[0].strip())
    )

    df["genre"] = (
        df["listed_in"]
        .fillna("Unknown")
        .astype(str)
        .apply(lambda x: x.split(",")[0].strip())
    )

    df["rating"] = df["rating"].fillna(
        df["rating"].mode()[0]
    )

    return df


df = load_data()

elif page == "Certificate":

    st.title("🎓 Internship Certificate")

    st.write(
        "ApexPlanet Software Pvt. Ltd. — Data Analytics Internship"
    )

    st.markdown("### 👨‍💻 Created By")
    st.markdown("## **Yeturi Venu Gopal**")

    st.markdown("---")

    if CERT.exists():
        st.image(
            str(CERT),
            width="stretch"
        )
    else:
        st.error("Certificate image not found!")
