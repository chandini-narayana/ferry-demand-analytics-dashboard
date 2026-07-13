"""
Central design system for the Ferry Flow Analytics dashboard.

Palette sampled directly from the reference "mission control" screenshot
(Ocean Research Platform / PELAGIA OPS) the user shared:

    bg_main       #060a14   deep navy-black — main content canvas
    bg_sidebar    #1d2430   slate navy — sidebar panel
    bg_card       #0b222e   teal-navy — card / panel surfaces
    border        #16303d   subtle card border
    accent_cyan   #30c9e8   primary accent (brand, active states, primary series)
    accent_green  #2fbf8b   live/positive status
    accent_amber  #f0a63a   warning / off-peak comparison series
    text_primary  #f3f5f7   headings, key values
    text_secondary#9aa4b2   nav text, body copy
    text_label    #6b727b   uppercase small labels (LAT/LON-style captions)
"""

import streamlit as st

COLORS = {
    "bg_main": "#060a14",
    "bg_sidebar": "#1d2430",
    "bg_card": "#0b1a24",
    "bg_card_alt": "#0e2530",
    "border": "#1a3341",
    "accent_cyan": "#30c9e8",
    "accent_cyan_soft": "rgba(48, 201, 232, 0.12)",
    "accent_green": "#2fbf8b",
    "accent_amber": "#f0a63a",
    "accent_red": "#ef5a6f",
    "text_primary": "#f3f5f7",
    "text_secondary": "#9aa4b2",
    "text_label": "#6b727b",
}


