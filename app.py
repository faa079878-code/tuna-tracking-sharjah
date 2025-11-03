import streamlit as st
import folium
from streamlit_folium import st_folium
from io import BytesIO
import base64
import pandas as pd
import matplotlib.pyplot as plt
import io
import arabic_reshaper
from bidi.algorithm import get_display

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Tuna Migration & Ecotype Distribution", layout="wide")

# ------------------ BACKGROUND IMAGE ------------------
def set_background(local_img_path):
    with open(local_img_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    header {{ background: none; }}
    footer {{ visibility: hidden; }}
    .stNumberInput {{ margin-bottom: 10px; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

set_background("Background.jpg")

# ------------------ APP TITLE ------------------
st.markdown(
    '<h1 style="text-align: center;"><span style="background-color: rgba(0,0,0,0.8); color: white; padding: 6px; border-radius: 6px;">🐟 Tuna Migration Mapping & Ecotype Distribution</span></h1>',
    unsafe_allow_html=True
)

# ------------------ SIDEBAR: FISH OBSERVATION ------------------
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
    st.experimental_rerun()

# ------------------ MAP AND INSTRUCTIONS ------------------
st.subheader("🐟 Tuna Migration Map")

# Create columns: left for map, right for instructions
map_col, info_col = st.columns([3, 1])

with map_col:
    m = folium.Map(location=[25.35, 55.4], zoom_start=11)

    # Add fish markers
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

    # Legend
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

    # Display map
    st_folium(m, width=900, height=600)

    # Download Map
    map_html = m._repr_html_().encode("utf-8")
    st.download_button(
        label="📥 Download Map as HTML (Interactive)",
        data=map_html,
        file_name="sharjah_tuna_map.html",
        mime="text/html"
    )

with info_col:
    st.markdown(
        """
        ### How to Use the Map
        1. **Enter Latitude and Longitude** in the sidebar to set the location of the fish sighting.
        2. **Select Fish Ecotype** from the dropdown menu (Juvenile, Migratory, Resident).
        3. **Click 'Add Fish Marker'** to place the marker on the map.
        4. **Markers are color-coded**:
            - Blue: Juvenile
            - Green: Migratory
            - Red: Resident
        5. **Clear All Markers** to reset the map.
        6. **Download the map** as an interactive HTML to save your observations.
        """
    )

# ------------------ ECOTYPE DISTRIBUTION ------------------
st.subheader("📊 Ecotype Distribution Input")

groups = ["Juvenile", "Migratory", "Resident"]
categories = ["أنثى مهاجرة", "أنثى خليط الجينات", "أنثى مقيمة", "ذكر مهاجر", "ذكر خليط الجينات", "ذكر مقيم"]

data = {}
for group in groups:
    st.markdown(f"### {group} Group")
    group_data = {}
    total = 0
    for cat in categories:
        val = st.number_input(f"{cat} - {group}", min_value=0.0, max_value=100.0, value=0.0, step=1.0)
        group_data[cat] = val
        total += val
    if total != 100:
        st.warning(f"The total percentage for the ({group}) group is ({total}). It must be equal to 100%.")
    data[group] = group_data

df = pd.DataFrame(data)

fig, ax = plt.subplots(figsize=(6,5))
colors = ["lightgrey","grey","dimgray","lightgrey","grey","dimgray"]
hatches = [None,None,None,"//","//","//"]
bottom = [0,0,0]
for i, cat in enumerate(categories):
    values = df.loc[cat]
    ax.bar(groups, values, bottom=bottom, color=colors[i], hatch=hatches[i], edgecolor="black", label=cat)
    bottom = [sum(x) for x in zip(bottom, values)]

ax.set_ylim(0, 100)
ax.set_ylabel("Percent", fontsize=14, fontweight='bold')
ax.set_xlabel("Ecotype", fontsize=14, fontweight='bold', labelpad=15)

labels_rtl = [get_display(arabic_reshaper.reshape(cat)) for cat in categories]
ax.legend(bbox_to_anchor=(1.05,1), loc='upper left', labels=labels_rtl)

st.pyplot(fig)

buf = io.BytesIO()
fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
buf.seek(0)

st.download_button(
    label="📥 Download Graph as PNG",
    data=buf,
    file_name="ecotype_distribution.png",
    mime="image/png"
)

# ------------------ FOOTER ------------------
st.markdown("""
---
Developed for the study of **Tuna migratory behavior** along the Sharjah coastal waters.
""")






