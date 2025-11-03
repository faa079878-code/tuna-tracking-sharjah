import streamlit as st
import folium
from streamlit_folium import st_folium
from io import BytesIO
import base64
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import tempfile
import os

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Tuna Migration Map - Sharjah", layout="wide")

st.title("🐟 Tuna Migration Mapping - Sharjah Coast")
st.write("""
This interactive app lets researchers log and visualize Tuna fish sightings along the Sharjah coastline.  
You can add new observations by entering coordinates and ecotype, then download the map image instantly.
""")

# ------------------ SIDEBAR INPUTS ------------------
st.sidebar.header("Add Fish Observation")

lat = st.sidebar.number_input("Latitude (°N)", min_value=24.0, max_value=26.0, value=25.35, step=0.0001)
lon = st.sidebar.number_input("Longitude (°E)", min_value=55.0, max_value=56.5, value=55.4, step=0.0001)
fish_type = st.sidebar.selectbox("Fish Ecotype", ["Juvenile", "Migratory", "Resident"])

# ------------------ SESSION STATE ------------------
if "fish_data" not in st.session_state:
    st.session_state.fish_data = []

if st.sidebar.button("Add Fish Marker"):
    st.session_state.fish_data.append({"lat": lat, "lon": lon, "type": fish_type})

if st.sidebar.button("Clear All Markers"):
    st.session_state.fish_data.clear()
    st.rerun()

# ------------------ MAP ------------------
m = folium.Map(location=[25.35, 55.4], zoom_start=11)

fish_styles = {
    "Juvenile": {"color": "blue", "icon": "fish"},
    "Migratory": {"color": "green", "icon": "fish"},
    "Resident": {"color": "red", "icon": "fish"}
}

for fish in st.session_state.fish_data:
    style = fish_styles[fish["type"]]
    folium.Marker(
        location=[fish["lat"], fish["lon"]],
        tooltip=f"{fish['type']} Fish\nLat: {fish['lat']:.4f}, Lon: {fish['lon']:.4f}",
        icon=folium.Icon(color=style["color"], icon=style["icon"], prefix='fa')
    ).add_to(m)

# Legend with black text
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
st_folium(m, width=900, height=600)

# ------------------ DOWNLOAD AS INTERACTIVE HTML ------------------
map_html = m._repr_html_().encode("utf-8")

st.download_button(
    label="📥 Download Map as HTML (Interactive)",
    data=map_html,
    file_name="sharjah_tuna_map.html",
    mime="text/html"
)



# ------------------ FOOTER ------------------
st.markdown("""
---
Developed for the study of **Tuna migratory behavior** along the Sharjah coastal waters.
""")

