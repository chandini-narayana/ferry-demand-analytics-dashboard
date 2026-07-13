import datetime as dt
import streamlit as st
from streamlit_option_menu import option_menu

from utils.styling import COLORS
from utils.data_loader import SEASON_ORDER

NAV_ITEMS = [
    "Mission Control",
    "Demand Trends",
    "Peak & Seasonal",
    "Terminal Occupancy",
    "Data Explorer",
    "Methodology",
]

NAV_ICONS = [
    "speedometer2",
    "graph-up-arrow",
    "fire",
    "people-fill",
    "table",
    "info-circle",
]


def render_sidebar(min_date: dt.date, max_date: dt.date):
    with st.sidebar:
        st.markdown(
            """
            <div class="ff-brand-title">FERRY FLOW</div>
            <div class="ff-brand-sub">Toronto Island ferry ops, in real time</div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="ff-section-label">Navigation</div>', unsafe_allow_html=True)

        selected = option_menu(
            menu_title=None,
            options=NAV_ITEMS,
            icons=NAV_ICONS,
            default_index=0,
            styles={
                "container": {"padding": "0", "background-color": "transparent"},
                "icon": {"color": COLORS["text_secondary"], "font-size": "0.95rem"},
                "nav-link": {
                    "font-size": "0.88rem",
                    "font-weight": "500",
                    "color": COLORS["text_secondary"],
                    "text-align": "left",
                    "margin": "2px 0",
                    "padding": "0.55rem 0.7rem",
                    "border-radius": "8px",
                    "--hover-color": COLORS["bg_card_alt"],
                },
                "nav-link-selected": {
                    "background-color": COLORS["accent_cyan_soft"],
                    "color": COLORS["accent_cyan"],
                    "font-weight": "700",
                },
            },
        )

        st.markdown('<div class="ff-section-label">Filters</div>', unsafe_allow_html=True)

        date_range = st.date_input(
            "Date range",
            value=(max_date - dt.timedelta(days=60), max_date),
            min_value=min_date,
            max_value=max_date,
            label_visibility="collapsed",
        )
        if isinstance(date_range, dt.date):
            date_range = (date_range, date_range)
        elif len(date_range) == 1:
            date_range = (date_range[0], date_range[0])

        seasons = st.multiselect(
            "Season", options=SEASON_ORDER, default=[], placeholder="All seasons",
        )

        weekend_mode = st.radio(
            "Day type", options=["All days", "Weekdays only", "Weekends only"], index=0,
        )

        include_outliers = st.checkbox(
            "Include flagged high-volume events", value=True,
            help="Extreme 15-min intervals flagged by IQR outlier detection in the notebook "
                 "(e.g. holiday/event days). Unchecking shows 'typical day' patterns only.",
        )

        st.markdown('<div class="ff-section-label">About this build</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="ff-caption">Data: Jack Layton Ferry Terminal ticketing system, '
            '15-min interval sales &amp; redemptions, 2015&ndash;2025.</div>',
            unsafe_allow_html=True,
        )

        filters = {
            "date_range": date_range,
            "seasons": seasons,
            "weekend_mode": weekend_mode,
            "include_outliers": include_outliers,
        }

    return selected, filters
