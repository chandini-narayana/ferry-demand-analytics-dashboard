import pandas as pd
import streamlit as st

from utils.data_loader import apply_filters


def _resample(df, granularity):
    if granularity == "15-minute (raw)":
        return df.sort_values("Timestamp")

    freq_map = {"Hourly": "H", "Daily": "D"}
    freq = freq_map[granularity]
    out = (
        df.set_index("Timestamp")
        .resample(freq)
        .agg({"Sales Count": "sum", "Redemption Count": "sum", "net_movement": "sum"})
        .reset_index()
    )
    return out


def render(full_df, filters):
    filtered = apply_filters(full_df, **filters)
    start, end = filters["date_range"]

    st.markdown('<div class="ff-topbar-title">Data Explorer</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="ff-topbar-sub">Browse, aggregate, and export the filtered dataset</div>',
        unsafe_allow_html=True,
    )
    st.write("")

    if filtered.empty:
        st.info("No data in the selected filters.")
        return

    st.markdown('<div class="ff-card">', unsafe_allow_html=True)

    ctrl1, ctrl2, ctrl3 = st.columns([1, 1, 2])
    with ctrl1:
        granularity = st.selectbox("Granularity", ["15-minute (raw)", "Hourly", "Daily"], index=2)
    with ctrl2:
        max_rows = st.selectbox("Rows to display", [100, 500, 1000, 5000], index=1)
    with ctrl3:
        st.markdown(
            f'<div class="ff-caption" style="margin-top:1.9rem;">'
            f'{len(filtered):,} interval rows matched between {start.strftime("%b %d, %Y")} and {end.strftime("%b %d, %Y")}.'
            f'</div>',
            unsafe_allow_html=True,
        )

    table_df = _resample(filtered, granularity)
    st.dataframe(table_df.head(max_rows), width='stretch', hide_index=True, height=460)

    csv_bytes = table_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇ Download this view as CSV",
        data=csv_bytes,
        file_name=f"ferry_data_{granularity.split()[0].lower()}_{start}_{end}.csv",
        mime="text/csv",
        width='content',
    )

    st.markdown('</div>', unsafe_allow_html=True)
