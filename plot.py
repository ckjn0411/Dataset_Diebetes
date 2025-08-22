import pandas as pd
import plotly.express as px

def hist_by_outcome(df: pd.DataFrame, col: str):
    return px.histogram(df, x=col, color="Outcome",
                        barmode="overlay", opacity=0.65, marginal="box")

def box_by_outcome(df: pd.DataFrame, col: str):
    return px.box(df, x="Outcome", y=col, points="outliers")

def corr_heatmap(df: pd.DataFrame):
    num_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    if not num_cols:
        return None
    corr = df[num_cols].corr()
    return px.imshow(corr, text_auto=True, aspect="auto")
