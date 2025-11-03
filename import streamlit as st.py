import streamlit as st
import folium
from streamlit_folium import st_folium
from typing import Dict, Any

# --- Streamlit Configuration ---
st.set_page_config(
    page_title="Sharjah Coordinate Mapper",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Constants ---
# Approximate center of Sharjah, UAE
SHARJAH_CENTER_COORDS = [25.35, 55.40] 
INITIAL_ZOOM = 11

# --- Session State Initialization ---
# Initialize the list to store points if it doesn't exist in the session state
if 'points' not in st.session_state:
    st.session_state.points = []

# --- Functions ---

def add_point(lat: float, lon: float):
    """Adds a new coordinate point to the session state list."""
    # Basic validation for an approximate UAE/Sharjah area
    if not (24.0 < lat < 26.5 and 54.0 < lon < 56.5):
        st.error("Error: Coordinates must be within the approximate range for the UAE/Sharjah area (Latitude 24-26.5, Longitude 54-56.5).")
        return

    new_point = {"lat": lat, "lon": lon, "label": f"Point {len(st.session_state.points) + 1}"}
    st.session_state.points.append(new_point)
    st.success(f"Added point: Latitude {lat:.4f}° N, Longitude {lon:.4f}° E")

def reset_points():
    """Clears all points from the map and resets the application."""
    st.session_state.points = []
    # Rerun the app to update the map immediately
    st.experimental_rerun()

# --- Streamlit UI Layout ---

st.title("🗺️ Sharjah Geo-Mapper: Adding N & E Coordinates")
st.markdown("""
Enter the Latitude (N) and Longitude (E) coordinates below to mark specific locations on the interactive map of Sharjah.
""")

col_form, col_map = st.columns([1, 2])

# --- Input Form (Left Column) ---
with col_form:
    st.header("1. Enter Coordinates")

    with st.form("coordinate_form", clear_on_submit=True):
        # Input for Latitude (N)
        lat_input = st.number_input(
            "Latitude (N):",
            min_value=24.0,
            max_value=26.5,
            value=SHARJAH_CENTER_COORDS[0],
            step=0.001,
            format="%.4f",
            help="Northern coordinate (e.g., 25.35)"
        )
        
        # Input for Longitude (E)
        lon_input = st.number_input(
            "Longitude (E):",
            min_value=54.0,
            max_value=56.5,
            value=SHARJAH_CENTER_COORDS[1],
            step=0.001,
            format="%.4f",
            help="Eastern coordinate (e.g., 55.40)"
        )

        submitted = st.form_submit_button("Add Point to Map ➕")

        if submitted:
            add_point(lat_input, lon_input)

    st.divider()
    
    st.header("2. Current Points List")
    if st.session_state.points:
        # Display points in a dataframe
        st.dataframe(
            st.session_state.points,
            column_order=("label", "lat", "lon"),
            hide_index=True,
            use_container_width=True
        )
        # Button to clear all points
        st.button("Clear All Points", on_click=reset_points, use_container_width=True)
    else:
        st.info("No points added yet. Use the form to start mapping your locations!")


# --- Map Visualization (Right Column) ---
with col_map:
    st.header("Interactive Map")

    # 1. Create the Folium Map object centered on Sharjah
    m = folium.Map(
        location=SHARJAH_CENTER_COORDS,
        zoom_start=INITIAL_ZOOM,
        control_scale=True,
        tiles="OpenStreetMap"
    )

    # 2. Add all stored points as markers
    for idx, point in enumerate(st.session_state.points):
        lat = point["lat"]
        lon = point["lon"]
        label = point["label"]

        # Add a marker with a popup containing the coordinates
        folium.Marker(
            [lat, lon],
            popup=f"**{label}**<br>Lat: {lat:.4f}° N<br>Lon: {lon:.4f}° E",
            tooltip=label,
            icon=folium.Icon(color="red", icon="crosshairs", prefix='fa')
        ).add_to(m)

    # 3. Display the map using st_folium
    st_folium(m, height=550, width="100%")
