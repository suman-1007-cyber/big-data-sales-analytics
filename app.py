from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from generate_data import generate_dataset


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Big Data Sales Analytics",
    page_icon="📊",
    layout="wide",
)


# --------------------------------------------------
# DATA LOADING
# --------------------------------------------------
DATA_PATH = Path("data/sales_data.csv")


@st.cache_data
def load_data():
    if not DATA_PATH.exists():
        generate_dataset()

    df = pd.read_csv(DATA_PATH)
    df["order_date"] = pd.to_datetime(df["order_date"])

    df["revenue"] = (
        df["quantity"]
        * df["unit_price"]
        * (1 - df["discount"])
    )

    df["month"] = df["order_date"].dt.to_period("M").astype(str)

    return df


df = load_data()


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
st.sidebar.title("📊 Dashboard Controls")
st.sidebar.caption("Big Data Sales Analytics")

st.sidebar.divider()

min_date = df["order_date"].min().date()
max_date = df["order_date"].max().date()

date_range = st.sidebar.date_input(
    "📅 Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

regions = st.sidebar.multiselect(
    "🌍 Region",
    options=sorted(df["region"].unique()),
    default=sorted(df["region"].unique()),
)

categories = st.sidebar.multiselect(
    "📦 Category",
    options=sorted(df["category"].unique()),
    default=sorted(df["category"].unique()),
)

products = st.sidebar.multiselect(
    "🛍️ Product",
    options=sorted(df["product_name"].unique()),
    default=sorted(df["product_name"].unique()),
)

st.sidebar.divider()

st.sidebar.info(
    "Student: Suman Gunashekar Nadar\n\n"
    "Roll No.: 19035\n\n"
    "T.Y.B.Sc. Information Technology\n\n"
    "Subject: Big Data Framework"
)


# --------------------------------------------------
# FILTER DATA
# --------------------------------------------------
if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = date_range[0]
    end_date = date_range[0]

filtered_df = df[
    (df["order_date"].dt.date >= start_date)
    & (df["order_date"].dt.date <= end_date)
    & (df["region"].isin(regions))
    & (df["category"].isin(categories))
    & (df["product_name"].isin(products))
].copy()


# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.title("📊 Big Data Sales Analytics Dashboard")

st.caption(
    "Interactive Business Intelligence & Sales Analysis Platform"
)

st.info(
    "This project demonstrates large-scale sales data processing, "
    "filtering, aggregation and visualization using Python, Pandas, "
    "NumPy, Streamlit and Plotly."
)

st.divider()


# --------------------------------------------------
# KPI CALCULATIONS
# --------------------------------------------------
total_revenue = filtered_df["revenue"].sum()
total_orders = len(filtered_df)
total_units = filtered_df["quantity"].sum()

average_order_value = (
    total_revenue / total_orders
    if total_orders > 0
    else 0
)

unique_customers = filtered_df["customer_id"].nunique()


# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.metric(
        "💰 Total Revenue",
        f"₹{total_revenue:,.0f}",
    )

with c2:
    st.metric(
        "🧾 Total Orders",
        f"{total_orders:,}",
    )

with c3:
    st.metric(
        "📦 Units Sold",
        f"{total_units:,}",
    )

with c4:
    st.metric(
        "🛒 Average Order Value",
        f"₹{average_order_value:,.0f}",
    )

with c5:
    st.metric(
        "👥 Customers",
        f"{unique_customers:,}",
    )


st.divider()


# --------------------------------------------------
# TABS
# --------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📈 Overview",
        "💰 Sales Analysis",
        "🛍️ Products & Customers",
        "🔍 Data Quality",
    ]
)


# ==================================================
# TAB 1 - OVERVIEW
# ==================================================
with tab1:

    st.header("Sales Performance Overview")

    if filtered_df.empty:
        st.warning("No data matches the selected filters.")
    else:

        # Monthly revenue
        monthly = (
            filtered_df.groupby("month", as_index=False)["revenue"]
            .sum()
            .sort_values("month")
        )

        fig_monthly = px.line(
            monthly,
            x="month",
            y="revenue",
            markers=True,
            title="Monthly Revenue Trend",
            labels={
                "month": "Month",
                "revenue": "Revenue (₹)",
            },
        )

        fig_monthly.update_layout(
            height=420,
            margin=dict(l=20, r=20, t=60, b=20),
        )

        st.plotly_chart(
            fig_monthly,
            use_container_width=True,
        )

        col1, col2 = st.columns(2)

        # Region revenue
        with col1:

            region_sales = (
                filtered_df.groupby("region", as_index=False)["revenue"]
                .sum()
                .sort_values("revenue", ascending=False)
            )

            fig_region = px.bar(
                region_sales,
                x="region",
                y="revenue",
                title="Revenue by Region",
                labels={
                    "region": "Region",
                    "revenue": "Revenue (₹)",
                },
            )

            fig_region.update_layout(height=400)

            st.plotly_chart(
                fig_region,
                use_container_width=True,
            )

        # Category revenue
        with col2:

            category_sales = (
                filtered_df.groupby("category", as_index=False)["revenue"]
                .sum()
                .sort_values("revenue", ascending=False)
            )

            fig_category = px.pie(
                category_sales,
                names="category",
                values="revenue",
                hole=0.45,
                title="Revenue by Category",
            )

            fig_category.update_layout(height=400)

            st.plotly_chart(
                fig_category,
                use_container_width=True,
            )

        # Automatic insight
        if not region_sales.empty and not category_sales.empty:

            best_region = region_sales.iloc[0]["region"]
            best_region_value = region_sales.iloc[0]["revenue"]

            best_category = category_sales.iloc[0]["category"]

            st.success(
                f"📌 **Key Insight:** {best_region} is the highest-revenue "
                f"region with ₹{best_region_value:,.0f}. "
                f"The strongest product category is **{best_category}**."
            )


