import matplotlib.pyplot as plt
import pandas as pd
from timple.timedelta import strftimedelta
import streamlit as st
import fastf1
import fastf1.plotting
from fastf1.core import Laps
import plotly.express as px


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
    laps = session.laps.pick_quicklaps()
    @st.cache_data(show_spinner=False)
    def load_telemetry_data(year, grand_prix, session_type, driver_code):
            
            session.load(telemetry=True, laps=True, weather=False)
            
            # Obtener la vuelta más rápida del piloto solicitado
            fastest_lap = session.laps.pick_driver(driver_code).pick_fastest()
            
            # Extraer la telemetría (distancia, velocidad, acelerador, freno, marchas)
            telemetry = fastest_lap.get_telemetry()
            telemetry['Driver'] = driver_code
            return telemetry, fastest_lap['LapTime']



                # make a color palette associating team names to hex codes
                #    team_palette = {team: fastf1.plotting.get_team_color(team, session=race)
                #    for team in standings}
    col1, col2 = st.sidebar.columns(2)
    with col1:
            driver1 = st.text_input("Driver 1", "VER").upper()
    with col2:
            driver2 = st.text_input("Driver 2", "NOR").upper()
    if st.sidebar.button("Show Telemetry", type="primary"):
            with st.spinner("Consulting telemetry data from F1 servers..."):
                try:
                    # Llamada a la función de carga
                    tel_driver1, time1 = load_telemetry_data(year, gp, session_type, driver1)
                    tel_driver2, time2 = load_telemetry_data(year, gp, session_type, driver2)
                    
                    st.success(f"Information from {gp} {year} was succesfully recovered!")

                    
                    # Métricas rápidas en pantalla
                    m_col1, m_col2 = st.columns(2)
                    m_col1.metric(f"Tiempo de Vuelta ({driver1})", str(time1)[7:15])
                    m_col2.metric(f"Tiempo de Vuelta ({driver2})", str(time2)[7:15])

                    # Mostrar la tabla de datos cargados (vista previa)
                    st.subheader("Telemetry Preview")
                    
                    st.dataframe(tel_driver1[['Distance', 'Speed', 'Throttle', 'Brake', 'nGear', 'RPM']].head(10))

                    c1,c2=st.columns([60,40])
                    with c1:
                        fig1=px.bar(session,x=f"{driver1}", y=f"{time1}", title=f"{driver1} time")
                        fig1.update_layout(showlegend=False)
                        st.plotly_chart(fig1,use_container_width=True)

                except Exception as e:
                    st.error(f"There was an error with: {e}. please, enter valid driver codes (ej. VER, NOR, LEC).")            
 
    #if(session_type.equals(R)):
#        s_type="Race"
    #else:
#         s_type="Qualy"
    #st.write(f"{s_type} Results")
    #st.dataframe(session.results)

