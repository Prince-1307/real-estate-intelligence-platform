import streamlit as st
import pickle
import pandas as pd

df = pickle.load(open("project_dataset.pkl","rb"))
similarity = pickle.load(open("project_similarity.pkl","rb"))

st.title("🏡 Project Recommendation System")

st.write("Select a project to find similar projects based on facilities, location advantages and property configuration.")

project_name = st.selectbox(
    "Search Project",
    sorted(df['PropertyName'].unique()),
    index=None,
    placeholder="Type or select project"
)

def recommend(project):

    idx = df[df['PropertyName'] == project].index[0]

    distances = similarity[idx]

    project_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_projects = []

    for i in project_list:
        recommended_projects.append(df.iloc[i[0]])

    return recommended_projects


if st.button("Show Recommendations"):

    recommendations = recommend(project_name)

    st.subheader("Similar Projects You May Like")

    col1, col2 = st.columns(2)

    for i, project in enumerate(recommendations):

        with col1 if i % 2 == 0 else col2:

            st.markdown(f"### 🏢 {project['PropertyName']}")

            try:
                facilities = project['TopFacilities']

                if isinstance(facilities, str):
                    facilities = ast.literal_eval(facilities)

                st.write("**Top Facilities:**")

                st.write(", ".join(facilities[:6]))

            except:
                st.write("Facilities data unavailable")
            
            st.markdown(
                f"[🔗 View Project Details]({project['Link']})")

            st.write("---")

