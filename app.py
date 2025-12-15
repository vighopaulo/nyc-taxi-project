import io
import numpy as np
import pandas as pd
import streamlit as st

DATA_PATH = "data/sample_data.csv"


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    # Load
    df = pd.read_csv(path)

    # Standardize common "missing" tokens
    df = df.replace(
        to_replace=["-", "—", "N/A", "n/a", "NA", "na", "null", "NULL", ""],
        value=np.nan,
    )

    # Strip whitespace from column names
    df.columns = [c.strip() for c in df.columns]

    # Try to auto-convert date/time-like columns by name
    for col in df.columns:
        col_l = col.lower()
        if any(k in col_l for k in ["date", "time", "month", "year"]):
            # Try datetime conversion (safe)
            try:
                df[col] = pd.to_datetime(df[col], errors="ignore")
            except Exception:
                pass

    # Try to convert object columns that look numeric
    for col in df.columns:
        if df[col].dtype == "object":
            # Attempt numeric conversion if it looks like numbers (commas, %)
            s = df[col].astype(str).str.replace(",", "", regex=False).str.replace("%", "", regex=False)
            numeric_try = pd.to_numeric(s, errors="coerce")

            # If a good portion converts, keep it numeric
            if numeric_try.notna().mean() >= 0.60:
                df[col] = numeric_try

    return df


def dataframe_info_text(df: pd.DataFrame) -> str:
    buffer = io.StringIO()
    df.info(buf=buffer)
    return buffer.getvalue()


