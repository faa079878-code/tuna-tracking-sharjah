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
    new_fish = {
        "lat": lat,
        "lon": lon,
        "type": fish_type
    }
    st.session_state.fish_data.append(new_fish)

# Option to clear all data safely
if st.sidebar.button("Clear All Markers"):
    st.session_state.fish_data.clear()
    st.rerun()

# ------------------ MAP SETUP ------------------
# Center map around Sharjah
m = folium.Map(location=[25.35, 55.4], zoom_start=11)

# Define marker style for each fish type
fish_styles = {
    "Juvenile": {"color": "blue", "icon": "fish"},
    "Migratory": {"color": "green", "icon": "fish"},
    "Resident": {"color": "red", "icon": "fish"}
}

# Add all markers to map
for fish in st.session_state.fish_data:
    style = fish_styles[fish["type"]]
    folium.Marker(
        location=[fish["lat"], fish["lon"]],
        tooltip=f"{fish['type']} Fish\nLat: {fish['lat']:.4f}, Lon: {fish['lon']:.4f}",
        icon=folium.Icon(color=style["color"], icon=style["icon"], prefix='fa')
    ).add_to(m)

# ------------------ ADD LEGEND ------------------
legend_html = """
     <div style="
     position: fixed; 
     bottom: 50px; left: 50px; width: 180px; height: 120px; 
     background-color: rgba(255, 255, 255, 0.85);
     border:2px solid grey; z-index:9999; font-size:14px;
     border-radius: 8px; padding: 10px; color: black;">
     <b>Fish Ecotype Legend</b><br>
     <i class="fa fa-fish fa-1x" style="color:blue"></i>&nbsp; Juvenile<br>
     <i class="fa fa-fish fa-1x" style="color:green"></i>&nbsp; Migratory<br>
     <i class="fa fa-fish fa-1x" style="color:red"></i>&nbsp; Resident
     </div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

# ------------------ DISPLAY MAP ------------------
st.markdown("### 🗺️ Sharjah Beach - Tuna Sightings Map")
st_folium(m, width=900, height=600)

# ------------------ FOOTER ------------------
st.markdown("""
---
Developed for research use to study **migratory behavior of Tuna species** 
along the Sharjah coastal waters.
""")
