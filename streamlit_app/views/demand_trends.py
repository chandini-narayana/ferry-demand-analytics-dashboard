import plotly.graph_objects as go
import streamlit as st

from utils.styling import COLORS, plotly_layout_defaults, SERIES_COLORS
from utils.data_loader import apply_filters, DOW_ORDER


def render(full_df, filters):
    filtered = apply_filters(full_df, **filters)
    start, end = filters["date_range"]

    st.markdown('<div class="ff-topbar-title">Demand Trends</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="ff-topbar-sub">Interactive time-series patterns for '
        f'{start.strftime("%b %d, %Y")} &rarr; {end.strftime("%b %d, %Y")}</div>',
        unsafe_allow_html=True,
    )
    st.write("")

    if filtered.empty:
        st.info("No data in the selected filters.")
        return

    col_a, col_b = st.columns(2)

    # ---------------- Hourly demand ----------------
    with col_a:
        st.markdown('<div class="ff-card">', unsafe_allow_html=True)
        st.markdown('<div class="ff-h2">Average Demand by Hour of Day</div>', unsafe_allow_html=True)
        hourly = filtered.groupby("hour")[["Sales Count", "Redemption Count"]].mean().reset_index()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hourly["hour"], y=hourly["Sales Count"], name="Sales",
                                  mode="lines+markers", line=dict(color=SERIES_COLORS["sales"], width=2)))
        fig.add_trace(go.Scatter(x=hourly["hour"], y=hourly["Redemption Count"], name="Redemptions",
                                  mode="lines+markers", line=dict(color=SERIES_COLORS["redemptions"], width=2)))
        layout = plotly_layout_defaults(height=320)
        layout["xaxis"]["title"] = "Hour of day"
        layout["xaxis"]["dtick"] = 2
        fig.update_layout(**layout)
        st.plotly_chart(fig, width='stretch', config={"displaylogo": False})
        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- Day of week demand ----------------
    with col_b:
        st.markdown('<div class="ff-card">', unsafe_allow_html=True)
        st.markdown('<div class="ff-h2">Average Demand by Day of Week</div>', unsafe_allow_html=True)
        dow = filtered.groupby("day_name")[["Sales Count", "Redemption Count"]].mean().reindex(DOW_ORDER).reset_index()
        fig = go.Figure()
        fig.add_trace(go.Bar(x=dow["day_name"], y=dow["Sales Count"], name="Sales", marker_color=SERIES_COLORS["sales"]))
        fig.add_trace(go.Bar(x=dow["day_name"], y=dow["Redemption Count"], name="Redemptions", marker_color=SERIES_COLORS["redemptions"]))
        layout = plotly_layout_defaults(height=320)
        layout["barmode"] = "group"
        fig.update_layout(**layout)
        st.plotly_chart(fig, width='stretch', config={"displaylogo": False})
        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- Rolling averages ----------------
    st.markdown('<div class="ff-card">', unsafe_allow_html=True)
    st.markdown('<div class="ff-h2">Rolling Averages (smoothing raw 15-min intervals)</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="ff-caption">1-hour = 4 intervals &middot; 4-hour = 16 intervals. '
        'Shown for the selected date range (raw series can be noisy at 15-min granularity).</div>',
        unsafe_allow_html=True,
    )

    ts = filtered.sort_values("Timestamp").copy()
    ts["roll_1h"] = ts["Sales Count"].rolling(4, min_periods=1).mean()
    ts["roll_4h"] = ts["Sales Count"].rolling(16, min_periods=1).mean()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ts["Timestamp"], y=ts["Sales Count"], name="Raw (15-min)",
                              mode="lines", line=dict(color=COLORS["text_label"], width=1), opacity=0.5))
    fig.add_trace(go.Scatter(x=ts["Timestamp"], y=ts["roll_1h"], name="1-hour rolling avg",
                              mode="lines", line=dict(color=SERIES_COLORS["sales"], width=2)))
    fig.add_trace(go.Scatter(x=ts["Timestamp"], y=ts["roll_4h"], name="4-hour rolling avg",
                              mode="lines", line=dict(color=SERIES_COLORS["net"], width=2)))
    layout = plotly_layout_defaults(height=360)
    fig.update_layout(**layout)
    st.plotly_chart(fig, width='stretch', config={"displaylogo": False})
    st.markdown('</div>', unsafe_allow_html=True)
