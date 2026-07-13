import streamlit as st

from utils.styling import inject_global_css
from utils.sidebar import render_sidebar
from utils.data_loader import load_full, load_daily, load_kpi_summary

from views import mission_control, demand_trends, peak_seasonal, terminal_occupancy, data_explorer, methodology

st.set_page_config(
    page_title="Ferry Flow Analytics",
    page_icon="⛴️",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_css()

full_df = load_full()
daily_df = load_daily()
kpi_summary_df = load_kpi_summary()

min_date = full_df["date"].min()
max_date = full_df["date"].max()

selected_page, filters = render_sidebar(min_date, max_date)

if selected_page == "Mission Control":
    mission_control.render(full_df, daily_df, kpi_summary_df, filters)
elif selected_page == "Demand Trends":
    demand_trends.render(full_df, filters)
elif selected_page == "Peak & Seasonal":
    peak_seasonal.render(full_df, filters)
elif selected_page == "Terminal Occupancy":
    terminal_occupancy.render(full_df, daily_df, filters)
elif selected_page == "Data Explorer":
    data_explorer.render(full_df, filters)
elif selected_page == "Methodology":
    methodology.render()
