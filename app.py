import streamlit as st
import pandas as pd

st.set_page_config(page_title="Global Convection Explorer", layout="wide")

st.title("🌍 Global Convection & Wind Explorer")
st.sidebar.header("Control Panel")

# Interactive Toggles
show_coriolis = st.sidebar.checkbox("Apply Coriolis Effect", value=True)
cell_focus = st.sidebar.selectbox("Focus on Cell:", ["All", "Hadley", "Ferrell", "Polar"])

# Educational Content Logic
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Atmospheric Cross-Section")
    if cell_focus == "Hadley":
        st.info("**Hadley Cell (0° - 30°):** Warm air rises at the Equator (Low Pressure), travels poleward aloft, and sinks at 30° (High Pressure).")
    elif cell_focus == "Ferrell":
        st.warning("**Ferrell Cell (30° - 60°):** The 'gear' cell. It moves in the opposite direction of the others, driven by the friction of the Hadley and Polar cells.")
    elif cell_focus == "Polar":
        st.error("**Polar Cell (60° - 90°):** Cold, dense air sinks at the poles and flows toward the equator before rising at 60°.")
    
    # Placeholder for a dynamic plot or 3D model
    st.image("https://upload.wikimedia.org/wikipedia/commons/9/9c/Earth_Global_Circulation_-_en.svg", use_column_width=True)

with col2:
    st.subheader("Resulting Surface Winds")
    wind_data = {
        "Cell": ["Hadley", "Ferrell", "Polar"],
        "Latitude": ["0°-30°", "30°-60°", "60°-90°"],
        "Base Direction": ["Equatorward", "Poleward", "Equatorward"],
        "With Coriolis (N. Hem)": ["NE Trade Winds", "Westerlies", "Polar Easterlies"]
    }
    df = pd.DataFrame(wind_data)
    st.table(df)

    if show_coriolis:
        st.success("✨ **Coriolis Active:** Winds are being deflected to the right in the Northern Hemisphere!")
    else:
        st.error("⚠️ **Coriolis Off:** In a non-rotating world, winds would move in simple North-South lines.")
