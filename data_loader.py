
import pandas as pd
import streamlit as st

@st.cache_data
def load_csv(path_or_buffer="./data/diabetes.csv") -> pd.DataFrame:
    return pd.read_csv(path_or_buffer)

def basic_info(df: pd.DataFrame):
    info = {
        "rows": len(df),
        "cols": df.shape[1],
        "columns": df.columns.tolist(),
        "missing_total": int(df.isna().sum().sum())
    }
    if "Outcome" in df.columns:
        info["pos"] = int(df["Outcome"].sum())
        info["pos_rate"] = float(df["Outcome"].mean() * 100)
    else:
        info["pos"] = None
        info["pos_rate"] = None
    return info

def zero_quality(df: pd.DataFrame):
    cols = ['Glucose','BloodPressure','SkinThickness','Insulin','BMI']
    rows = []
    for c in cols:
        if c in df.columns:
            z = int((df[c] == 0).sum())
            rows.append({"column": c, "zero_count": z, "zero_percent": round(z / len(df) * 100, 2)})
    return pd.DataFrame(rows)
