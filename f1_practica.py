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
    page_title="F1 Team Results Dashboard!",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded"
)



st.title("F1 Team Results && Driver Performance Dashboard")

fastf1.Cache.enable_cache(CACHE_DIR)


#we can check the data with this functions
#schedule = fastf1.get_event_schedule(2021)
#st.dataframe(schedule)

#this is just to check our info at first
#session = fastf1.get_session(2025, 'Las Vegas', 'R')
#session.load()
#st.dataframe(session.results)

with st.sidebar:
    st.write("Check GP results!")
    year=st.selectbox("Year",options=["SELECT",2025, 2024, 2023, 2022], index=0)
    gp = st.sidebar.selectbox("Grand Prix", ["SELECT","Monza", "Silverstone", "Spa", "Bahrain", "Monaco"], index=0)
    session_type = st.sidebar.selectbox("Session", ["SELECT","Q", "R"], index=0)

if year and gp and session_type !="SELECT":
      session = fastf1.get_session(year,gp, session_type)
      session.load()
      st.dataframe(session.results)
      laps = session.laps.pick_quicklaps()
      c1,c2,c3,c4,c5=st.columns(5)
      with c1:
                standings = (
                full_df.groupby('TeamName')['Points']
                .sum()
                .reset_index()
                .sort_values(by='Points', ascending=False)
                .reset_index(drop=True)
            )
            
                st.write(standings)

            # make a color palette associating team names to hex codes
                team_palette = {team: fastf1.plotting.get_team_color(team, session=race)
                for team in standings}