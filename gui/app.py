from datetime import date

import streamlit as st

from thermo.recommender import Recommender

################
# SIDEBAR
################

st.sidebar.title("GovTech AI")

# User input for building name
BUILDING_NAME = st.sidebar.selectbox(
    "Building name",
    ("demo_school", "demo_school_2"),
)
# User input for booking date
BOOKING_DATE = st.sidebar.date_input("Date", date.today())

# User input for required capacity
REQUIRED_CAPACITY = st.sidebar.slider(
    "Capacity",
    min_value=0,
    max_value=30,
    value=10,
    step=1,
)

# User input for required amenities
REQUIRED_AMENITIES = st.sidebar.multiselect(
    "Amenities",
    ("screen", "projector", "whiteboard", "speaker", "instruments"),
)

if st.sidebar.button("Get recommendations"):
    ################
    # MAIN PANE
    ################

    recommender = Recommender.from_config(building_name=BUILDING_NAME)

    with st.spinner("Calculating recommendations..."):
        recommendation = recommender.run(
            day=BOOKING_DATE,
            required_amenities=set(REQUIRED_AMENITIES),
            required_capacity=REQUIRED_CAPACITY,
        )

        st.table(recommendation.show())

        recommendations_list = (
            recommendation.top_recommendations().set_index("Time Slot").round(2)
        )
        st.dataframe(recommendations_list, use_container_width=True)
