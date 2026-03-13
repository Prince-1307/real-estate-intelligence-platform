import streamlit as st

st.set_page_config(
    page_title="Real Estate Intelligence Platform",
    page_icon="🏠",
    layout="wide"
)

# ------------------------------
# Sidebar Design
# ------------------------------

with st.sidebar:

    st.title("🏠 Real Estate AI")

    st.divider()

    st.markdown("### 📌 Modules")

    st.markdown("💰 **Price Predictor**")
    st.caption("Estimate property prices")

    st.markdown("📊 **Market Analytics**")
    st.caption("Explore market trends")

    st.markdown("🏢 **Project Recommendations**")
    st.caption("Find similar projects")

    st.markdown("🔬 **Market Inference**")
    st.caption("Analyze feature impact")

    st.divider()

    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            width: 300px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# ------------------------------
# Header
# ------------------------------

st.title("🏠 Real Estate Intelligence Platform")

st.markdown(
"""
Welcome to the **Real Estate Intelligence Platform** — an AI-powered system designed to help users explore property markets, predict prices, and discover similar projects.

Use the modules on the **left sidebar** to explore different capabilities of the platform.
"""
)

st.divider()

# ------------------------------
# Feature Cards
# ------------------------------

col1, col2 = st.columns(2)

with col1:
    st.markdown(
    """
    ### 💰 Price Predictor

    Predict property prices using a machine learning model trained on real estate data.

    **Key Features**
    - Instant price prediction
    - Supports multiple property attributes
    - Provides price range estimates
    """
    )

with col2:
    st.markdown(
    """
    ### 📊 Market Analytics

    Explore insights and trends across different sectors and property types.

    **Key Features**
    - Sector-level insights
    - Price distribution analysis
    - Geographical visualization
    """
    )

col3, col4 = st.columns(2)

with col3:
    st.markdown(
    """
    ### 🏢 Project Recommendations

    Discover projects similar to a selected property using a recommendation system.

    **Key Features**
    - Content-based recommendations
    - Location & facility similarity
    - Project comparison
    """
    )

with col4:
    st.markdown(
    """
    ### 🔬 Market Inference

    Understand how different features affect property prices using what-if analysis.

    **Key Features**
    - Feature impact analysis
    - Price change simulation
    - Model explanation
    """
    )

st.divider()

# ------------------------------
# Footer
# ------------------------------

st.markdown(
"""
### 🚀 How to Use

1. Navigate through the modules using the **sidebar**.
2. Start with **Price Predictor** to estimate property value.
3. Use **Market Analytics** to explore data insights.
4. Discover similar projects in **Project Recommendations**.
5. Experiment with **Market Inference** to analyze price changes.

---

Built using **Python, Machine Learning, and Streamlit**.
"""
)