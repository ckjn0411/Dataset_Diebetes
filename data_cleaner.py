
import numpy as np
import pandas as pd
import streamlit as st

ZERO_COLS = ['Glucose','BloodPressure','SkinThickness','Insulin','BMI']

@st.cache_data
def clean_data(df: pd.DataFrame, method: str = "median"):
    """
    Thay 0 -> NaN cho các cột không hợp lý rồi điền theo median/mean hoặc drop hàng đó.
    Trả về: (df_clean, cleaning_log)
    """
    out = df.copy()
    log = {}

    for c in ZERO_COLS:
        if c not in out.columns:
            continue
        zero_mask = (out[c] == 0)
        zcount = int(zero_mask.sum())
        if zcount == 0:
            continue

        out.loc[zero_mask, c] = np.nan

        if method == "median":
            val = out[c].median()
            out[c] = out[c].fillna(val)
        elif method == "mean":
            val = out[c].mean()
            out[c] = out[c].fillna(val)
        elif method == "drop":
            # drop đúng những hàng thiếu ở cột này
            out = out.dropna(subset=[c])
            val = None
        else:
            val = out[c].median()
            out[c] = out[c].fillna(val)

        log[c] = {
            "zeros_replaced": zcount,
            "method": method,
            "fill_value": None if val is None else round(float(val), 2)
        }

    return out, log

def apply_basic_filters(df: pd.DataFrame,
                        age_range=None, bmi_range=None,
                        glu_range=None, preg_range=None):
    view = df.copy()
    if age_range and "Age" in view.columns:
        view = view[view["Age"].between(*age_range)]
    if bmi_range and "BMI" in view.columns:
        view = view[view["BMI"].between(*bmi_range)]
    if glu_range and "Glucose" in view.columns:
        view = view[view["Glucose"].between(*glu_range)]
    if preg_range and "Pregnancies" in view.columns:
        view = view[view["Pregnancies"].between(*preg_range)]
    return view

def summary_table(df: pd.DataFrame):
    num_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    rows = []
    for c in num_cols:
        s = df[c]
        q25, q75 = s.quantile([0.25, 0.75])
        rows.append({
            "Feature": c,
            "Count": int(s.count()),
            "Missing": int(s.isna().sum()),
            "Mean": round(float(s.mean()), 2),
            "Median": round(float(s.median()), 2),
            "Std": round(float(s.std()), 2),
            "Min": round(float(s.min()), 2),
            "Max": round(float(s.max()), 2),
            "Q25": round(float(q25), 2),
            "Q75": round(float(q75), 2),
            "IQR": round(float(q75 - q25), 2),
            "Zeros": int((s == 0).sum())
        })
    return pd.DataFrame(rows)
