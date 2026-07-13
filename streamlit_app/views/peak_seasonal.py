import plotly.graph_objects as go
import streamlit as st

from utils.styling import COLORS, plotly_layout_defaults, SERIES_COLORS
from utils.data_loader import apply_filters, DOW_ORDER, SEASON_ORDER


def render(full_df, filters):
    filtered = apply_filters(full_df, **filters)
    start, end = filters["date_range"]

    st.markdown('<div class="ff-topbar-title">Peak &amp; Seasonal Analysis</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="ff-topbar-sub">Where and when demand concentrates &mdash; peak vs off-peak comparison</div>',
        unsafe_allow_html=True,
    )
    st.write("")

    if filtered.empty:
        st.info("No data in the selected filters.")
        return

    # ---------------- Heatmap ----------------
    st.markdown('<div class="ff-card">', unsafe_allow_html=True)
    st.markdown('<div class="ff-h2">Demand Heatmap &mdash; Hour of Day vs Day of Week</div>', unsafe_allow_html=True)

    pivot = filtered.pivot_table(index="day_name", columns="hour", values="Sales Count", aggfunc="mean").reindex(DOW_ORDER)
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values, x=pivot.columns, y=pivot.index,
        colorscale=[[0, COLORS["bg_card"]], [0.5, "#1d6f85"], [1, COLORS["accent_cyan"]]],
        colorbar=dict(
            title=dict(text="Avg Sales", font=dict(color=COLORS["text_label"])),
            tickfont=dict(color=COLORS["text_label"]),
        ),
        hovertemplate="%{y}, %{x}:00<br>Avg sales: %{z:.1f}<extra></extra>",
    ))
    layout = plotly_layout_defaults(height=340)
    layout["xaxis"]["title"] = "Hour of day"
    layout["xaxis"]["dtick"] = 2
    fig.update_layout(**layout)
    st.plotly_chart(fig, width='stretch', config={"displaylogo": False})
    st.markdown('</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns([1, 1])

    # ---------------- Peak windows table ----------------
    with col_a:
        st.markdown('<div class="ff-card">', unsafe_allow_html=True)
        st.markdown('<div class="ff-h2">Top 10 Peak Demand Windows</div>', unsafe_allow_html=True)
        peak_windows = (
            filtered.groupby(["day_name", "hour"])["Sales Count"]
            .mean().reset_index().sort_values("Sales Count", ascending=False).head(10)
        )
        peak_windows.columns = ["Day", "Hour", "Avg Sales / Interval"]
        peak_windows["Avg Sales / Interval"] = peak_windows["Avg Sales / Interval"].round(1)
        st.dataframe(peak_windows, width='stretch', hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- Weekday vs weekend ----------------
    with col_b:
        st.markdown('<div class="ff-card">', unsafe_allow_html=True)
        st.markdown('<div class="ff-h2">Weekday vs Weekend</div>', unsafe_allow_html=True)
        wk = filtered.groupby("is_weekend")[["Sales Count", "Redemption Count"]].mean()
        wk.index = ["Weekday" if not i else "Weekend" for i in wk.index]
        fig = go.Figure()
        fig.add_trace(go.Bar(x=wk.index, y=wk["Sales Count"], name="Sales", marker_color=SERIES_COLORS["sales"]))
        fig.add_trace(go.Bar(x=wk.index, y=wk["Redemption Count"], name="Redemptions", marker_color=SERIES_COLORS["redemptions"]))
        layout = plotly_layout_defaults(height=260)
        layout["barmode"] = "group"
        fig.update_layout(**layout)
        st.plotly_chart(fig, width='stretch', config={"displaylogo": False})
        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- Seasonal comparison ----------------
    st.markdown('<div class="ff-card">', unsafe_allow_html=True)
    st.markdown('<div class="ff-h2">Seasonal Comparison &amp; Off-Season Utilization</div>', unsafe_allow_html=True)

    season_avg = filtered.groupby("season")[["Sales Count", "Redemption Count"]].mean().reindex(SEASON_ORDER).dropna(how="all")
    if not season_avg.empty:
        summer_avg = season_avg.loc["Summer", "Sales Count"] if "Summer" in season_avg.index else None
        offseason_rows = season_avg.loc[season_avg.index.isin(["Fall", "Winter"])]
        offseason_avg = offseason_rows["Sales Count"].mean() if not offseason_rows.empty else None

        c1, c2 = st.columns([2, 1])
        with c1:
            fig = go.Figure()
            fig.add_trace(go.Bar(x=season_avg.index, y=season_avg["Sales Count"], name="Sales", marker_color=SERIES_COLORS["sales"]))
            fig.add_trace(go.Bar(x=season_avg.index, y=season_avg["Redemption Count"], name="Redemptions", marker_color=SERIES_COLORS["redemptions"]))
            layout = plotly_layout_defaults(height=280)
            layout["barmode"] = "group"
            fig.update_layout(**layout)
            st.plotly_chart(fig, width='stretch', config={"displaylogo": False})
        with c2:
            if summer_avg and offseason_avg is not None:
                index_val = offseason_avg / summer_avg
                st.markdown(
                    f"""
                    <div class="ff-kpi-card" style="margin-top: 1.6rem;">
                        <div class="ff-kpi-label">Off-Season Utilization Index</div>
                        <div class="ff-kpi-value" style="color:{COLORS['accent_cyan']};">{index_val:.2f}</div>
                        <div class="ff-caption" style="margin-top:0.4rem;">
                            Ratio of average Fall+Winter demand to Summer demand within the current
                            filter window. 1.00 = no seasonality; lower = stronger summer concentration.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.info("Select a range covering Summer and Fall/Winter to compute this index.")
    st.markdown('</div>', unsafe_allow_html=True)
