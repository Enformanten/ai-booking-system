from datetime import date

import pandas as pd
import streamlit as st

from thermo.config import AMENITIES, BUILDING_NAMES
from thermo.recommender import Recommender

################
# FUNCTIONS
# used for caching
################


@st.cache_data
def get_recommender(building_name: str) -> Recommender:
    """Return a recommender object based on the building name."""
    return Recommender.from_config(building_name=building_name)


@st.cache_data
def run_recommender(_recommender: Recommender, day: date, **kwargs) -> pd.DataFrame:
    """Return a dataframe of recommendations. Leading "_"
    on recommender tells  Streamlit not to try and hash
    the recommender object for caching.
    """
    return _recommender.run(day=day, **kwargs)


################
# SIDEBAR
################

st.sidebar.title("GovTech AI")

# User input for building name
BUILDING_NAME = st.sidebar.selectbox(
    "Building name",
    BUILDING_NAMES,
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
    AMENITIES,
)

if st.sidebar.button("Get recommendations"):
    ################
    # MAIN PANE
    ################

    recommender = get_recommender(building_name=BUILDING_NAME)

    with st.spinner("Calculating recommendations..."):
        recommendation = run_recommender(
            _recommender=recommender,
            day=BOOKING_DATE,
            required_amenities=set(REQUIRED_AMENITIES),
            required_capacity=REQUIRED_CAPACITY,
        )

        st.table(recommendation.show())

        recommendations_list = (
            recommendation.top_recommendations().set_index("Time Slot").round(2)
        )
        st.dataframe(recommendations_list, use_container_width=True)
