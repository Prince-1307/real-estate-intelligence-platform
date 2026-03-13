import streamlit as st
import pickle
import numpy as np
import pandas as pd
import os

# Load model

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

model_path = os.path.join(BASE_DIR, "price_model.pkl")
data_path = os.path.join(BASE_DIR, "data.pkl")

model = pickle.load(open(model_path, "rb"))
df = pickle.load(open(data_path, "rb"))


st.title("🏠 House Price Predictor")
st.write("Fill the property details below to estimate price")

# -------- INPUTS --------

property_type = st.selectbox(
    "Property Type",
    ["flat", "house"],
    index=None,
    placeholder="Select property type"
)

sector = st.selectbox(
    "Sector",
    sorted(df['sector'].unique()),
    index=None,
    placeholder="Select sector"
)

bedRoom = st.number_input(
    "Bedrooms",
    min_value=1,
    max_value=10,
    value=None,
    placeholder="Enter number of bedrooms"
)

bathroom = st.number_input(
    "Bathrooms",
    min_value=1,
    max_value=10,
    value=None,
    placeholder="Enter number of bathrooms"
)

balcony = st.selectbox(
    "Balcony",
    ["0", "1", "2", "3", "3+"],
    index=None,
    placeholder="Select balcony count"
)

agePossession = st.selectbox(
    "Property Age / Possession Status",
    [
        "Under Construction",
        "New Property",
        "Relatively New",
        "Moderately Old",
        "Old Property"
    ],
    index=None,
    placeholder="Select property age"
)

built_up_area = st.number_input(
    "Built Up Area (sqft)",
    min_value=200,
    value=None,
    placeholder="Enter built up area"
)

servant_room = st.selectbox(
    "Servant Room",
    ["No", "Yes"],
    index=None,
    placeholder="Select option"
)

store_room = st.selectbox(
    "Store Room",
    ["No", "Yes"],
    index=None,
    placeholder="Select option"
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
    index=None,
    placeholder="Select luxury category"
)

floor_category = st.selectbox(
    "Floor Category",
    ["low","mid","high"],
    index=None,
    placeholder="Select floor category"
)


# -------- PREDICTION --------
with st.container():

    if st.button("Predict Price"):

        if None in [property_type, sector, balcony, agePossession,
                furnishing_type, luxury_category, floor_category]:
            st.warning("Please fill all fields before predicting.")
        else:
            servant_room_value = 1 if servant_room == "Yes" else 0
            store_room_value = 1 if store_room == "Yes" else 0

            input_df = pd.DataFrame({
                "property_type":[property_type],
                "sector":[sector],
                "bedRoom":[bedRoom],
                "bathroom":[bathroom],
                "balcony":[balcony],
                "agePossession":[agePossession],
                "built_up_area":[built_up_area],
                "servant room":[servant_room_value],
                "store room":[store_room_value],
                "furnishing_type":[furnishing_type],
                "luxury_category":[luxury_category],
                "floor_category":[floor_category]
            })

            prediction = model.predict(input_df)

            price = np.expm1(prediction)[0]

            margin = 0.12   # 12%

            lower_price = price * (1 - margin)
            upper_price = price * (1 + margin)

            st.markdown(
            f"""
            <div style="
                background-color:#f5f7fa;
                padding:25px;
                border-radius:12px;
                text-align:center;
                border:1px solid #ddd;
            ">
                <h3 style="color:#555;">Estimated Property Price</h3>
                <h1 style="color:#2E8B57; font-size:48px;">
                    ₹ {price:.2f} Cr
                </h1>
                <p style="color:#777; font-size:18px;">
                    Expected Market Range
                </p>
                <h3 style="color:#444;">
                    ₹ {lower_price:.2f} Cr — ₹ {upper_price:.2f} Cr
                </h3>
            </div>
            """,
            unsafe_allow_html=True
            )