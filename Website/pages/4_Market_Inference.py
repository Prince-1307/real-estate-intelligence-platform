import streamlit as st
import pickle
import pandas as pd
import numpy as np
import plotly.express as px

# Load files
pipeline = pickle.load(open("price_model.pkl","rb"))
feature_importance = pickle.load(open("feature_importance.pkl","rb"))
df = pickle.load(open("data.pkl","rb"))

st.title("🔬 Market Inference Engine")

st.caption(
"Understand how property attributes influence price using model-based what-if analysis."
)

# ------------------------------
# Base Property Inputs
# ------------------------------

st.subheader("🏠 Base Property Profile")

col1, col2 = st.columns(2)

with col1:

    property_type = st.selectbox(
        "Property Type",
        ["flat","house"],
        index=None,
        placeholder="Select property type"
    )

    sector = st.selectbox(
        "Sector",
        sorted(df['sector'].unique()),
        index=None,
        placeholder="Select sector"
    )

    bedRoom = st.slider("Bedrooms",1,10,3)

    bathroom = st.slider("Bathrooms",1,10,3)

    balcony = st.selectbox("Balcony",["0","1","2","3","3+"],index=None)

with col2:

    built_up_area = st.number_input(
        "Built-up Area (sqft)",
        min_value=200,
        value=None,
        placeholder="Enter area"
    )

    agePossession = st.selectbox(
        "Property Age",
        [
            "Under Construction",
            "New Property",
            "Relatively New",
            "Moderately Old",
            "Old Property"
        ],
        index=None,
        placeholder="Select age category"
    )

    furnishing_type = st.selectbox(
        "Furnishing",
        ["unfurnished","semi-furnished","furnished"],
        index=None,
        placeholder="Select furnishing type"
    )

    luxury_category = st.selectbox(
        "Luxury Category",
        ["low","medium","high"],
        index=None
    )

    floor_category = st.selectbox(
        "Floor Category",
        ["low","mid","high"],
        index=None
    )

servant_room = st.selectbox("Servant Room",["No","Yes"])
store_room = st.selectbox("Store Room",["No","Yes"])

# Convert to numeric
servant_room_val = 1 if servant_room=="Yes" else 0
store_room_val = 1 if store_room=="Yes" else 0

# ------------------------------
# Create Input DataFrame
# ------------------------------

if None not in [
property_type, sector, balcony,
agePossession, furnishing_type,
luxury_category, floor_category
]:

    input_df = pd.DataFrame({
    "property_type":[property_type],
    "sector":[sector],
    "bedRoom":[bedRoom],
    "bathroom":[bathroom],
    "balcony":[balcony],
    "agePossession":[agePossession],
    "built_up_area":[built_up_area],
    "servant room":[servant_room_val],
    "store room":[store_room_val],
    "furnishing_type":[furnishing_type],
    "luxury_category":[luxury_category],
    "floor_category":[floor_category]
    })

    base_price = np.expm1(pipeline.predict(input_df))[0]

    st.markdown(
    f"""
    <div style="
    background-color:#f7f9fc;
    padding:20px;
    border-radius:10px;
    border:1px solid #ddd;
    text-align:center;
    ">
    <h4>Base Price Prediction</h4>
    <h2 style="color:#2E8B57;">₹ {base_price:.2f} Cr</h2>
    </div>
    """,
    unsafe_allow_html=True
    )

    # ------------------------------
    # What If Section
    # ------------------------------

    st.subheader("🔁 What-If Scenario")

    feature_to_modify = st.selectbox(
    "Choose Feature to Modify",
    [
    "sector",
    "property_type",
    "bedRoom",
    "agePossession",
    "furnishing_type",
    "luxury_category",
    "floor_category"
    ]
    )

    new_value = None

    if feature_to_modify == "sector":
        new_value = st.selectbox(
        "New Sector",
        sorted(df['sector'].unique())
        )

    elif feature_to_modify == "property_type":
        new_value = st.selectbox(
        "New Property Type",
        ["flat","house"]
        )

    elif feature_to_modify == "bedRoom":
        new_value = st.slider("Bedrooms",1,10,3)

    elif feature_to_modify == "agePossession":
        new_value = st.selectbox(
        "New Age Category",
        [
        "Under Construction",
        "New Property",
        "Relatively New",
        "Moderately Old",
        "Old Property"
        ]
        )

    elif feature_to_modify == "furnishing_type":
        new_value = st.selectbox(
        "New Furnishing",
        ["unfurnished","semi-furnished","furnished"]
        )

    elif feature_to_modify == "luxury_category":
        new_value = st.selectbox(
        "New Luxury Category",
        ["low","medium","high"]
        )

    elif feature_to_modify == "floor_category":
        new_value = st.selectbox(
        "New Floor Category",
        ["low","mid","high"]
        )

    # ------------------------------
    # Run What If
    # ------------------------------

    if new_value is not None:

        modified_df = input_df.copy()
        modified_df[feature_to_modify] = new_value

        new_price = np.expm1(pipeline.predict(modified_df))[0]

        change = ((new_price-base_price)/base_price)*100

        c1,c2 = st.columns(2)

        with c1:
            st.metric("Base Price",f"₹ {base_price:.2f} Cr")

        with c2:
            st.metric(
            "Modified Price",
            f"₹ {new_price:.2f} Cr",
            f"{change:.2f}%"
            )

# ------------------------------
# Feature Importance Chart
# ------------------------------

st.subheader("Feature Impact Ranking")

feature_importance['importance_pct'] = (
                feature_importance['importance'] / feature_importance['importance'].sum()
                )*100

top_feature = feature_importance.iloc[0]

st.info(
f"📊 The most influential feature is **{top_feature['feature']}**, "
f"contributing **{top_feature['importance_pct']:.1f}%** to price predictions."
)

top_features = feature_importance.head(8)

fig = px.bar(
    top_features,
    x="importance_pct",
    y="feature",
    orientation="h",
    text="importance_pct",
    title="🏆 Feature Impact Leaderboard",
    color="importance_pct",
    color_continuous_scale="viridis"
)

fig.update_layout(
    xaxis_title="Impact on Price (%)",
    yaxis_title="Property Features",
    title_font_size=22,
    xaxis_title_font_size=16,
    yaxis_title_font_size=16,
    coloraxis_showscale=False
)

fig.update_traces(
    texttemplate='%{text:.1f}%',
    textposition='outside'
)

fig.update_layout(
    yaxis=dict(autorange="reversed")
)

st.plotly_chart(fig,use_container_width=True)