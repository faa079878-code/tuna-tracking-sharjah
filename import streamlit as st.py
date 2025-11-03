import streamlit as st
import folium
from streamlit_folium import st_folium

# --- Page configuration ---
st.set_page_config(page_title="Tuna Migration Map - Sharjah", layout="wide")

st.title("🐟 Tuna Fish Migration Tracking in Sharjah Beach")
st.write("""
This interactive tool allows researchers to input observed Tuna locations 
and visualize their migratory patterns along the Sharjah coast.
""")

# --- Input section ---
st.sidebar.header("Add Fish Observation")

# Input coordinates
lat = st.sidebar.number_input("Latitude (N)", min_value=24.0, max_value=26.0, value=25.35, step=0.0001)
lon = st.sidebar.number_input("Longitude (E)", min_value=55.0, max_value=56.5, value=55.4, step=0.0001)

# Select fish ecotype
fish_type = st.sidebar.selectbox("Fish Ecotype", ["Juvenile", "Migratory", "Resident"])

# Initialize session state to store fish data
if "fish_data" not in st.session_state:
    st.session_state.fish_data = []

# Button to add fish point
if st.sidebar.button("Add Fish Marker"):
    st.session_state.fish_data.append({
        "lat": lat,
        "lon": lon,
        "type": fish_type
    })

# --- Map setup ---
# Center around Sharjah coastline
m = folium.Map(location=[25.35, 55.4], zoom_start=11)

# Define fish symbol/colors for each ecotype
fish_styles = {
    "Juvenile": {"color": "blue", "icon": "fish"},
    "Migratory": {"color": "green", "icon": "fish"},
    "Resident": {"color": "red", "icon": "fish"}
}

# Add markers for each recorded fish
for fish in st.session_state.fish_data:
    style = fish_styles[fish["type"]]
    folium.Marker(
        location=[fish["lat"], fish["lon"]],
        tooltip=f"{fish['type']} Fish\nLat: {fish['lat']}, Lon: {fish['lon']}",
        icon=folium.Icon(color=style["color"], icon=style["icon"], prefix='fa')
    ).add_to(m)

# --- Display map ---
st_data = st_folium(m, width=900, height=600)

# --- Option to clear data ---
if st.sidebar.button("Clear All Markers"):
    st.session_state.fish_data = []
    st.experimental_rerun()


