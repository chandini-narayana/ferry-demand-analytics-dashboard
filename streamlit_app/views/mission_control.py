import time
import datetime as dt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils.styling import COLORS, badge, readout, kpi_card, plotly_layout_defaults, SERIES_COLORS
from utils.data_loader import apply_filters


def _status_for_day(day_total, season_avg_lookup, season):
    """Classify a day's demand relative to its own season's typical level."""
    typical = season_avg_lookup.get(season, day_total)
    if typical == 0:
        return "No Data", COLORS["text_secondary"]
    ratio = day_total / typical
    if ratio >= 1.4:
        return "Peak Demand", COLORS["accent_amber"]
    elif ratio <= 0.6:
        return "Low Demand", COLORS["text_secondary"]
    return "Normal", COLORS["accent_green"]


def render(full_df, daily_df, kpi_summary_df, filters):
    date_range = filters["date_range"]
    filtered = apply_filters(full_df, **filters)
    start, end = date_range

    daily_mask = (daily_df["date"].dt.date >= start) & (daily_df["date"].dt.date <= end)
    daily_filtered = daily_df.loc[daily_mask].copy()

    # ---------------- Top bar ----------------
    top_l, top_r = st.columns([3, 2])
    with top_l:
        st.markdown('<div class="ff-topbar-title">Mission Control</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="ff-topbar-sub">Terminal-wide ticket sales &amp; redemption overview</div>',
            unsafe_allow_html=True,
        )
    with top_r:
        b1, b2 = st.columns(2)
        with b1:
            st.markdown(badge("Dataset: 2015 &ndash; 2025"), unsafe_allow_html=True)
        with b2:
            live_on = st.session_state.get("live_mode_on", False)
            st.markdown(badge("Live Replay" if live_on else "Historical Batch", live=live_on), unsafe_allow_html=True)

    st.write("")

    # ---------------- Readout row ----------------
    if len(filtered):
        last_row = filtered.sort_values("Timestamp").iloc[-1]
        last_sales = int(last_row["Sales Count"])
        last_redeem = int(last_row["Redemption Count"])
        last_net = int(last_row["net_movement"])
        last_ts = last_row["Timestamp"]
    else:
        last_sales = last_redeem = last_net = 0
        last_ts = pd.Timestamp(end)

    r1, r2, r3, r4, r5 = st.columns(5)
    with r1:
        st.markdown(readout("Latest Interval", last_ts.strftime("%b %d, %H:%M")), unsafe_allow_html=True)
    with r2:
        st.markdown(readout("Sales", last_sales, color_class="ff-readout-value ff-readout-value-cyan"), unsafe_allow_html=True)
    with r3:
        st.markdown(readout("Redemptions", last_redeem, color_class="ff-readout-value ff-readout-value-green"), unsafe_allow_html=True)
    with r4:
        sign = "+" if last_net >= 0 else ""
        st.markdown(readout("Net Movement", f"{sign}{last_net}", color_class="ff-readout-value ff-readout-value-amber"), unsafe_allow_html=True)
    with r5:
        st.markdown(readout("Window", f"{(end-start).days + 1}", unit="days"), unsafe_allow_html=True)

    st.write("")

    # ---------------- KPI cards ----------------
    total_sales = int(filtered["Sales Count"].sum())
    total_redeem = int(filtered["Redemption Count"].sum())
    net_total = total_sales - total_redeem
    outlier_count = int((filtered["sales_outlier"] | filtered["redeem_outlier"]).sum()) if len(filtered) else 0
    peak_occupancy = int(daily_filtered["peak_occupancy"].max()) if len(daily_filtered) else 0

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(kpi_card("Tickets Sold", f"{total_sales:,}"), unsafe_allow_html=True)
    with k2:
        st.markdown(kpi_card("Tickets Redeemed", f"{total_redeem:,}"), unsafe_allow_html=True)
    with k3:
        direction = "up" if net_total > 0 else ("down" if net_total < 0 else "flat")
        st.markdown(kpi_card("Net Movement (window)", f"{net_total:,}", delta="Sales − Redemptions", delta_direction=direction), unsafe_allow_html=True)
    with k4:
        st.markdown(kpi_card("Peak Same-Day Occupancy", f"{peak_occupancy:,}", delta=f"{outlier_count} flagged intervals", delta_direction="flat"), unsafe_allow_html=True)

    st.write("")

    # ---------------- Hero panel ----------------
    season_avg_lookup = full_df.groupby("season")["Sales Count"].sum().to_dict()
    # normalize to a rough "per day" typical using season day counts
    season_days = full_df.groupby("season")["date"].nunique().to_dict()
    season_avg_lookup = {s: season_avg_lookup[s] / max(season_days.get(s, 1), 1) for s in season_avg_lookup}

    if len(daily_filtered):
        last_day = daily_filtered.sort_values("date").iloc[-1]
        last_day_season = full_df.loc[full_df["date"] == last_day["date"].date(), "season"]
        season_for_day = last_day_season.iloc[0] if len(last_day_season) else "Summer"
        status_label, status_color = _status_for_day(last_day["total_sales"], season_avg_lookup, season_for_day)
    else:
        status_label, status_color = "No Data", COLORS["text_secondary"]

    hero_l, hero_r = st.columns([1, 3])
    with hero_l:
        st.markdown(
            f"""
            <div class="ff-card" style="height: 100%;">
                <div class="ff-readout-label">Current Window Status</div>
                <div style="font-size:1.25rem; font-weight:800; color:{status_color}; margin: 0.3rem 0 0.8rem 0;">
                    {status_label}
                </div>
                <div class="ff-caption">
                    Based on total sales for the most recent day in your selected window,
                    compared to that season's typical daily volume.
                </div>
                <hr/>
                <div class="ff-readout-label">Selected Range</div>
                <div style="color:{COLORS['text_primary']}; font-weight:600; margin-top:0.2rem;">
                    {start.strftime('%b %d, %Y')} &rarr; {end.strftime('%b %d, %Y')}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with hero_r:
        st.markdown('<div class="ff-card">', unsafe_allow_html=True)
        st.markdown('<div class="ff-h2">Passenger Flow &mdash; Sales vs Redemptions</div>', unsafe_allow_html=True)

        if len(daily_filtered):
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=daily_filtered["date"], y=daily_filtered["total_sales"],
                name="Sales", mode="lines", line=dict(color=SERIES_COLORS["sales"], width=2),
                fill="tozeroy", fillcolor="rgba(48,201,232,0.08)",
            ))
            fig.add_trace(go.Scatter(
                x=daily_filtered["date"], y=daily_filtered["total_redemptions"],
                name="Redemptions", mode="lines", line=dict(color=SERIES_COLORS["redemptions"], width=2),
            ))
            fig.add_trace(go.Scatter(
                x=daily_filtered["date"], y=daily_filtered["net_movement"],
                name="Net Movement", mode="lines",
                line=dict(color=SERIES_COLORS["net"], width=1.5, dash="dot"),
                yaxis="y2",
            ))
            layout = plotly_layout_defaults(height=340)
            layout["yaxis2"] = dict(overlaying="y", side="right", showgrid=False,
                                     tickfont=dict(color=COLORS["text_label"]))
            fig.update_layout(**layout)
            st.plotly_chart(fig, width='stretch', config={"displaylogo": False})
        else:
            st.info("No data in the selected filters.")

        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- Live Replay simulation ----------------
    with st.expander("⚡ Live Replay Mode — simulate a real-time feed"):
        st.markdown(
            '<div class="ff-caption">Steps tick-by-tick through the 15-minute interval data '
            'for the last day in your selected window, as if watching it stream live. '
            'Bounded to a fixed number of ticks so it never runs indefinitely.</div>',
            unsafe_allow_html=True,
        )
        c1, c2, c3 = st.columns([1, 1, 1])
        with c1:
            n_ticks = st.slider("Ticks to replay", 5, 60, 20)
        with c2:
            speed = st.slider("Seconds per tick", 0.1, 1.5, 0.4)
        with c3:
            start_btn = st.button("▶ Start Replay", width='stretch')

        if start_btn:
            last_day_data = full_df[full_df["date"] == end].sort_values("Timestamp")
            if last_day_data.empty:
                last_day_data = full_df[full_df["date"] == full_df["date"].max()].sort_values("Timestamp")

            if last_day_data.empty:
                st.warning("No interval-level data available to replay for this window.")
            else:
                st.session_state["live_mode_on"] = True
                placeholder = st.empty()
                tick_data = last_day_data.tail(n_ticks) if len(last_day_data) >= n_ticks else last_day_data
                running_net = 0
                history = []
                for _, row in tick_data.iterrows():
                    running_net += int(row["net_movement"])
                    history.append(running_net)
                    with placeholder.container():
                        st.markdown(f'<div class="ff-card">', unsafe_allow_html=True)
                        lc1, lc2, lc3, lc4 = st.columns(4)
                        with lc1:
                            st.markdown(readout("Tick Time", row["Timestamp"].strftime("%H:%M")), unsafe_allow_html=True)
                        with lc2:
                            st.markdown(readout("Sales", int(row["Sales Count"]), color_class="ff-readout-value ff-readout-value-cyan"), unsafe_allow_html=True)
                        with lc3:
                            st.markdown(readout("Redemptions", int(row["Redemption Count"]), color_class="ff-readout-value ff-readout-value-green"), unsafe_allow_html=True)
                        with lc4:
                            st.markdown(readout("Running Net (island)", running_net, color_class="ff-readout-value ff-readout-value-amber"), unsafe_allow_html=True)

                        mini = go.Figure()
                        mini.add_trace(go.Scatter(y=history, mode="lines", line=dict(color=SERIES_COLORS["net"], width=2)))
                        mini_layout = plotly_layout_defaults(height=120)
                        mini_layout["xaxis"]["visible"] = False
                        mini_layout["showlegend"] = False
                        mini.update_layout(**mini_layout)
                        st.plotly_chart(mini, width='stretch', config={"displayModeBar": False})
                        st.markdown('</div>', unsafe_allow_html=True)
                    time.sleep(speed)
                st.session_state["live_mode_on"] = False
                st.success(f"Replay finished — {len(tick_data)} intervals streamed.")
