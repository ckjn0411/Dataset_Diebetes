
import io
import pandas as pd
import streamlit as st
import plot as pl
import data_loader as dio
import data_cleaner as dc

st.set_page_config(page_title="Dataset Diabetes", page_icon="🩺", layout="wide")
st.title("🩺 Diabetes Dataset Explorer")
st.markdown("A simple and clean Streamlit app for exploring and cleaning the Pima Indians Diabetes dataset.")
st.markdown("## ⚙️ Data Preparation Settings")

df_raw = dio.load_csv("./data/diabetes.csv")

method = st.selectbox("Imputation method", ["median","mean","drop"], index=0, key="method")
use_clean = st.toggle("Use cleaned dataset", value=True, key="use_clean")

df_clean, clean_log = dc.clean_data(df_raw, method=method)
df = df_clean if use_clean else df_raw

# ===== Tabs =====
tab1, tab2, tab3 = st.tabs(["📌 Overview", "📊 Data Exploration", "🧹 Clean & Export"])

# -------- Overview --------
with tab1:
    st.markdown("### Dataset overview")
    info = dio.basic_info(df)
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Rows", info["rows"])
    c2.metric("Columns", info["cols"])
    c3.metric("Outcome=1", "-" if info["pos"] is None else info["pos"])
    c4.metric("% Positive", "-" if info["pos_rate"] is None else f"{info['pos_rate']:.1f}%")
    c5.metric("Missing (total)", info["missing_total"])

    st.markdown("### Preview")
    st.dataframe(df.head(20), use_container_width=True)

    st.markdown("### Summary Statistics")
    st.dataframe(dc.summary_table(df), use_container_width=True)

    st.markdown("### Data Quality ")
    qdf = dio.zero_quality(df_raw)
    if not qdf.empty:
        # đảm bảo dạng số để round không lỗi
        qdf["zero_percent"] = pd.to_numeric(qdf["zero_percent"], errors="coerce").round(2)
        st.dataframe(qdf, use_container_width=True)
    else:
        st.info("Không phát hiện 0 ở các cột nhạy cảm (Glucose/BMI/...).")

# -------- EDA --------
with tab2:
    st.markdown("### Basic Filters")
    def rng(s):
        return float(s.min()), float(s.max())

    view = df.copy()
    if "Age" in df.columns:
        a_lo, a_hi = rng(df["Age"])
        age_range = st.slider("Age", a_lo, a_hi, (a_lo, a_hi))
        view = view[view["Age"].between(*age_range)]
    if "BMI" in df.columns:
        b_lo, b_hi = rng(df["BMI"])
        bmi_range = st.slider("BMI", b_lo, b_hi, (b_lo, b_hi))
        view = view[view["BMI"].between(*bmi_range)]
    if "Glucose" in df.columns:
        g_lo, g_hi = rng(df["Glucose"])
        glu_range = st.slider("Glucose", g_lo, g_hi, (g_lo, g_hi))
        view = view[view["Glucose"].between(*glu_range)]
    if "Pregnancies" in df.columns:
        p_lo, p_hi = rng(df["Pregnancies"])
        preg_range = st.slider("Pregnancies", p_lo, p_hi, (p_lo, p_hi))
        view = view[view["Pregnancies"].between(*preg_range)]

    st.markdown(
        f"<div class='small-note'>After filtering: <b>{len(view)}</b> rows • Outcome=1: <b>{int(view['Outcome'].sum())}</b> ({view['Outcome'].mean()*100:.1f}%)</div>",
        unsafe_allow_html=True
    )

    st.markdown("### Distribution by Outcome")
    num_cols = [c for c in view.columns if pd.api.types.is_numeric_dtype(view[c]) and c != "Outcome"]
    if num_cols:
        col = st.selectbox("Select numeric feature", num_cols, index=min(1, len(num_cols)-1))
        c1, c2 = st.columns(2)
        with c1:
            fig = pl.hist_by_outcome(view, col)
            fig.update_layout(height=420)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig2 = pl.box_by_outcome(view, col)
            fig2.update_layout(height=420)
            st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### Correlation Heatmap")
    figc = pl.corr_heatmap(view)
    if figc is not None:
        figc.update_layout(height=520)
        st.plotly_chart(figc, use_container_width=True)
    else:
        st.info("No numeric columns available to plot.")

# -------- Clean & Export --------
with tab3:
    st.markdown("### Data Cleaning Report")
    if clean_log:
        st.json(clean_log)
    else:
        st.info("No zeros detected in sensitive columns (Glucose, BMI, etc.).")

    st.markdown("### Download cleaned dataset")
    buf = io.BytesIO()
    df.to_csv(buf, index=False)
    st.download_button("⬇️ Download CSV (current view)", data=buf.getvalue(),
                       file_name="diabetes_current.csv", mime="text/csv")
