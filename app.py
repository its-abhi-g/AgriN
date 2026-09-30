import time

import streamlit as st

from services.gemini_service import analyze_farm_problem
from utils.demo_data import DEMO_SCENARIOS, DEMO_INSIGHTS


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AgriN - Agricultural Intelligence Network",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# STYLES
# --------------------------------------------------

st.markdown(
    """
    <style>

    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    .agrin-logo {
        font-size: 28px;
        font-weight: 800;
        color: #17351F;
        margin-bottom: 4px;
    }

    .hero {
        padding: 45px 10px 35px 0;
    }

    .hero-title {
        font-size: 52px;
        line-height: 1.05;
        font-weight: 800;
        color: #17351F;
    }

    .green-text {
        color: #2E7D32;
    }

    .hero-subtitle {
        color: #667085;
        font-size: 19px;
        max-width: 680px;
        margin-top: 18px;
    }

    .small-label {
        color: #2E7D32;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1px;
    }

    .agrin-card {
        background: white;
        border: 1px solid #E1E8DF;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0px 2px 8px rgba(23,53,31,0.04);
    }

    .result-title {
        font-weight: 800;
        font-size: 19px;
        color: #17351F;
        margin-bottom: 10px;
    }

    .risk-low {
        color: #166534;
        background: #DCFCE7;
    }

    .risk-moderate {
        color: #854D0E;
        background: #FEF9C3;
    }

    .risk-high {
        color: #9A3412;
        background: #FFEDD5;
    }

    .risk-critical {
        color: #991B1B;
        background: #FEE2E2;
    }

    .risk {
        display: inline-block;
        font-weight: 800;
        padding: 6px 12px;
        border-radius: 999px;
    }

    .disclaimer {
        color: #667085;
        font-size: 13px;
        padding: 15px;
        background: #F2F5F1;
        border-radius: 12px;
        margin-top: 25px;
    }

    @media (max-width: 700px) {

        .hero-title {
            font-size: 38px;
        }

        .hero {
            padding-top: 20px;
        }

    }

    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

DEFAULTS = {
    "query": "",
    "state": "",
    "district": "",
    "crop": "Not specified",
    "crop_stage": "Not specified",
    "irrigation": "Not specified",
    "analysis_result": None,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def risk_html(risk):
    css_name = {
        "LOW": "risk-low",
        "MODERATE": "risk-moderate",
        "HIGH": "risk-high",
        "CRITICAL": "risk-critical",
    }.get(risk, "risk-moderate")

    return (
        f'<span class="risk {css_name}">'
        f'{risk}'
        f'</span>'
    )


def load_demo(example_name):
    demo = DEMO_SCENARIOS.get(example_name)

    if not demo:
        return

    st.session_state.query = demo["query"]
    st.session_state.state = demo["state"]
    st.session_state.district = demo["district"]
    st.session_state.crop = demo["crop"]
    st.session_state.crop_stage = demo["stage"]
    st.session_state.irrigation = demo["irrigation"]


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown(
        '<div class="agrin-logo">🌱 AgriN</div>',
        unsafe_allow_html=True,
    )

    st.caption("Agricultural Intelligence Network")

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Home",
            "🌾 Ask AgriN",
            "📊 Insights",
            "ℹ️ About",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    language = st.selectbox(
        "Language",
        [
            "Auto Detect",
            "English",
            "हिन्दी",
        ],
    )

    demo_mode = st.toggle(
        "Demo Mode",
        value=True,
        help="Enables quick hackathon demonstration scenarios.",
    )

    if demo_mode:
        st.caption(
            "🧪 Demonstration information is clearly "
            "marked and is not a real farmer record."
        )


# --------------------------------------------------
# HOME
# --------------------------------------------------

if page == "🏠 Home":

    st.markdown(
    """
<div class="hero">
<div class="small-label">AI-ASSISTED FARM DECISIONS</div>
<div class="hero-title">
Smarter Decisions.<br>
<span class="green-text">Stronger Farms.</span>
</div>
<div class="hero-subtitle">
AI-powered agricultural intelligence that understands your farm,
your crop, and your challenges.
</div>
</div>
    """,
    unsafe_allow_html=True,
)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="agrin-card">
                <div class="small-label">01</div>
                <h3>Understand</h3>
                <p>
                    Tell AgriN what's happening
                    on your farm.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="agrin-card">
                <div class="small-label">02</div>
                <h3>Analyse</h3>
                <p>
                    Gemini evaluates your crop
                    and farming context.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="agrin-card">
                <div class="small-label">03</div>
                <h3>Act</h3>
                <p>
                    Get simple, practical
                    next steps.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.info(
        "👈 Select **Ask AgriN** from the sidebar "
        "to analyze a farming problem."
    )


# --------------------------------------------------
# ASK AGRIN
# --------------------------------------------------

elif page == "🌾 Ask AgriN":

    st.title(
        "🌾 What's happening on your farm?"
    )

    st.caption(
        "Describe the problem naturally. "
        "You don't need agricultural terminology."
    )

    # ----------------------------------------------
    # DEMO SCENARIOS
    # ----------------------------------------------

    if demo_mode:

        st.markdown("### 🧪 Try an example")

        example = st.selectbox(
            "Demo scenario",
            list(DEMO_SCENARIOS.keys()),
        )

        if st.button(
            "Load demonstration",
            use_container_width=True,
        ):
            load_demo(example)
            st.rerun()

        st.caption(
            "Demonstration input only. "
            "This is not a real farmer record."
        )

    st.divider()

    # ----------------------------------------------
    # TEXT INPUT
    # ----------------------------------------------

    st.markdown("### 💬 Tell AgriN your problem")

    query = st.text_area(
        "Farmer question",
        key="query",
        height=140,
        placeholder=(
            "Example: My wheat leaves are turning yellow "
            "during early growth. What should I check?"
        ),
        label_visibility="collapsed",
    )

    st.caption(
        "You can write naturally in English or हिन्दी."
    )

    # ----------------------------------------------
    # FARM CONTEXT
    # ----------------------------------------------

    with st.expander(
        "📍 Add farm context (optional)",
        expanded=True,
    ):

        location_col1, location_col2 = st.columns(2)

        with location_col1:
            st.text_input(
                "State",
                key="state",
                placeholder="e.g. Uttar Pradesh",
            )

        with location_col2:
            st.text_input(
                "District",
                key="district",
                placeholder="e.g. Lucknow",
            )

        field1, field2 = st.columns(2)

        crops = [
            "Not specified",
            "Wheat",
            "Rice",
            "Mustard",
            "Sugarcane",
            "Cotton",
            "Maize",
            "Potato",
            "Other",
        ]

        stages = [
            "Not specified",
            "Sowing",
            "Germination",
            "Vegetative Growth",
            "Flowering",
            "Fruiting",
            "Harvest Ready",
            "Unknown",
        ]

        irrigation_options = [
            "Not specified",
            "Available",
            "Limited",
            "Rain-fed",
            "Unknown",
        ]

        with field1:

            st.selectbox(
                "Crop",
                crops,
                key="crop",
            )

        with field2:

            st.selectbox(
                "Crop Stage",
                stages,
                key="crop_stage",
            )

        st.selectbox(
            "Irrigation",
            irrigation_options,
            key="irrigation",
        )

    # ----------------------------------------------
    # ANALYZE
    # ----------------------------------------------

    analyze_button = st.button(
        "🌱 Analyze my farm problem",
        type="primary",
        use_container_width=True,
    )

    if analyze_button:

        if len(query.strip()) < 8:

            st.warning()