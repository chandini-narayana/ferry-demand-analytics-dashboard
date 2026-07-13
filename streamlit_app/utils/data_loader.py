"""
Cached data loaders. Reads the compact files exported by the preprocessing
notebook (notebook/Ferry_Analytics_Preprocessing_EDA.ipynb -> data/processed/)
so the app starts instantly instead of reprocessing the raw 260k-row CSV.
"""

import os
import pandas as pd
import streamlit as st

_HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(_HERE, "data", "processed")

DOW_ORDER = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
SEASON_ORDER = ["Winter", "Spring", "Summer", "Fall"]


@st.cache_data(show_spinner=False)
def load_full():
    """Interval-level cleaned dataset with engineered features."""
    path = os.path.join(DATA_DIR, "ferry_cleaned_full.csv")
    df = pd.read_csv(path, parse_dates=["Timestamp"])
    df["date"] = df["Timestamp"].dt.date
    return df


@st.cache_data(show_spinner=False)
def load_daily():
    path = os.path.join(DATA_DIR, "ferry_daily_agg.csv")
    df = pd.read_csv(path, parse_dates=["date"])
    return df


@st.cache_data(show_spinner=False)
def load_kpi_hourly():
    return pd.read_csv(os.path.join(DATA_DIR, "ferry_kpi_hourly.csv"))


@st.cache_data(show_spinner=False)
def load_peak_windows():
    return pd.read_csv(os.path.join(DATA_DIR, "ferry_peak_windows.csv"))


@st.cache_data(show_spinner=False)
def load_kpi_summary():
    return pd.read_csv(os.path.join(DATA_DIR, "ferry_kpi_summary.csv"))


def apply_filters(df, date_range, seasons, weekend_mode, include_outliers):
    """Shared filter logic applied across every view."""
    start, end = date_range
    mask = (df["date"] >= start) & (df["date"] <= end)
    out = df.loc[mask].copy()

    if seasons:
        out = out[out["season"].isin(seasons)]

    if weekend_mode == "Weekdays only":
        out = out[~out["is_weekend"]]
    elif weekend_mode == "Weekends only":
        out = out[out["is_weekend"]]

    if not include_outliers and "sales_outlier" in out.columns:
        out = out[~(out["sales_outlier"] | out["redeem_outlier"])]

    return out
