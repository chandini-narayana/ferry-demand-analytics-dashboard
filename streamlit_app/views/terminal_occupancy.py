import datetime as dt
import plotly.graph_objects as go
import streamlit as st

from utils.styling import COLORS, plotly_layout_defaults, SERIES_COLORS, readout
from utils.data_loader import apply_filters


def render(full_df, daily_df, filters):
    filtered = apply_filters(full_df, **filters)
    start, end = filters["date_range"]
    daily_mask = (daily_df["date"].dt.date >= start) & (daily_df["date"].dt.date <= end)
    daily_filtered = daily_df.loc[daily_mask].copy()

    st.markdown('<div class="ff-topbar-title">Terminal Occupancy</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="ff-topbar-sub">Net passenger movement as a same-day proxy for people on the island</div>',
        unsafe_allow_html=True,
    )
    st.write("")

    if filtered.empty or daily_filtered.empty:
        st.info("No data in the selected filters.")
        return

    # ---------------- Daily net movement ----------------
    st.markdown('<div class="ff-card">', unsafe_allow_html=True)
    st.markdown('<div class="ff-h2">Daily Net Passenger Movement</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="ff-caption">Positive = more tickets sold than redeemed that day '
        '(net arrivals); negative = net departures.</div>',
        unsafe_allow_html=True,
    )
    fig = go.Figure()
    colors = [SERIES_COLORS["sales"] if v >= 0 else SERIES_COLORS["alt"] for v in daily_filtered["net_movement"]]
    fig.add_trace(go.Bar(x=daily_filtered["date"], y=daily_filtered["net_movement"], marker_color=colors, name="Net movement"))
    layout = plotly_layout_defaults(height=300)
    layout["showlegend"] = False
    fig.update_layout(**layout)
    st.plotly_chart(fig, width='stretch', config={"displaylogo": False})
    st.markdown('</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns([2, 1])

    # ---------------- Intraday cumulative occupancy for a single day ----------------
    with col_a:
        st.markdown('<div class="ff-card">', unsafe_allow_html=True)
        st.markdown('<div class="ff-h2">Same-Day Cumulative Occupancy Proxy</div>', unsafe_allow_html=True)

        available_dates = sorted(filtered["date"].unique())
        default_idx = len(available_dates) - 1
        picked_date = st.select_slider(
            "Pick a day to inspect", options=available_dates, value=available_dates[default_idx],
            format_func=lambda d: d.strftime("%b %d, %Y"),
        )
        day_data = filtered[filtered["date"] == picked_date].sort_values("Timestamp").copy()
        day_data["cum_net"] = day_data["net_movement"].cumsum()

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=day_data["Timestamp"], y=day_data["cum_net"], mode="lines",
            line=dict(color=SERIES_COLORS["net"], width=2.5), fill="tozeroy",
            fillcolor="rgba(240,166,58,0.10)", name="Cumulative net movement",
        ))
        layout = plotly_layout_defaults(height=300)
        fig.update_layout(**layout)
        st.plotly_chart(fig, width='stretch', config={"displaylogo": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        peak_val = int(day_data["cum_net"].max()) if len(day_data) else 0
        peak_time = day_data.loc[day_data["cum_net"].idxmax(), "Timestamp"].strftime("%H:%M") if len(day_data) else "--"
        st.markdown('<div class="ff-card" style="height:100%;">', unsafe_allow_html=True)
        st.markdown('<div class="ff-h2">Selected Day Summary</div>', unsafe_allow_html=True)
        st.markdown(readout("Peak Estimated Occupancy", f"{peak_val:,}", color_class="ff-readout-value ff-readout-value-amber"), unsafe_allow_html=True)
        st.write("")
        st.markdown(readout("Time of Peak", peak_time), unsafe_allow_html=True)
        st.write("")
        st.markdown(readout("Total Sales That Day", f"{int(day_data['Sales Count'].sum()):,}", color_class="ff-readout-value ff-readout-value-cyan"), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- Top peak occupancy days ----------------
    st.markdown('<div class="ff-card">', unsafe_allow_html=True)
    st.markdown('<div class="ff-h2">Top 10 Peak-Occupancy Days in Selected Window</div>', unsafe_allow_html=True)
    top_days = daily_filtered.sort_values("peak_occupancy", ascending=False).head(10)[
        ["date", "total_sales", "total_redemptions", "peak_occupancy"]
    ].copy()
    top_days.columns = ["Date", "Total Sales", "Total Redemptions", "Peak Occupancy (est.)"]
    top_days["Date"] = top_days["Date"].dt.strftime("%b %d, %Y")
    st.dataframe(top_days, width='stretch', hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)
