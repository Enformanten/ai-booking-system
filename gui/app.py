from datetime import date

import streamlit as st

from thermo.recommender import Recommender

st.sidebar.title("GovTech AI")

# add dropdown input for school name
BUILDING_NAME = st.sidebar.selectbox(
    "Building name",
    ("demo_school", "demo_school_2"),
)
DATE = st.sidebar.date_input("Date", date.today())

if st.sidebar.button("Get recommendations"):
    recommender = Recommender.from_config(building_name=BUILDING_NAME)

    with st.spinner("Calculating recommendations..."):
        recommendation = recommender.run(day=DATE)

    st.table(recommendation.show())

    recommendations_list = (
        recommendation.top_recommendations().set_index("Time Slot").round(2)
    )
    st.dataframe(recommendations_list, use_container_width=True)
