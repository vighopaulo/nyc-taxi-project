import streamlit as st
import pandas as pd

DATA_PATH = "data/sample_data.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)

    # Automatically convert any date/time-like columns
    for col in df.columns:
        if df[col].dtype == "object":
            if any(key in col.lower() for key in ["date", "time"]):
                try:
                    df[col] = pd.to_datetime(df[col])
                except:
                    pass
    return df


def main():
    st.title("CSV Data Explorer")
    st.write("A general-purpose data exploration interface built with pandas + Streamlit.")

    df = load_data()

    option = st.sidebar.selectbox(
        "Choose an operation",
        [
            "View raw data",
            "Data summary",
            "Data quality & charts",
            "Filter rows",
            "Group & aggregate",
            "Plot numeric column",
        ],
    )

    if option == "View raw data":
        st.subheader("Raw Data (first 50 rows)")
        st.dataframe(df.head(50))
    elif option == "Data summary":
        st.subheader("DataFrame Info")
        
        import io
        buffer = io.StringIO()
        df.info(buf=buffer)
        st.text(buffer.getvalue())

        st.subheader("Describe (stats)")
        st.write(df.describe(include="all"))
        
    elif option == "Data quality & charts":
        st.subheader("Missing Values (per column)")
        missing = df.isna().sum().sort_values(ascending=False)
        st.dataframe(missing.rename("missing_count"))

        st.subheader("Missing Values (%)")
        missing_pct = (missing / len(df) * 100).round(2)
        st.dataframe(missing_pct.rename("missing_percent"))

        st.subheader("Duplicate Rows")
        dup_count = df.duplicated().sum()
        st.write(f"Duplicate rows: **{dup_count}**")

        st.subheader("Numeric Column Distributions")
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
    
    if numeric_cols:
        col = st.selectbox("Pick a numeric column", numeric_cols)
        st.bar_chart(df[col].dropna().value_counts().head(30))
    else:
        st.warning("No numeric columns detected for distribution plots.")

    st.subheader("Correlation (Numeric Columns)")
    if len(numeric_cols) >= 2:
        corr = df[numeric_cols].corr(numeric_only=True)
        st.dataframe(corr)
    else:
        st.warning("Need at least two numeric columns for correlation.")
        

    elif option == "Filter rows":
        st.subheader("Filter Rows")
        col = st.selectbox("Select column to filter", df.columns)

        if pd.api.types.is_numeric_dtype(df[col]):
            st.write("Filtering numeric column")
            min_val = float(df[col].min())
            max_val = float(df[col].max())
            low, high = st.slider("Select range", min_val, max_val, (min_val, max_val))
            filtered = df[(df[col] >= low) & (df[col] <= high)]
            st.dataframe(filtered)

        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            st.write("Filtering datetime column")
            start = df[col].min()
            end = df[col].max()
            start_date, end_date = st.date_input("Select date range", (start, end))
            filtered = df[
                (df[col] >= pd.to_datetime(start_date))
                & (df[col] <= pd.to_datetime(end_date))
            ]
            st.dataframe(filtered)

        else:
            st.write("Filtering text/category column")
            values = st.multiselect("Select values", df[col].dropna().unique())
            if values:
                filtered = df[df[col].isin(values)]
            else:
                filtered = df
            st.dataframe(filtered)

    elif option == "Group & aggregate":
        st.subheader("Group & Aggregate")
        group_col = st.selectbox("Group by", df.columns)
        numeric_cols = df.select_dtypes(include="number").columns.tolist()

        if numeric_cols:
            agg_col = st.selectbox("Numeric column to average", numeric_cols)
            grouped = df.groupby(group_col)[agg_col].mean().reset_index()
            st.dataframe(grouped)
            st.bar_chart(grouped.set_index(group_col))
        else:
            st.warning("No numeric columns available to aggregate.")

    elif option == "Plot numeric column":
        st.subheader("Plot Numeric Column")
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        if not numeric_cols:
            st.warning("No numeric columns available to plot.")
        else:
            col = st.selectbox("Select numeric column", numeric_cols)
            st.line_chart(df[col].dropna().reset_index(drop=True))


if __name__ == "__main__":
    main()