def main():
    st.set_page_config(page_title="CSV Data Explorer", layout="wide")
    st.title("CSV Data Explorer")
    st.write("A general-purpose data exploration interface built with **pandas + Streamlit**.")

    # Load data
    try:
        df = load_data(DATA_PATH)
    except FileNotFoundError:
        st.error(f"Could not find `{DATA_PATH}`. Make sure the CSV exists in your repo at that path.")
        st.stop()
    except Exception as e:
        st.error("Failed to load data. See details below:")
        st.exception(e)
        st.stop()

    # Sidebar controls
    st.sidebar.header("Controls")
    option = st.sidebar.selectbox(
        "Choose an operation",
        [
            "View raw data",
            "Data summary",
            "Missing values (cleaning)",
            "Filter rows",
            "Group & aggregate",
            "Plot numeric column",
            "Correlation (numeric)",
        ],
    )

    # ============ 1) View raw data ============
    if option == "View raw data":
        st.subheader("Raw Data (first 50 rows)")
        st.dataframe(df.head(50), use_container_width=True)

        st.caption(f"Rows: {len(df):,} | Columns: {df.shape[1]}")

    # ============ 2) Data summary ============
    elif option == "Data summary":
        st.subheader("DataFrame Info")
        st.text(dataframe_info_text(df))

        st.subheader("Describe (stats)")
        st.write(df.describe(include="all"))

    # ============ 3) Missing values (cleaning) ============
    elif option == "Missing values (cleaning)":
        st.subheader("Missing Values Summary (before/after handling)")

        missing = df.isna().sum().sort_values(ascending=False)
        missing_df = pd.DataFrame(
            {"missing_count": missing, "missing_percent": (missing / len(df) * 100).round(2)}
        )
        st.dataframe(missing_df, use_container_width=True)

        st.subheader("Visual: Missing counts by column")
        st.bar_chart(missing_df["missing_count"])

        st.markdown("### Cleaning options")
        clean_choice = st.radio(
            "What do you want to do?",
            ["Do nothing (just inspect)", "Drop rows with ANY missing values", "Fill numeric missing values with median"],
        )

        if clean_choice == "Drop rows with ANY missing values":
            cleaned = df.dropna()
            st.success(f"Dropped rows with missing values. Rows: {len(df):,} → {len(cleaned):,}")
            st.dataframe(cleaned.head(50), use_container_width=True)

        elif clean_choice == "Fill numeric missing values with median":
            cleaned = df.copy()
            num_cols = cleaned.select_dtypes(include="number").columns
            for c in num_cols:
                cleaned[c] = cleaned[c].fillna(cleaned[c].median())
            st.success("Filled numeric missing values with median (non-numeric columns unchanged).")
            st.dataframe(cleaned.head(50), use_container_width=True)

    # ============ 4) Filter rows ============
    elif option == "Filter rows":
        st.subheader("Filter Rows")
        col = st.selectbox("Select column to filter", df.columns)

        # Numeric filter
        if pd.api.types.is_numeric_dtype(df[col]):
            st.write("Filtering numeric column")
            col_series = df[col].dropna()
            if col_series.empty:
                st.warning("This column has no numeric values to filter.")
            else:
                min_val = float(col_series.min())
                max_val = float(col_series.max())
                low, high = st.slider(
                    "Select range",
                    min_value=min_val,
                    max_value=max_val,
                    value=(min_val, max_val),
                )
                filtered = df[(df[col] >= low) & (df[col] <= high)]
                st.caption(f"Filtered rows: {len(filtered):,}")
                st.dataframe(filtered, use_container_width=True)

        # Datetime filter
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            st.write("Filtering datetime column")
            col_series = df[col].dropna()
            if col_series.empty:
                st.warning("This column has no datetime values to filter.")
            else:
                start = col_series.min().date()
                end = col_series.max().date()
                start_date, end_date = st.date_input("Select date range", (start, end))
                filtered = df[
                    (df[col] >= pd.to_datetime(start_date))
                    & (df[col] <= pd.to_datetime(end_date))
                ]
                st.caption(f"Filtered rows: {len(filtered):,}")
                st.dataframe(filtered, use_container_width=True)

        # Text/categorical filter
        else:
            st.write("Filtering text/category column")
            values = st.multiselect("Select values", df[col].dropna().unique().tolist())
            if values:
                filtered = df[df[col].isin(values)]
            else:
                filtered = df
            st.caption(f"Filtered rows: {len(filtered):,}")
            st.dataframe(filtered, use_container_width=True)

    # ============ 5) Group & aggregate ============
    elif option == "Group & aggregate":
        st.subheader("Group & Aggregate")

        group_col = st.selectbox("Group by", df.columns)

        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        if not numeric_cols:
            st.warning("No numeric columns available to aggregate.")
        else:
            agg_col = st.selectbox("Numeric column to aggregate", numeric_cols)
            agg_func = st.selectbox("Aggregation function", ["mean", "sum", "median", "min", "max", "count"])

            grouped = df.groupby(group_col)[agg_col].agg(agg_func).reset_index()
            st.dataframe(grouped, use_container_width=True)

            st.subheader("Chart")
            st.bar_chart(grouped.set_index(group_col)[agg_col])

    # ============ 6) Plot numeric column ============
    elif option == "Plot numeric column":
        st.subheader("Plot Numeric Column")

        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        if not numeric_cols:
            st.warning("No numeric columns available to plot.")
        else:
            col = st.selectbox("Select numeric column", numeric_cols)

            chart_type = st.selectbox("Chart type", ["Line (index order)", "Histogram", "Box plot (summary)"])

            if chart_type == "Line (index order)":
                st.line_chart(df[col].dropna().reset_index(drop=True))

            elif chart_type == "Histogram":
                # Simple histogram using value_counts on bins
                series = df[col].dropna()
                if series.empty:
                    st.warning("No values to plot.")
                else:
                    bins = st.slider("Bins", 5, 100, 20)
                    counts, edges = np.histogram(series, bins=bins)
                    hist_df = pd.DataFrame({"bin_left": edges[:-1], "count": counts})
                    st.bar_chart(hist_df.set_index("bin_left")["count"])

            elif chart_type == "Box plot (summary)":
                # Streamlit doesn't have native boxplot without libraries; show quantiles clearly
                series = df[col].dropna()
                if series.empty:
                    st.warning("No values to summarize.")
                else:
                    q = series.quantile([0, 0.25, 0.5, 0.75, 1]).rename(
                        index={0: "min", 0.25: "25%", 0.5: "50% (median)", 0.75: "75%", 1: "max"}
                    )
                    st.write("Box plot summary (quantiles):")
                    st.dataframe(q.to_frame(name=col), use_container_width=True)

    # ============ 7) Correlation ============
    elif option == "Correlation (numeric)":
        st.subheader("Correlation (numeric columns)")

        num_df = df.select_dtypes(include="number")
        if num_df.shape[1] < 2:
            st.warning("Need at least 2 numeric columns to compute correlation.")
        else:
            corr = num_df.corr(numeric_only=True)
            st.dataframe(corr, use_container_width=True)

            st.subheader("Heatmap-style view (table + highlight)")
            st.dataframe(corr.style.background_gradient(axis=None), use_container_width=True)

    # Footer
    st.caption("Tip: If you update code on GitHub, Streamlit Cloud auto-redeploys. Refresh the app after the redeploy completes.")


if __name__ == "__main__":
    main()
