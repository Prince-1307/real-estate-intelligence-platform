import streamlit as st
import pandas as pd
import pickle
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.express as px

Analytics_df = pickle.load(open("analytics_data.pkl", "rb"))
feature_counts = pickle.load(open("feature_wordcount.pkl", "rb"))

st.title("📊 Real Estate Market Analytics")

st.write("Explore property market trends and insights.")

# Top Metrics -----------

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Listings", len(Analytics_df))

col2.metric(
    "Median Price/Sqft",
    f"{Analytics_df['price_per_sqft'].median():,.0f}"
)

col3.metric(
    "Avg Area",
    f"{Analytics_df['built_up_area'].mean():,.0f} sqft"
)

premium_sector = Analytics_df.groupby("sector")["price_per_sqft"].mean().idxmax()

col4.metric("Premium Sector", premium_sector)

# Dashboard Tabs-----------

tab1, tab2, tab3, tab4 = st.tabs([
    "Market Overview",
    "Location Insights",
    "Property Insights",
    "Amenities Analysis"
])


# Market Overview Tab-----------

with tab1:

    st.subheader("Price per Sqft Distribution")

    fig, ax = plt.subplots()

    sns.histplot(
        Analytics_df["price_per_sqft"],
        bins=50,
        kde=True,
        ax=ax
    )

    st.pyplot(fig)


    st.subheader("Area vs Price per Sqft")

    fig, ax = plt.subplots()

    sns.scatterplot(
        data=Analytics_df,
        x="built_up_area",
        y="price_per_sqft",
        alpha=0.6,
        ax=ax
    )

    st.pyplot(fig)


# Location Insights Tab-----------

with tab2:

    st.subheader("Property Locations")

    fig = px.scatter_mapbox(
        Analytics_df,
        lat="latitude",
        lon="longitude",
        color="price_per_sqft",
        size="price",
        hover_name="sector",
        zoom=10,
        height=600,
        width=600,
        color_continuous_scale="Turbo"
    )

    fig.update_layout(mapbox_style="open-street-map")

    st.plotly_chart(fig)

    sector = st.selectbox(
        "Select Sector",
        sorted(Analytics_df["sector"].unique())
    )

    sector_df = Analytics_df[Analytics_df["sector"] == sector]

    if len(sector_df) < 5:
        st.info("Limited data available for this sector.")
    
    else:

        st.subheader("Property Locations")

        st.map(sector_df[['latitude','longitude']])

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Properties Listed",
            len(sector_df)
        )

        col2.metric(
            "Avg Price",
            f"{sector_df['price'].mean():.2f} Cr"
        )

        col3.metric(
            "Avg Price/Sqft",
            f"{sector_df['price_per_sqft'].mean():,.0f}"
        )

        st.subheader("Price Distribution in Selected Sector")

        fig, ax = plt.subplots()

        sns.histplot(
            sector_df["price"],
            bins=20,
            kde=True,
            ax=ax
        )

        st.pyplot(fig)

        st.subheader("BHK Distribution")

        bhk_counts = sector_df["bedRoom"].value_counts().sort_index()

        st.bar_chart(bhk_counts)





    st.subheader("Average Price per Sqft by Sector")

    sector_price = Analytics_df.groupby("sector")["price_per_sqft"].mean().sort_values(ascending=False)

    st.bar_chart(sector_price.head(15))



with tab3:

    st.subheader("Sector vs BHK Distribution")

    # Create pivot table
    heatmap_data = pd.crosstab(
        Analytics_df['sector'],
        Analytics_df['bedRoom']
    )

    # Select top sectors (optional but cleaner)
    top_sectors = Analytics_df['sector'].value_counts().head(10).index

    heatmap_data = heatmap_data.loc[top_sectors]

    heatmap_data.columns = [f"{i} BHK" for i in heatmap_data.columns]

    # Plot heatmap
    fig, ax = plt.subplots(figsize=(10,6))

    sns.heatmap(
        heatmap_data,
        annot=True,
        fmt="d",
        cmap="YlOrRd",
        ax=ax
    )

    ax.set_xlabel("Number of Bedrooms (BHK)")
    ax.set_ylabel("Sector")

    st.pyplot(fig)

    # Property Type Distribution
    st.subheader("Price Distribution: Flats vs Houses")

    fig, ax = plt.subplots()

    sns.histplot(
        data=Analytics_df,
        x="price_per_sqft",
        hue="property_type",
        kde=True,
        ax=ax
    )

    st.pyplot(fig)


# Amenities Frequency Chart-----------

with tab4:

    st.subheader("Popular Property Features")

    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color="black",
        colormap="Set2"
    ).generate_from_frequencies(feature_counts)

    fig, ax = plt.subplots()

    ax.imshow(wordcloud)
    ax.axis("off")

    st.pyplot(fig)

    st.subheader("Most Common Amenities")

    amenity_cols = [
        'study room',
        'servant room',
        'store room',
        'pooja room',
        'others'
    ]

    amenity_counts = Analytics_df[amenity_cols].sum().sort_values(ascending=False)

    amenity_counts.index = [
        "Study Room",
        "Servant Room",
        "Store Room",
        "Pooja Room",
        "Others"
    ]

    amenity_counts.index = amenity_counts.index.str.title()

    st.bar_chart(amenity_counts)


    