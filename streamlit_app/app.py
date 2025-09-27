import streamlit as st
import pandas as pd
import plotly.express as px
import duckdb
from pathlib import Path

# --- Setup base directory ---
BASE_DIR = Path(__file__).resolve().parent

# --- Load cleaned dataset ---
@st.cache_data
def load_data():
    return pd.read_parquet(BASE_DIR / "output" / "ola_clean.parquet")

df = load_data()

st.set_page_config(page_title="Ola Ride Insights", layout="wide")
st.title("🚕 Ola Ride Insights Dashboard")

# --- Sidebar Filters ---
st.sidebar.header("Filters")
vehicle_types = st.sidebar.multiselect(
    "Select Vehicle Type", options=df["vehicle_type"].dropna().unique(), default=[]
)
payment_methods = st.sidebar.multiselect(
    "Select Payment Method", options=df["payment_method"].dropna().unique(), default=[]
)

# Apply filters
filtered_df = df.copy()
if vehicle_types:
    filtered_df = filtered_df[filtered_df["vehicle_type"].isin(vehicle_types)]
if payment_methods:
    filtered_df = filtered_df[filtered_df["payment_method"].isin(payment_methods)]

# --- KPI Cards ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Rides", f"{len(filtered_df):,}")
col2.metric("Completed Rides", f"{filtered_df['is_completed'].sum():,}")
col3.metric("Total Revenue", f"₹{filtered_df['total_amount'].sum():,.0f}")
col4.metric("Cancellation Rate", 
            f"{(1 - (filtered_df['is_completed'].sum() / len(filtered_df))):.1%}" if len(filtered_df)>0 else "0%")

# --- Charts ---
st.subheader("📊 Ride Volume Over Time")
if "Date" in filtered_df.columns:
    # Ensure Date is in datetime format
    filtered_df["Date"] = pd.to_datetime(filtered_df["Date"], errors="coerce")
    
    # Resample daily
    daily = filtered_df.set_index("Date").resample("D").size().reset_index(name="rides")
    
    # Plot
    fig = px.line(daily, x="Date", y="rides", title="Daily Rides")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("💳 Revenue by Payment Method")
if "payment_method" in filtered_df.columns:
    pm = filtered_df.groupby("payment_method")["total_amount"].sum().reset_index()
    fig = px.pie(pm, names="payment_method", values="total_amount", title="Revenue Share")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("🚘 Top Vehicle Types by Distance")
if "vehicle_type" in filtered_df.columns:
    vt = (
        filtered_df.groupby("vehicle_type")["distance_km"]
        .sum()
        .reset_index()
        .sort_values("distance_km", ascending=False)
        .head(5)
    )
    fig = px.bar(
        vt,
        x="vehicle_type",
        y="distance_km",
        title="Top 5 Vehicle Types by Distance",
        text=vt["distance_km"].apply(lambda x: f"{x:,.0f} km")
    )
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("⭐ Ratings Distribution")
if "customer_rating" in filtered_df.columns:
    fig = px.histogram(filtered_df, x="customer_rating", nbins=10, title="Customer Rating Distribution")
    st.plotly_chart(fig, use_container_width=True)

# --- SQL Queries Viewer (Optional) ---
st.sidebar.subheader("SQL Query Explorer")
with open(BASE_DIR / "output" / "sql_queries.sql", "r") as f:
    sql_queries = f.read().split("-- ")
for q in sql_queries[1:]:  # first split is empty
    title, query = q.split("\n", 1)
    if st.sidebar.button(title.strip()):
        st.code(query.strip(), language="sql")

# --- SQL Query Runner ---
st.header("🔎 SQL Query Explorer")

with open(BASE_DIR / "output" / "sql_queries.sql", "r") as f:
    sql_queries = f.read().split("-- ")

# Register dataframe as table in DuckDB
con = duckdb.connect()
con.register("ola_clean", df)

for q in sql_queries[1:]:
    title, query = q.split("\n", 1)
    query = query.strip()
    if st.button(f"Run: {title.strip()}"):
        st.code(query, language="sql")
        try:
            result = con.execute(query).fetchdf()
            st.dataframe(result.head(50))   # show top 50 rows
            st.download_button(
                "Download CSV",
                result.to_csv(index=False).encode("utf-8"),
                f"{title.strip().replace(' ', '_')}.csv",
                "text/csv"
            )
        except Exception as e:
            st.error(f"Query failed: {e}")
