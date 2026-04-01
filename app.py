import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="Global Convection Explorer", layout="wide")

st.title("🌍 Global Convection & Wind Explorer")
st.markdown("""
This interactive app lets you explore how solar heating and the Earth's rotation combine to create our global wind patterns.
Use the controls on the left to see how different forces change the system.
""")

st.sidebar.header("Control Panel")

# 1. Primary Toggle: Rotation (Coriolis)
show_coriolis = st.sidebar.checkbox("Apply Coriolis Effect (Earth Rotation)", value=True)

# 2. Secondary Focus: Cell Selection (Only active if Coriolis is ON)
if show_coriolis:
    cell_focus = st.sidebar.selectbox("Focus on Cell:", ["All Cells (Overview)", "Hadley (Tropical)", "Ferrell (Mid-Latitude)", "Polar (High-Latitude)"])
else:
    cell_focus = "Non-Rotating Earth" # Override if rotation is off
    st.sidebar.warning("Activate the Coriolis Effect to see the three-cell model.")


# --- Visualization Logic ---
col1, col2 = st.columns([2, 1])

# Image URLs (Using representative public domain images)
# 1. Full Three-Cell Model (Standard view)
img_3cell_all = "https://upload.wikimedia.org/wikipedia/commons/9/9c/Earth_Global_Circulation_-_en.svg"

# 2. Simplified/Single-Cell Model (Hypothetical Non-Rotating Earth)
# Since a perfect image is hard to find, we use a single Hadley-style circulation overview
img_single_cell = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Global_atmospheric_circulation_-_Hadley_cell_only.svg/1024px-Global_atmospheric_circulation_-_Hadley_cell_only.svg.png"

# Helper to load images efficiently
def load_image(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

with col1:
    st.subheader("Atmospheric Cross-Section & Visualization")
    
    # Selection logic for which image to show
    if not show_coriolis:
        # Non-rotating Earth scenario
        st.warning("🔄 **Non-Rotating Earth Visualization**")
        st.write("In this hypothetical scenario, the Earth does not rotate. The only driver of wind is the temperature difference between the Equator and the Poles. We get one giant convection cell.")
        st.image(load_image(img_single_cell), caption="A simplified single-cell circulation model (Equator to Pole).", use_column_width=True)

    else:
        # Rotating Earth (Standard Three-Cell Model)
        st.success("✨ **Coriolis Effect Active**")
        
        # Determine specific text/emphasis based on cell focus
        if cell_focus == "Hadley (Tropical)":
            st.info("**Hadley Cell (0° - 30°):** The primary driver. Sun heats the equator, air rises, travels poleward, and sinks at 30°.")
        elif cell_focus == "Ferrell (Mid-Latitude)":
            st.warning("**Ferrell Cell (30° - 60°):** A 'mechanical' cell powered by the friction of the Hadley and Polar cells. Air moves poleward at the surface.")
        elif cell_focus == "Polar (High-Latitude)":
            st.error("**Polar Cell (60° - 90°):** Cold, dense air sinks at the poles and flows equatorward.")
        else:
            st.write("Earth's rotation breaks the single-cell circulation into three distinct cells in each hemisphere.")
            
        # Display the full three-cell model
        st.image(load_image(img_3cell_all), caption="The standard three-cell global circulation model.", use_column_width=True)


with col2:
    st.subheader("Resulting Surface Winds")
    
    if not show_coriolis:
        # Simplified Wind Data for Non-Rotating
        simplified_wind_data = {
            "Latitude": ["90°N (Pole)", "45°N", "0° (Equator)", "45°S", "90°S (Pole)"],
            "Surface Wind Direction": ["Southward", "Southward", "Calm/Rising", "Northward", "Northward"],
            "Description": ["Air flows directly toward Equator", "Air flows directly toward Equator", "Air rises vertically", "Air flows directly toward Equator", "Air flows directly toward Equator"]
        }
        st.table(pd.DataFrame(simplified_wind_data))
        st.markdown("⚠️ Without rotation, all surface winds would flow directly north or south toward the low pressure at the Equator.")
        
    else:
        # Standard Three-Cell Wind Data
        wind_data = {
            "Cell": ["Hadley", "Ferrell", "Polar"],
            "Latitude": ["0°-30° N/S", "30°-60° N/S", "60°-90° N/S"],
            "Base Flow": ["Equatorward", "Poleward", "Equatorward"],
            "Deflection (Coriolis)": ["Right (N. Hem), Left (S. Hem)", "Right (N. Hem), Left (S. Hem)", "Right (N. Hem), Left (S. Hem)"],
            "Resulting Wind": ["NE/SE Trade Winds", "Westerlies", "Polar Easterlies"]
        }
        st.table(pd.DataFrame(wind_data))
        st.markdown("Observe how the same initial flow direction is deflected differently depending on whether it's moving poleward or equatorward.")
