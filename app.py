import streamlit as st
import folium
from streamlit_folium import st_folium

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Tuna Migration Map - Sharjah", layout="wide")

st.title("🐟 Tuna Migration Mapping - Sharjah Coast")
st.write("""
This interactive web app allows researchers to record and visualize Tuna fish sightings 
along the Sharjah coastline. Simply enter the geographic coordinates and ecotype, 
and a marker will appear on the map to indicate the location of the observation.
""")

# ------------------ SIDEBAR INPUTS ------------------
st.sidebar.header("Add Fish Observation")

lat = st.sidebar.number_input("Latitude (°N)", min_value=24.0, max_value=26.0, value=25.35, step=0.0001)
lon = st.sidebar.number_input("Longitude (°E)", min_value=55.0, max_value=56.5, value=55.4, step=0.0001)

fish_type = st.sidebar.selectbox(
    "Fish Ecotype",
    ["Juvenile", "Migratory", "Resident"]
)

# ------------------ SESSION STATE ------------------
if "fish_data" not in st.session_state:
    st.session_state.fish_data = []

# Add a new fish observation
if st.sidebar.button("Add Fish Marker"):
    st.session_state.fish_data.append({
        "lat": lat,
        "lon": lon,
        "type": fish_type
