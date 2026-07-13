import streamlit as st


def render():
    st.markdown('<div class="ff-topbar-title">Methodology</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="ff-topbar-sub">Data source, cleaning approach, and KPI definitions</div>',
        unsafe_allow_html=True,
    )
    st.write("")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="ff-card">', unsafe_allow_html=True)
        st.markdown('<div class="ff-h2">Data Source</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="ff-caption">
            Ticket sales and redemptions recorded every 15 minutes at the Jack Layton Ferry
            Terminal, covering service to Centre Island, Hanlan's Point, and Ward's Island
            (Toronto Government, Parks, Forestry &amp; Recreation).<br><br>
            <b>Coverage:</b> May 1, 2015 &ndash; December 21, 2025<br>
            <b>Rows:</b> ~261,500 interval-level records<br>
            <b>Fields:</b> <code>_id</code>, <code>Timestamp</code>, <code>Sales Count</code>,
            <code>Redemption Count</code>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="ff-card">', unsafe_allow_html=True)
        st.markdown('<div class="ff-h2">Data Cleaning</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="ff-caption">
            &bull; No missing values or duplicate timestamps were found.<br>
            &bull; Gaps between consecutive 15-min records reflect real overnight terminal
            closures, not data loss.<br>
            &bull; Extreme-volume intervals are flagged via the IQR method rather than removed
            &mdash; they align with known high-attendance dates (summer weekends, holidays)
            rather than sensor errors. Use the "Include flagged high-volume events" filter to
            toggle them in or out.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="ff-card">', unsafe_allow_html=True)
        st.markdown('<div class="ff-h2">KPI Definitions</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="ff-caption">
            <b>Tickets Sold / Redeemed per Hour</b> &mdash; average interval count &times; 4.<br><br>
            <b>Net Passenger Movement</b> &mdash; Sales &minus; Redemptions for an interval or day;
            summed within a day (reset at midnight) as a proxy for how many people are
            currently on the island.<br><br>
            <b>Peak Demand Windows</b> &mdash; the day-of-week &times; hour-of-day combinations
            with the highest average sales.<br><br>
            <b>Off-Season Utilization Index</b> &mdash; ratio of average Fall+Winter daily demand
            to average Summer daily demand. 1.00 = no seasonality; lower values indicate
            stronger summer concentration.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="ff-card">', unsafe_allow_html=True)
        st.markdown('<div class="ff-h2">Project Pipeline</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="ff-caption">
            1. <b>Jupyter Notebook</b> &mdash; ingestion, cleaning, feature engineering, EDA,
            KPI computation, and export of compact aggregates.<br>
            2. <b>Streamlit Dashboard</b> (this app) &mdash; interactive exploration for
            operations, policy, and management stakeholders.<br>
            3. <b>Research Paper</b> &mdash; full write-up of methodology, findings, and
            recommendations.<br>
            4. <b>Executive Summary</b> &mdash; condensed briefing for government stakeholders.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)
