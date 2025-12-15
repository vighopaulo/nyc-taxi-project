import io
import numpy as np
import pandas as pd
import streamlit as st

# -----------------------------
# Configuration
# -----------------------------
DATA_PATH = "data/sample_data.csv"

st.set_page_config(
    page_title="CSV Data Explorer",
    layout="wide"
)

# -----------------------------
# Data loading & cleaning
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)

    # Strip column names
    df.columns = df.columns.str.strip()

    # Attempt numeric conversion where possible
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="ignore")

    return df


# -----------------------------
# Main app
# -----------------------------
def main():
    st.title("CSV Data Explorer")
    st.write("A general-purpose data exploration interface built with Pandas + Streamlit.")

    df = load_data()

    option = st.sidebar.selectbox(
        "Choose an operation",
        [
            "View raw data",
            "Data summary",
            "Filter rows",
            "Group & aggregate",
            "Plot numeric column",
        ],
    )

    # -------------------------
    # View raw data
    # -------------------------
    if option == "View raw data":
        st.subheader("Raw Data (first 50 rows)")
        st.dataframe(df.head(50))

    # -------------------------
    # Data summary
    # -------------------------
    elif option == "Data summary":
        st.subheader("DataFrame Info")

        buffer = io.StringIO()
        df.info(buf=buffer)
        st.text(buffer.getvalue())

        st.subheader("Describe (statistics)")
        st.dataframe(df.describe(include="all"))

    # -------------------------
    # Filter rows
    # -------------------------
    elif option == "Filter rows":
        st.subheader("Filter Rows")

        col = st.selectbox("Select column to filter", df.columns)

        if pd.api.types.is_numeric_dtype(df[col]):
            min_val = float(df[col].min())
            max_val = float(df[col].max())

            low, high = st.slider(
                "Select numeric range",
                min_val,
                max_val,
                (min_val, max_val),
            )

            filtered = df[(df[col] >= low) & (df[col] <= high)]
            st.dataframe(filtered)

        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            start = df[col].min()
            end = df[col].max()

            start_date, end_date = st.date_input(
                "Select date range",
                (start, end),
            )

            filtered = df[
                (df[col] >= pd.to_datetime(start_date))
                & (df[col] <= pd.to_datetime(end_date))
            ]
            st.dataframe(filtered)

        else:
            values = st.multiselect(
                "Select values",
                df[col].dropna().unique()
            )

            if values:
                filtered = df[df[col].isin(values)]
                st.dataframe(filtered)
            else:
                st.dataframe(df)

    # -------------------------
    # Group & aggregate
    # -------------------------
    elif option == "Group & aggregate":
        st.subheader("Group & Aggregate")

        group_col = st.selectbox("Group by", df.columns)
        numeric_cols = df.select_dtypes(include="number").columns.tolist()

        if not numeric_cols:
            st.warning("No numeric columns available for aggregation.")
        else:
            agg_col = st.selectbox("Numeric column to average", numeric_cols)
            grouped = df.groupby(group_col)[agg_col].mean().reset_index()

            st.dataframe(grouped)
            st.bar_chart(grouped.set_index(group_col))

    # -------------------------
    # Plot numeric column
    # -------------------------
    elif option == "Plot numeric column":
        st.subheader("Plot Numeric Column")

        numeric_cols = df.select_dtypes(include="number").columns.tolist()

        if not numeric_cols:
            st.warning("No numeric columns available to plot.")
        else:
            col = st.selectbox("Select numeric column", numeric_cols)
            st.line_chart(df[col].dropna().reset_index(drop=True))


# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    main()
