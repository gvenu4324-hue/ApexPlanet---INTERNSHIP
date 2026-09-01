import pandas as pd
import streamlit as st
import plotly.express as px
from scipy.stats import chisquare
from pathlib import Path

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Netflix Content Analysis | Yeturi Venu Gopal",
    page_icon="🎬",
    layout="wide"
)

# ============================================================
# CREATED BY - TOP OF WEBSITE
# ============================================================

st.markdown(
    """
    <div style="text-align: center; padding: 5px 0 10px 0;">
        <h3>Created by — Yeturi Venu Gopal</h3>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ============================================================
# FILE PATHS
# ============================================================

BASE_DIR = Path(__file__).parent

DATA = BASE_DIR / "Task-1-DATA IMMERSION AND WRANGLING" / "netflix_titles_cleaned.csv"

CERT = BASE_DIR / "apex_planet_certificate.png"

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    df = pd.read_csv(DATA)

    # Clean country
    if "country" in df.columns:
        df["country"] = (
            df["country"]
            .fillna("Unknown")
            .astype(str)
            .apply(lambda x: x.split(",")[0].strip())
        )

    # Clean genre
    if "listed_in" in df.columns:
        df["genre"] = (
            df["listed_in"]
            .fillna("Unknown")
            .astype(str)
            .apply(lambda x: x.split(",")[0].strip())
        )
    else:
        df["genre"] = "Unknown"

    # Clean rating
    if "rating" in df.columns:
        mode_value = df["rating"].mode()

        if not mode_value.empty:
            df["rating"] = df["rating"].fillna(mode_value[0])
        else:
            df["rating"] = df["rating"].fillna("Unknown")

    # Clean director
    if "director" in df.columns:
        df["director"] = df["director"].fillna("Unknown")

    # Clean cast
    if "cast" in df.columns:
        df["cast"] = df["cast"].fillna("Not Available")

    return df


# Load dataset
try:
    df = load_data()
except Exception as e:
    st.error("❌ Unable to load the dataset.")
    st.error(f"Please check that this file exists: {DATA}")
    st.stop()

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🎬 Netflix Analysis")

st.sidebar.caption(
    "Created by Yeturi Venu Gopal"
)

page = st.sidebar.radio(
    "Go to",
    [
        "Overview",
        "Dashboard",
        "Explorer",
        "Hypothesis Test",
        "Certificate"
    ]
)

# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.markdown("---")
st.sidebar.subheader("🔎 Filters")

types = st.sidebar.multiselect(
    "Content Type",
    options=df["type"].dropna().unique(),
    default=list(df["type"].dropna().unique())
)

min_year = int(df["release_year"].min())
max_year = int(df["release_year"].max())

default_start = max(min_year, 2015)
default_end = min(max_year, 2021)

if default_start > default_end:
    default_start = min_year
    default_end = max_year

years = st.sidebar.slider(
    "Release Year",
    min_value=min_year,
    max_value=max_year,
    value=(default_start, default_end)
)

# Apply filters
f = df[
    df["type"].isin(types)
    & df["release_year"].between(years[0], years[1])
]

# ============================================================
# OVERVIEW
# ============================================================

if page == "Overview":

    st.title("🎬 Netflix Movies & TV Shows Analysis")

    st.subheader(
        "ApexPlanet Software Pvt. Ltd. — Data Analytics Internship"
    )

    st.markdown(
        """
        This project analyzes the Netflix Movies and TV Shows dataset
        using Python, Pandas, Plotly, Statistics, and Streamlit.
        """
    )

    # Metrics
    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Total Titles",
        f"{len(df):,}"
    )

    c2.metric(
        "Movies",
        f"{(df['type'] == 'Movie').sum():,}"
    )

    c3.metric(
        "TV Shows",
        f"{(df['type'] == 'TV Show').sum():,}"
    )

    st.markdown("### 📌 Key Insights")

    st.markdown(
        """
        - 🎥 **Movies** make up approximately 70% of all content.
        - 🇺🇸 **USA** leads content production, followed by India.
        - 🔞 **TV-MA** is the most common rating.
        - 📈 Content additions peaked around **2018–2019**.
        """
    )

    st.markdown("### 📊 Dataset Preview")

    st.dataframe(
        df.head(10),
        use_container_width=True
    )

# ============================================================
# DASHBOARD
# ============================================================

elif page == "Dashboard":

    st.title("📊 Netflix Dashboard")

    st.caption(
        f"Showing {len(f):,} titles based on the selected filters."
    )

    # --------------------------------------------------------
    # Movies vs TV Shows
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        type_counts = (
            f["type"]
            .value_counts()
            .reset_index()
        )

        type_counts.columns = [
            "type",
            "count"
        ]

        fig1 = px.bar(
            type_counts,
            x="type",
            y="count",
            title="🎬 Movies vs TV Shows",
            text="count"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    # --------------------------------------------------------
    # Top Countries
    # --------------------------------------------------------

    with col2:

        country_counts = (
            f["country"]
            .value_counts()
            .head(10)
            .reset_index()
        )

        country_counts.columns = [
            "country",
            "count"
        ]

        fig2 = px.bar(
            country_counts,
            x="country",
            y="count",
            title="🌎 Top 10 Countries",
            text="count"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    # --------------------------------------------------------
    # Ratings
    # --------------------------------------------------------

    col3, col4 = st.columns(2)

    with col3:

        rating_counts = (
            f["rating"]
            .value_counts()
            .reset_index()
        )

        rating_counts.columns = [
            "rating",
            "count"
        ]

        fig3 = px.bar(
            rating_counts,
            x="rating",
            y="count",
            title="🔞 Ratings Distribution",
            text="count"
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

    # --------------------------------------------------------
    # Release Year
    # --------------------------------------------------------

    with col4:

        year_counts = (
            f["release_year"]
            .value_counts()
            .sort_index()
            .reset_index()
        )

        year_counts.columns = [
            "release_year",
            "count"
        ]

        fig4 = px.line(
            year_counts,
            x="release_year",
            y="count",
            title="📈 Release Year Trend",
            markers=True
        )

        st.plotly_chart(
            fig4,
            use_container_width=True
        )

    # --------------------------------------------------------
    # Top Genres
    # --------------------------------------------------------

    st.markdown("### 🎭 Top Genres")

    genre_counts = (
        f["genre"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    genre_counts.columns = [
        "genre",
        "count"
    ]

    fig5 = px.bar(
        genre_counts,
        x="count",
        y="genre",
        orientation="h",
        title="Top 10 Genres",
        text="count"
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )

# ============================================================
# EXPLORER
# ============================================================

elif page == "Explorer":

    st.title("🔎 Data Explorer")

    st.write(
        "Search for a movie or TV show by title, director, or cast."
    )

    q = st.text_input(
        "🔍 Search title / director / cast"
    )

    d = f.copy()

    if q:

        title_match = (
            d["title"]
            .astype(str)
            .str.contains(
                q,
                case=False,
                na=False
            )
        )

        director_match = (
            d["director"]
            .astype(str)
            .str.contains(
                q,
                case=False,
                na=False
            )
        )

        cast_match = (
            d["cast"]
            .astype(str)
            .str.contains(
                q,
                case=False,
                na=False
            )
        )

        d = d[
            title_match
            | director_match
            | cast_match
        ]

    st.write(
        f"### 📌 {len(d):,} results found"
    )

    columns_to_show = [
        "title",
        "type",
        "director",
        "country",
        "release_year",
        "rating"
    ]

    st.dataframe(
        d[columns_to_show],
        use_container_width=True,
        height=500
    )

    # Download
    csv = d.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "⬇️ Download Filtered CSV",
        csv,
        "netflix_filtered.csv",
        "text/csv"
    )

# ============================================================
# HYPOTHESIS TEST
# ============================================================

elif page == "Hypothesis Test":

    st.title("🧪 Hypothesis Testing")

    st.markdown("### Research Question")

    st.write(
        "Is there a statistically significant difference between "
        "the number of Movies and TV Shows on Netflix?"
    )

    st.markdown("### 📝 Hypotheses")

    st.write(
        "**H₀ (Null Hypothesis):** "
        "Movies and TV Shows are equally represented on Netflix."
    )

    st.write(
        "**H₁ (Alternative Hypothesis):** "
        "Movies and TV Shows are NOT equally represented on Netflix."
    )

    # Counts
    movie_count = int(
        (df["type"] == "Movie").sum()
    )

    tv_count = int(
        (df["type"] == "TV Show").sum()
    )

    observed = [
        movie_count,
        tv_count
    ]

    total = sum(observed)

    expected = [
        total / 2,
        total / 2
    ]

    # Chi-square test
    stat, p = chisquare(
        observed,
        f_exp=expected
    )

    # Metrics
    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Chi-square",
        f"{stat:,.2f}"
    )

    c2.metric(
        "P-value",
        f"{p:.2e}"
    )

    c3.metric(
        "Significance Level",
        "0.05"
    )

    st.markdown("### 📊 Test Result")

    if p < 0.05:

        st.success(
            f"""
            ✅ Reject H₀.

            The p-value ({p:.2e}) is less than 0.05.

            Therefore, there is a statistically significant
            difference between the number of Movies and TV Shows.
            """
        )

    else:

        st.info(
            f"""
            Fail to reject H₀.

            The p-value ({p:.2e}) is greater than or equal to 0.05.
            """
        )

    # Chart
    observed_df = pd.DataFrame(
        {
            "Type": [
                "Movie",
                "TV Show"
            ],
            "Count": observed
        }
    )

    fig6 = px.bar(
        observed_df,
        x="Type",
        y="Count",
        title="Observed Movie vs TV Show Counts",
        text="Count"
    )

    st.plotly_chart(
        fig6,
        use_container_width=True
    )

# ============================================================
# CERTIFICATE
# ============================================================

elif page == "Certificate":

    st.title("🎓 Internship Certificate")

    st.write(
        "ApexPlanet Software Pvt. Ltd. — Data Analytics Internship"
    )

    st.markdown("### 👨‍💻 Created By")

    st.markdown(
        "## **Yeturi Venu Gopal**"
    )

    st.markdown("---")

    if CERT.exists():

        st.image(
            str(CERT),
            use_container_width=True
        )

    else:

        st.error(
            "❌ Certificate image not found!"
        )

        st.info(
            "Please place certificate.png inside the assets folder."
        )

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; padding:10px;">
        <small>
            Created by <b>Yeturi Venu Gopal</b> |
            Netflix Content Analysis |
            ApexPlanet Data Analytics Internship
        </small>
    </div>
    """,
    unsafe_allow_html=True
)
