# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import sys
# import os

# # Add project root to Python path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# from ml.run_ml import run_ml_pipeline
# from insights.generator import generate_insights
# from agent.decision_agent import rank_insights
# from genai.summarizer import generate_summary

# st.set_page_config(layout="wide")

# st.title("🤖 AI Insight Generation Dashboard")

# # -----------------------
# # FILE UPLOAD
# # -----------------------
# file = st.file_uploader("Upload CSV/JSON", type=["csv", "json"])

# if file:
#     # Run pipeline
#     df, daily_trend, weekly_trend = run_ml_pipeline(file)

#     # -----------------------
#     # SIDEBAR FILTERS
#     # -----------------------
#     st.sidebar.header("🔍 Filters")

#     country = st.sidebar.multiselect(
#         "Select Country", df["country"].unique(), default=df["country"].unique()
#     )

#     category = st.sidebar.multiselect(
#         "Select Category", df["category"].unique(), default=df["category"].unique()
#     )

#     filtered_df = df[
#         (df["country"].isin(country)) &
#         (df["category"].isin(category))
#     ]

#     # -----------------------
#     # KPIs
#     # -----------------------
#     st.subheader("📌 Key Metrics")

#     col1, col2, col3, col4 = st.columns(4)

#     col1.metric("Total Orders", len(filtered_df))
#     col2.metric("Total Revenue", f"${filtered_df['total_amount'].sum():,.0f}")
#     col3.metric("Anomalies", int(filtered_df['anomaly'].sum()))
#     col4.metric("Clusters", filtered_df['cluster'].nunique())

#     # -----------------------
#     # TABS
#     # -----------------------
#     tab1, tab2, tab3 = st.tabs(["📊 Visuals", "🔥 Insights", "🧠 AI Summary"])

#     # =======================
#     # TAB 1: VISUALS
#     # =======================
#     with tab1:
#         st.subheader("Customer Segmentation")

#         fig1 = px.scatter(
#             filtered_df,
#             x="quantity",
#             y="total_amount",
#             color="cluster",
#             hover_data=["country", "category"]
#         )
#         st.plotly_chart(fig1, use_container_width=True)

#         st.subheader("Anomaly Detection")

#         fig2 = px.scatter(
#             filtered_df,
#             x="quantity",
#             y="total_amount",
#             color="anomaly",
#             hover_data=["country", "category"]
#         )
#         st.plotly_chart(fig2, use_container_width=True)

#         st.subheader("Sales Trend")

#         fig3 = px.line(
#             daily_trend,
#             x="order_date",
#             y="total_amount",
#             title="Daily Sales"
#         )
#         st.plotly_chart(fig3, use_container_width=True)

#         st.subheader("Revenue by Category")

#         cat_fig = px.bar(
#             filtered_df.groupby("category")["total_amount"].sum().reset_index(),
#             x="category",
#             y="total_amount",
#             color="category"
#         )
#         st.plotly_chart(cat_fig, use_container_width=True)

#     # =======================
#     # TAB 2: INSIGHTS
#     # =======================
#     with tab2:
#         insights = generate_insights(filtered_df, daily_trend, weekly_trend)
#         ranked = rank_insights(insights)

#         st.subheader("Top Insights")

#         for ins in ranked:
#             if ins.priority == "high":
#                 st.error(f"🔥 {ins.text} → {ins.action}")
#             elif ins.priority == "medium":
#                 st.warning(f"⚠️ {ins.text} → {ins.action}")
#             else:
#                 st.info(f"ℹ️ {ins.text} → {ins.action}")

#     # =======================
#     # TAB 3: AI SUMMARY
#     # =======================
#     with tab3:
#         summary = generate_summary(ranked)

#         st.subheader("AI Generated Explanation")
#         st.write(summary)








import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ml.run_ml import run_ml_pipeline
from insights.generator import generate_insights
from agent.decision_agent import rank_insights
from genai.summarizer import generate_summary

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(layout="wide")
st.title("🤖 AI Insight Generation Dashboard")

# -----------------------
# FILE UPLOAD
# -----------------------
file = st.file_uploader("📂 Upload CSV/JSON", type=["csv", "json"])

