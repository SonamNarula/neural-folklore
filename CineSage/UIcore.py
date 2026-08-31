import streamlit as st
from core import get_movie_info


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="CineSage — Movie Intelligence",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* =========================
       GLOBAL
    ========================= */

    .stApp {
        background:
            radial-gradient(
                circle at 15% 10%,
                rgba(255, 0, 76, 0.12),
                transparent 30%
            ),
            radial-gradient(
                circle at 85% 15%,
                rgba(120, 50, 255, 0.12),
                transparent 30%
            ),
            #08080c;
        color: #f5f5f7;
    }

    .main {
        padding-top: 1rem;
    }

    /* =========================
       SIDEBAR
       ========================= */

    section[data-testid="stSidebar"] {
        background: #0d0d12;
        border-right: 1px solid rgba(255,255,255,0.07);
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 2rem;
    }

    .sidebar-logo {
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 0.2rem;
    }

    .sidebar-tagline {
        color: #8d8d98;
        font-size: 0.85rem;
        margin-bottom: 2rem;
    }

    .sidebar-card {
        background: rgba(255,255,255,0.035);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 14px;
        padding: 1rem;
        margin-top: 1rem;
    }

    .sidebar-card-title {
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .sidebar-card-text {
        color: #9999a5;
        font-size: 0.82rem;
        line-height: 1.6;
    }


    /* =========================
       HERO
       ========================= */

    .hero {
        text-align: center;
        padding: 3.5rem 1rem 2rem 1rem;
    }

    .hero-badge {
        display: inline-block;
        padding: 0.4rem 0.9rem;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.055);
        border: 1px solid rgba(255,255,255,0.09);
        color: #b8b8c3;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-bottom: 1rem;
    }

    .hero-title {
        font-size: clamp(3rem, 7vw, 6rem);
        line-height: 0.95;
        font-weight: 900;
        letter-spacing: -5px;
        margin: 0;
        background: linear-gradient(
            90deg,
            #ffffff,
            #ff3b75,
            #a46cff
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        color: #9b9ba6;
        font-size: 1.05rem;
        max-width: 650px;
        margin: 1.3rem auto 0 auto;
        line-height: 1.7;
    }


    /* =========================
       SEARCH AREA
       ========================= */

    .search-label {
        text-align: center;
        color: #aaaab5;
        font-size: 0.85rem;
        margin-bottom: 0.6rem;
    }

    div[data-testid="stTextInput"] input {
        background: #111116 !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 14px !important;
        color: white !important;
        font-size: 1rem !important;
        padding: 1rem !important;
    }

    div[data-testid="stTextInput"] input:focus {
        border-color: #ff3b75 !important;
        box-shadow: 0 0 0 1px #ff3b75 !important;
    }

    div[data-testid="stTextInput"] label {
        display: none;
    }

    /* =========================
       BUTTON
       ========================= */

    div.stButton > button {
        width: 100%;
        height: 54px;
        border: none;
        border-radius: 14px;
        background: linear-gradient(
            135deg,
            #ff2f68,
            #a34cff
        );
        color: white;
        font-weight: 800;
        font-size: 0.95rem;
        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow:
            0 10px 30px rgba(255,47,104,0.22);
    }


    /* =========================
       FEATURE CARDS
       ========================= */

    .feature-card {
        background: rgba(255,255,255,0.035);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 18px;
        padding: 1.4rem;
        height: 100%;
        transition: 0.2s ease;
    }

    .feature-icon {
        font-size: 1.7rem;
        margin-bottom: 0.7rem;
    }

    .feature-title {
        font-size: 1rem;
        font-weight: 750;
        margin-bottom: 0.35rem;
    }

    .feature-text {
        color: #8f8f9b;
        font-size: 0.82rem;
        line-height: 1.55;
    }


    /* =========================
       REPORT
       ========================= */

    .report-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }

    .report-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: #ff3b75;
        box-shadow: 0 0 18px rgba(255,59,117,0.7);
    }

    .report-title {
        font-size: 1.4rem;
        font-weight: 800;
    }

    .report-container {
        background: rgba(255,255,255,0.025);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 2rem;
    }


    /* =========================
       MARKDOWN
       ========================= */

    .report-container h1 {
        font-size: 2.3rem;
        font-weight: 850;
        margin-bottom: 1.5rem;
    }

    .report-container h2 {
        font-size: 1.35rem;
        margin-top: 2rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(255,255,255,0.07);
    }

    .report-container h3 {
        font-size: 1.05rem;
        margin-top: 1.3rem;
    }

    .report-container p,
    .report-container li {
        color: #c2c2ca;
        line-height: 1.75;
    }

    .report-container strong {
        color: #ffffff;
    }


    /* =========================
       FOOTER
       ========================= */

    .footer {
        text-align: center;
        color: #5e5e68;
        font-size: 0.75rem;
        padding: 3rem 0 1rem 0;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-logo">🎬 CineSage</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-tagline">'
        'AI-powered movie intelligence'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("### 🧭 What CineSage does")

    st.markdown(
        """
        <div class="sidebar-card">
            <div class="sidebar-card-title">
                🔎 Research
            </div>
            <div class="sidebar-card-text">
                Extract detailed information about movies,
                cast, crew, story, reception and more.
            </div>
        </div>

        <div class="sidebar-card">
            <div class="sidebar-card-title">
                🧠 Analyze
            </div>
            <div class="sidebar-card-text">
                Understand themes, cinematic style,
                strengths and weaknesses.
            </div>
        </div>

        <div class="sidebar-card">
            <div class="sidebar-card-title">
                ⭐ Evaluate
            </div>
            <div class="sidebar-card-text">
                Get a clear CineSage verdict based on
                the movie's overall qualities.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.caption("Powered by Mistral AI")
    st.caption("Built with Python + LangChain + Streamlit")


# =========================================================
# HERO
# =========================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-badge">
            ✦ AI MOVIE INTELLIGENCE
        </div>

        <h1 class="hero-title">
            CineSage
        </h1>

        <p class="hero-subtitle">
            Discover movies beyond the rating.
            Explore the story, cast, crew, themes,
            reception, box office and cinematic soul —
            all in one intelligent report.
        </p>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SEARCH
# =========================================================

st.markdown(
    '<div class="search-label">What movie are you curious about?</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns([4, 1], gap="medium")

with col1:

    movie_name = st.text_input(
        "Movie",
        placeholder="e.g. Interstellar, Inception, 3 Idiots...",
        label_visibility="collapsed"
    )

with col2:

    generate = st.button(
        "✨ Analyze Movie"
    )


# =========================================================
# FEATURE SECTION
# =========================================================

if "movie_report" not in st.session_state:

    st.markdown("<br>", unsafe_allow_html=True)

    f1, f2, f3 = st.columns(3, gap="medium")

    with f1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🎭</div>
                <div class="feature-title">
                    Cast & Crew
                </div>
                <div class="feature-text">
                    Explore actors, characters, directors,
                    writers, producers and key creatives.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with f2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🧠</div>
                <div class="feature-title">
                    Deep Analysis
                </div>
                <div class="feature-text">
                    Understand themes, filmmaking,
                    performances, music and cinematic style.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with f3:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <div class="feature-title">
                    Movie Intelligence
                </div>
                <div class="feature-text">
                    Get reception, box office,
                    awards and a final CineSage verdict.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# GENERATE REPORT
# =========================================================

if generate:

    if not movie_name.strip():

        st.warning(
            "🎬 Enter a movie name first."
        )

    else:

        with st.spinner(
            "🎥 CineSage is researching the movie..."
        ):

            try:

                report = get_movie_info(
                    movie_name.strip()
                )

                st.session_state.movie_report = report
                st.session_state.movie_name = movie_name.strip()

            except Exception as e:

                st.error(
                    f"Something went wrong: {e}"
                )


# =========================================================
# DISPLAY REPORT
# =========================================================

if "movie_report" in st.session_state:

    st.markdown(
        """
        <div class="report-header">
            <div class="report-dot"></div>
            <div class="report-title">
                CineSage Intelligence Report
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="report-container">',
        unsafe_allow_html=True
    )

    st.markdown(
        st.session_state.movie_report
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    # =====================================================
    # ACTIONS
    # =====================================================

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:

        if st.button(
            "🔄 Analyze Another Movie",
            use_container_width=True
        ):

            st.session_state.pop(
                "movie_report",
                None
            )

            st.session_state.pop(
                "movie_name",
                None
            )

            st.rerun()

    with c2:

        st.download_button(
            "📄 Download Report",
            data=st.session_state.movie_report,
            file_name=(
                f"{st.session_state.movie_name}"
                ".md"
            ),
            mime="text/markdown",
            use_container_width=True
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        CineSage · AI Movie Intelligence ·
        Built with LangChain + Mistral + Streamlit
    </div>
    """,
    unsafe_allow_html=True
)