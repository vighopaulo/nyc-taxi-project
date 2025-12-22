import io
import pandas as pd
import streamlit as st

DATA_PATH = "data/sample_data.csv"

st.set_page_config(page_title="CSV Data Explorer", layout="wide")


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)

    # Strip column names (prevents issues like "Trips Per Day " vs "Trips Per Day")
    df.columns = df.columns.str.strip()

    # Convert date/time-like columns
    for col in df.columns:
        if df[col].dtype == "object" and any(key in col.lower() for key in ["date", "time"]):
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # Convert numeric-looking text (e.g., "647,819" or "-") to numeric
    for col in df.columns:
        if df[col].dtype == "object":
            cleaned = (
                df[col]
                .astype(str)
                .str.strip()
                .str.replace(",", "", regex=False)
                .replace("-", pd.NA)
                .replace("None", pd.NA)
                .replace("nan", pd.NA)
            )
            df[col] = pd.to_numeric(cleaned, errors="ignore")

    return df


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
            "Category comparison",
            "Distribution analysis",
        ],
    )

    # ---------------- VIEW RAW DATA ----------------
    if option == "View raw data":
        st.subheader("Raw Data (first 50 rows)")
        st.dataframe(df.head(50), use_container_width=True)

    # ---------------- DATA SUMMARY ----------------
    elif option == "Data summary":
        st.subheader("DataFrame Info")
        buffer = io.StringIO()
        df.info(buf=buffer)
        st.text(buffer.getvalue())

        st.subheader("Describe (statistics)")
        st.dataframe(df.describe(include="all"), use_container_width=True)

    # ---------------- FILTER ROWS ----------------
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
            st.dataframe(filtered, use_container_width=True)

        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            start = df[col].min()
            end = df[col].max()

            start_date, end_date = st.date_input("Select date range", (start, end))
            filtered = df[
                (df[col] >= pd.to_datetime(start_date))
                & (df[col] <= pd.to_datetime(end_date))
            ]
            st.dataframe(filtered, use_container_width=True)

        else:
            values = st.multiselect("Select values", df[col].dropna().unique())
            filtered = df[df[col].isin(values)] if values else df
            st.dataframe(filtered, use_container_width=True)

    # ---------------- GROUP & AGGREGATE ----------------
    elif option == "Group & aggregate":
        st.subheader("Group & Aggregate")
        group_col = st.selectbox("Group by", df.columns)
        numeric_cols = df.select_dtypes(include="number").columns.tolist()

        if not numeric_cols:
            st.warning("No numeric columns available for aggregation.")
        else:
            agg_col = st.selectbox("Numeric column to average", numeric_cols)
            grouped = df.groupby(group_col)[agg_col].mean().reset_index()

            st.dataframe(grouped, use_container_width=True)
            st.bar_chart(grouped.set_index(group_col))

    # ---------------- PLOT NUMERIC COLUMN ----------------
    elif option == "Plot numeric column":
        st.subheader("Plot Numeric Column")
        numeric_cols = df.select_dtypes(include="number").columns.tolist()

        if not numeric_cols:
            st.warning("No numeric columns available.")
        else:
            col = st.selectbox("Select numeric column", numeric_cols)
            st.line_chart(df[col].dropna().reset_index(drop=True))

    # ---------------- CATEGORY COMPARISON ----------------
    elif option == "Category comparison":
        st.subheader("Average metric by License Class")

        required_cols = {"License Class", "Trips Per Day", "Unique Drivers", "Unique Vehicles"}
        missing = required_cols - set(df.columns)
        if missing:
            st.error(f"Missing required columns for this view: {sorted(missing)}")
        else:
            metric = st.selectbox(
                "Select metric",
                ["Trips Per Day", "Unique Drivers", "Unique Vehicles"],
            )

            grouped = df.groupby("License Class")[metric].mean().sort_values(ascending=False)
            st.bar_chart(grouped)

    # ---------------- DISTRIBUTION ANALYSIS ----------------
    elif option == "Distribution analysis":
        st.subheader("Distribution Analysis")
        numeric_cols = df.select_dtypes(include="number").columns.tolist()

        if not numeric_cols:
            st.warning("No numeric columns available.")
        else:
            col = st.selectbox("Select numeric column", numeric_cols)
            st.write("Histogram (binned counts)")

            st.bar_chart(
                df[col]
                .dropna()
                .value_counts(bins=30)
                .sort_index()
            )


if __name__ == "__main__":
    main()