if file:

    # -----------------------
    # RUN ML PIPELINE
    # -----------------------
    df, daily_trend, weekly_trend = run_ml_pipeline(file)

    # -----------------------
    # SIDEBAR FILTERS
    # -----------------------
    st.sidebar.header("🔍 Filters")

    countries = ["All"] + sorted(df["country"].dropna().unique().tolist())
    categories = ["All"] + sorted(df["category"].dropna().unique().tolist())

    selected_country = st.sidebar.multiselect(
        "Select Country", countries, default=["All"]
    )

    selected_category = st.sidebar.multiselect(
        "Select Category", categories, default=["All"]
    )

    filtered_df = df.copy()

    if "All" not in selected_country:
        filtered_df = filtered_df[filtered_df["country"].isin(selected_country)]

    if "All" not in selected_category:
        filtered_df = filtered_df[filtered_df["category"].isin(selected_category)]

    # -----------------------
    # KPIs
    # -----------------------
    st.subheader("📌 Key Metrics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Orders", len(filtered_df))
    col2.metric("Total Revenue", f"${filtered_df['total_amount'].sum():,.0f}")
    col3.metric("Anomalies", int(filtered_df['anomaly'].sum()))
    col4.metric("Clusters", filtered_df['cluster'].nunique())

    # -----------------------
    # TABS
    # -----------------------
    tab1, tab2, tab3 = st.tabs(["📊 Visuals", "🔥 Insights", "🧠 AI Summary"])

    # =======================
    # TAB 1: VISUALS
    # =======================
    with tab1:

        # -----------------------
        # CLUSTERING
        # -----------------------
        st.subheader("🎯 Cluster-wise Revenue")
        cluster_names = {
            0: "Low Value Customers",
            1: "Regular Customers",
            2: "High Value Customers",
            3: "Premium Customers"}

# Map cluster numbers to names
        filtered_df["cluster_name"] = filtered_df["cluster"].map(cluster_names)

        cluster_rev = filtered_df.groupby("cluster_name")["total_amount"].sum().reset_index()
        fig1 = px.bar(
                cluster_rev,
                x="cluster_name",
                y="total_amount",
                color="cluster_name",
                title="Revenue by Customer Segment"
        )

        st.plotly_chart(fig1, use_container_width=True)
        # -----------------------
        # ANOMALY
        # -----------------------
        st.subheader("🚨 Anomaly Detection")

        fig2 = px.scatter(
            filtered_df,
            x="quantity",
            y="total_amount",
            color=filtered_df["anomaly"].map({1: "Normal", -1: "Anomaly"}),
            color_discrete_map={"Normal": "blue", "Anomaly": "red"},
            hover_data=["country", "category"],
            title="Anomaly Detection"
        )
        st.plotly_chart(fig2, use_container_width=True)

        # -----------------------
        # LINE CHART (TREND)
        # -----------------------
        st.subheader("📈 Yearly Revenue Trend")
        trend = daily_trend.copy()
        trend["year"] = pd.to_datetime(trend["order_date"]).dt.year

        yearly_trend = trend.groupby("year")["total_amount"].sum().reset_index()

        fig3 = px.line(
                yearly_trend,
                x="year",
                y="total_amount",
                markers=True,
                title="Yearly Sales Trend"
            )

        st.plotly_chart(fig3, use_container_width=True)

        # -----------------------
        # PIE CHART
        # -----------------------
        st.subheader("🥧 Revenue Distribution by Category")

        pie_data = filtered_df.groupby("category")["total_amount"].sum().reset_index()

        pie_fig = px.pie(
            pie_data,
            names="category",
            values="total_amount",
            title="Category Contribution"
        )
        st.plotly_chart(pie_fig, use_container_width=True)

        # -----------------------
        # BAR CHART
        # -----------------------
        st.subheader("📊 Revenue by Category")

        cat_fig = px.bar(
            pie_data,
            x="category",
            y="total_amount",
            color="category",
            title="Category Revenue"
        )
        st.plotly_chart(cat_fig, use_container_width=True)

    # =======================
    # TAB 2: INSIGHTS
    # =======================
    with tab2:

        insights = generate_insights(filtered_df, daily_trend, weekly_trend)
        ranked = rank_insights(insights)

        st.subheader("🔥 Top Insights")

        if not ranked:
            st.info("No significant insights found.")
        else:
            for ins in ranked:
                if ins.priority == "high":
                    st.error(f"🔥 {ins.text} → {ins.action}")
                elif ins.priority == "medium":
                    st.warning(f"⚠️ {ins.text} → {ins.action}")
                else:
                    st.info(f"ℹ️ {ins.text} → {ins.action}")

    # =======================
    # TAB 3: AI SUMMARY
    # =======================
    with tab3:

        st.subheader("🧠 AI Generated Business Summary")

        try:
            summary = generate_summary(ranked)
            st.write(summary)
        except Exception as e:
            st.error(f"Error generating summary: {e}")

else:
    st.info("👆 Upload a dataset to get started.")