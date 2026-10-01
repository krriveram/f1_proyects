import matplotlib.pyplot as plt
import pandas as pd
from timple.timedelta import strftimedelta
import streamlit as st
import fastf1
import fastf1.plotting
from fastf1.core import Laps



import streamlit as st
import fastf1
import pandas as pd
import os

CACHE_DIR = 'fastf1_cache'
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

#the first configuration
st.set_page_config(
    page_title="F1 Telemetry Dashboard!",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded"
)



st.title("F1 Telemetry && Performance Dashboard")

fastf1.Cache.enable_cache(CACHE_DIR)

#we can check the data with this functions
schedule = fastf1.get_event_schedule(2021)
st.dataframe(schedule)

session = fastf1.get_session(2025, 'Las Vegas', 'R')
session.load()
st.dataframe(session.results)