# ==================================================
# TAB 2 - SALES ANALYSIS
# ==================================================
with tab2:

    st.header("Detailed Sales Analysis")

    col1, col2 = st.columns(2)

    with col1:

        region_quantity = (
            filtered_df.groupby("region", as_index=False)["quantity"]
            .sum()
            .sort_values("quantity", ascending=False)
        )

        fig_quantity = px.bar(
            region_quantity,
            x="region",
            y="quantity",
            title="Units Sold by Region",
            labels={
                "region": "Region",
                "quantity": "Units Sold",
            },
        )

        fig_quantity.update_layout(height=400)

        st.plotly_chart(
            fig_quantity,
            use_container_width=True,
        )

    with col2:

        category_quantity = (
            filtered_df.groupby("category", as_index=False)["quantity"]
            .sum()
            .sort_values("quantity", ascending=False)
        )

        fig_cat_quantity = px.bar(
            category_quantity,
            x="category",
            y="quantity",
            title="Units Sold by Category",
            labels={
                "category": "Category",
                "quantity": "Units Sold",
            },
        )

        fig_cat_quantity.update_layout(height=400)

        st.plotly_chart(
            fig_cat_quantity,
            use_container_width=True,
        )

    st.subheader("Discount Analysis")

    discount_summary = (
        filtered_df.groupby("category", as_index=False)["discount"]
        .mean()
    )

    discount_summary["discount"] *= 100

    fig_discount = px.bar(
        discount_summary,
        x="category",
        y="discount",
        title="Average Discount by Category",
        labels={
            "category": "Category",
            "discount": "Average Discount (%)",
        },
    )

    fig_discount.update_layout(height=400)

    st.plotly_chart(
        fig_discount,
        use_container_width=True,
    )


# ==================================================
# TAB 3 - PRODUCTS & CUSTOMERS
# ==================================================
with tab3:

    st.header("Products & Customer Analysis")

    col1, col2 = st.columns(2)

    # Top products by revenue
    with col1:

        top_products = (
            filtered_df.groupby("product_name", as_index=False)["revenue"]
            .sum()
            .sort_values("revenue", ascending=False)
            .head(10)
        )

        fig_products = px.bar(
            top_products.sort_values("revenue"),
            x="revenue",
            y="product_name",
            orientation="h",
            title="Top 10 Products by Revenue",
            labels={
                "revenue": "Revenue (₹)",
                "product_name": "Product",
            },
        )

        fig_products.update_layout(height=500)

        st.plotly_chart(
            fig_products,
            use_container_width=True,
        )

    # Top products by quantity
    with col2:

        top_quantity = (
            filtered_df.groupby("product_name", as_index=False)["quantity"]
            .sum()
            .sort_values("quantity", ascending=False)
            .head(10)
        )

        fig_top_quantity = px.bar(
            top_quantity.sort_values("quantity"),
            x="quantity",
            y="product_name",
            orientation="h",
            title="Top 10 Products by Quantity",
            labels={
                "quantity": "Units Sold",
                "product_name": "Product",
            },
        )

        fig_top_quantity.update_layout(height=500)

        st.plotly_chart(
            fig_top_quantity,
            use_container_width=True,
        )

    st.subheader("Top 10 Customers by Revenue")

    top_customers = (
        filtered_df.groupby("customer_id", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
        .head(10)
    )

    top_customers["revenue"] = top_customers["revenue"].round(2)

    st.dataframe(
        top_customers,
        use_container_width=True,
        hide_index=True,
    )


# ==================================================
# TAB 4 - DATA QUALITY
# ==================================================
with tab4:

    st.header("Data Quality & Dataset Information")

    q1, q2, q3, q4 = st.columns(4)

    with q1:
        st.metric(
            "Total Records",
            f"{len(filtered_df):,}",
        )

    with q2:
        st.metric(
            "Columns",
            f"{len(filtered_df.columns):,}",
        )

    with q3:
        st.metric(
            "Missing Values",
            f"{filtered_df.isna().sum().sum():,}",
        )

    with q4:
        st.metric(
            "Duplicate Rows",
            f"{filtered_df.duplicated().sum():,}",
        )

    st.divider()

    st.subheader("Dataset Processing Pipeline")

    pipeline = pd.DataFrame(
        {
            "Stage": [
                "Data Generation",
                "Data Loading",
                "Data Cleaning",
                "Filtering",
                "Aggregation",
                "Visualization",
            ],
            "Technology": [
                "NumPy + Pandas",
                "Pandas",
                "Pandas",
                "Pandas",
                "Pandas",
                "Plotly + Streamlit",
            ],
            "Status": [
                "Completed",
                "Completed",
                "Completed",
                "Completed",
                "Completed",
                "Completed",
            ],
        }
    )

    st.dataframe(
        pipeline,
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Data Preview")

    st.dataframe(
        filtered_df.head(100),
        use_container_width=True,
        hide_index=True,
    )

    csv_data = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Filtered CSV",
        data=csv_data,
        file_name="filtered_sales_data.csv",
        mime="text/csv",
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.divider()

st.caption(
    "Big Data Sales Analytics Dashboard | "
    "Big Data Framework | T.Y.B.Sc. IT | "
    "Educational project using synthetic sales data"
)