def inject_global_css():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }}

        /* ---- App shell ---- */
        .stApp {{
            background-color: {COLORS['bg_main']};
        }}
        [data-testid="stHeader"] {{
            background-color: {COLORS['bg_main']};
        }}
        [data-testid="stToolbar"] {{ display: none; }}
        #MainMenu {{ visibility: hidden; }}
        footer {{ visibility: hidden; }}

        /* ---- Sidebar ---- */
        [data-testid="stSidebar"] {{
            background-color: {COLORS['bg_sidebar']};
            border-right: 1px solid {COLORS['border']};
        }}
        [data-testid="stSidebar"] > div:first-child {{
            padding-top: 1.4rem;
        }}

        /* ---- Section labels (NAVIGATION / FILTERS style) ---- */
        .ff-section-label {{
            color: {COLORS['text_label']};
            font-size: 0.68rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin: 1.4rem 0 0.5rem 0.2rem;
        }}

        /* ---- Brand block ---- */
        .ff-brand-title {{
            color: {COLORS['accent_cyan']};
            font-size: 1.35rem;
            font-weight: 800;
            letter-spacing: 0.02em;
            margin-bottom: 0.1rem;
        }}
        .ff-brand-sub {{
            color: {COLORS['text_secondary']};
            font-size: 0.78rem;
            margin-bottom: 0.4rem;
        }}

        /* ---- Cards ---- */
        .ff-card {{
            background-color: {COLORS['bg_card']};
            border: 1px solid {COLORS['border']};
            border-radius: 12px;
            padding: 1.1rem 1.3rem;
            margin-bottom: 1rem;
        }}
        .ff-card-flush {{
            background-color: {COLORS['bg_card']};
            border: 1px solid {COLORS['border']};
            border-radius: 12px;
            padding: 0;
            margin-bottom: 1rem;
            overflow: hidden;
        }}

        /* ---- Top bar ---- */
        .ff-topbar-title {{
            color: {COLORS['text_primary']};
            font-size: 1.55rem;
            font-weight: 800;
            margin-bottom: 0.1rem;
        }}
        .ff-topbar-sub {{
            color: {COLORS['text_secondary']};
            font-size: 0.92rem;
            margin-bottom: 0;
        }}

        /* ---- Pill badges ---- */
        .ff-badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            background-color: {COLORS['bg_card_alt']};
            border: 1px solid {COLORS['border']};
            border-radius: 999px;
            padding: 0.32rem 0.85rem;
            font-size: 0.78rem;
            font-weight: 600;
            color: {COLORS['text_secondary']};
        }}
        .ff-dot {{
            width: 7px; height: 7px; border-radius: 50%;
            display: inline-block;
        }}
        .ff-dot-live {{
            background-color: {COLORS['accent_green']};
            box-shadow: 0 0 6px 1px {COLORS['accent_green']};
            animation: ff-pulse 1.6s infinite;
        }}
        .ff-dot-idle {{ background-color: {COLORS['text_label']}; }}
        @keyframes ff-pulse {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.35; }}
            100% {{ opacity: 1; }}
        }}

        /* ---- Readout metrics (LAT / LON style) ---- */
        .ff-readout-label {{
            color: {COLORS['text_label']};
            font-size: 0.66rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            margin-bottom: 0.15rem;
        }}
        .ff-readout-value {{
            color: {COLORS['text_primary']};
            font-size: 1.28rem;
            font-weight: 700;
            font-family: 'JetBrains Mono', monospace;
        }}
        .ff-readout-value-cyan {{ color: {COLORS['accent_cyan']}; }}
        .ff-readout-value-green {{ color: {COLORS['accent_green']}; }}
        .ff-readout-value-amber {{ color: {COLORS['accent_amber']}; }}
        .ff-readout-unit {{
            color: {COLORS['text_secondary']};
            font-size: 0.85rem;
            font-weight: 500;
            margin-left: 0.2rem;
        }}

        /* ---- KPI cards ---- */
        .ff-kpi-card {{
            background-color: {COLORS['bg_card']};
            border: 1px solid {COLORS['border']};
            border-radius: 12px;
            padding: 1rem 1.2rem;
        }}
        .ff-kpi-label {{
            color: {COLORS['text_label']};
            font-size: 0.68rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            margin-bottom: 0.35rem;
        }}
        .ff-kpi-value {{
            color: {COLORS['text_primary']};
            font-size: 1.7rem;
            font-weight: 800;
            line-height: 1.1;
        }}
        .ff-kpi-delta-up {{ color: {COLORS['accent_green']}; font-size: 0.82rem; font-weight: 600; }}
        .ff-kpi-delta-down {{ color: {COLORS['accent_red']}; font-size: 0.82rem; font-weight: 600; }}
        .ff-kpi-delta-flat {{ color: {COLORS['text_secondary']}; font-size: 0.82rem; font-weight: 600; }}

        /* ---- Section headings inside content ---- */
        .ff-h2 {{
            color: {COLORS['text_primary']};
            font-size: 1.05rem;
            font-weight: 700;
            margin: 0 0 0.7rem 0;
        }}
        .ff-caption {{
            color: {COLORS['text_secondary']};
            font-size: 0.85rem;
        }}

        /* ---- Streamlit widget overrides ---- */
        [data-testid="stMetricValue"] {{ color: {COLORS['text_primary']}; }}
        [data-testid="stMetricLabel"] {{ color: {COLORS['text_label']}; }}
        div[data-baseweb="select"] > div {{
            background-color: {COLORS['bg_card_alt']};
            border-color: {COLORS['border']};
        }}
        .stDateInput input, .stTextInput input {{
            background-color: {COLORS['bg_card_alt']};
            color: {COLORS['text_primary']};
        }}
        hr {{ border-color: {COLORS['border']}; }}

        /* option menu container tweak (icon nav) */
        .nav-link {{
            font-family: 'Inter', sans-serif !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def readout(label, value, unit="", color_class="ff-readout-value"):
    """Small LAT/LON-style readout block."""
    unit_html = f'<span class="ff-readout-unit">{unit}</span>' if unit else ""
    return f"""
    <div>
        <div class="ff-readout-label">{label}</div>
        <div class="{color_class}">{value}{unit_html}</div>
    </div>
    """


def badge(text, live=False):
    dot_class = "ff-dot-live" if live else "ff-dot-idle"
    return f"""<span class="ff-badge"><span class="ff-dot {dot_class}"></span>{text}</span>"""


def kpi_card(label, value, delta=None, delta_direction="flat"):
    delta_html = ""
    if delta is not None:
        cls = {"up": "ff-kpi-delta-up", "down": "ff-kpi-delta-down", "flat": "ff-kpi-delta-flat"}[delta_direction]
        arrow = {"up": "▲", "down": "▼", "flat": "―"}[delta_direction]
        delta_html = f'<div class="{cls}">{arrow} {delta}</div>'
    return f"""
    <div class="ff-kpi-card">
        <div class="ff-kpi-label">{label}</div>
        <div class="ff-kpi-value">{value}</div>
        {delta_html}
    </div>
    """


# ---------------------------------------------------------------------------
# Plotly dark theme matching the app
# ---------------------------------------------------------------------------
def plotly_layout_defaults(title=None, height=380):
    return dict(
        title=dict(text=title, font=dict(size=15, color=COLORS["text_primary"], family="Inter")) if title else None,
        paper_bgcolor=COLORS["bg_card"],
        plot_bgcolor=COLORS["bg_card"],
        font=dict(family="Inter", color=COLORS["text_secondary"], size=12),
        height=height,
        margin=dict(l=10, r=10, t=50 if title else 20, b=10),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
            font=dict(color=COLORS["text_secondary"]),
        ),
        xaxis=dict(
            gridcolor=COLORS["border"], zerolinecolor=COLORS["border"],
            linecolor=COLORS["border"], tickfont=dict(color=COLORS["text_label"]),
        ),
        yaxis=dict(
            gridcolor=COLORS["border"], zerolinecolor=COLORS["border"],
            linecolor=COLORS["border"], tickfont=dict(color=COLORS["text_label"]),
        ),
        hoverlabel=dict(
            bgcolor=COLORS["bg_card_alt"], font=dict(color=COLORS["text_primary"], family="Inter"),
            bordercolor=COLORS["border"],
        ),
    )


SERIES_COLORS = {
    "sales": COLORS["accent_cyan"],
    "redemptions": COLORS["accent_green"],
    "net": COLORS["accent_amber"],
    "alt": COLORS["accent_red"],
}
