
import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Nykaa Marketing Dashboard",
    page_icon="💄",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df = pd.read_csv("marketing_performance.csv")

df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("💄 NYKAA MARKETING PERFORMANCE DASHBOARD")
st.subheader("Executive Marketing Overview")

st.write(
    "Interactive analysis of marketing campaign performance, "
    "customer engagement and business KPIs."
)

# --------------------------------------------------
# DATE FILTER
# --------------------------------------------------

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

start_date, end_date = st.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Filter dataset
filtered_df = df[
    (df["Date"].dt.date >= start_date) &
    (df["Date"].dt.date <= end_date)
]

# --------------------------------------------------
# KPI CALCULATIONS
# --------------------------------------------------

total_revenue = filtered_df["Revenue"].sum()

total_cost = filtered_df["Acquisition_Cost"].sum()

total_conversions = filtered_df["Conversions"].sum()

total_visits = filtered_df["website_visits"].sum()

total_impressions = filtered_df["Impressions"].sum()

total_clicks = filtered_df["Clicks"].sum()

total_leads = filtered_df["Leads"].sum()

total_profit = filtered_df["Profit"].sum()

ctr = (total_clicks * 100 / total_impressions
    if total_impressions != 0 else 0
)

conversion_rate = (total_conversions * 100 / total_clicks
    if total_clicks != 0 else 0
)

roas = (total_revenue / total_cost
    if total_cost != 0 else 0
)

roi = (total_profit * 100 / total_cost
    if total_cost != 0 else 0
)

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

st.markdown("### Marketing KPI Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Revenue",
        f"₹{total_revenue:,.0f}"
    )

with col2:
    st.metric(
        "Acquisition Cost",
        f"₹{total_cost:,.0f}"
    )

with col3:
    st.metric(
        "Conversions",
        f"{total_conversions:,.0f}"
    )

with col4:
    st.metric(
        "Website Visits",
        f"{total_visits:,.0f}"
    )


col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric(
        "ROAS",
        f"{roas:,.2f}"
    )

with col6:
    st.metric(
        "CTR",
        f"{ctr:.2f}%"
    )

with col7:
    st.metric(
        "Conversion Rate",
        f"{conversion_rate:.2f}%"
    )

with col8:
    st.metric(
        "ROI",
        f"{roi:,.2f}%"
    )

# --------------------------------------------------
# MONTHLY ANALYSIS
# --------------------------------------------------

monthly = (
    filtered_df
    .assign(Year_Month=filtered_df["Date"].dt.to_period("M"))
    .groupby("Year_Month")
    .agg(
        Revenue=("Revenue", "sum"),
        Acquisition_Cost=("Acquisition_Cost", "sum"),
        Conversions=("Conversions", "sum")
    )
    .reset_index()
)

monthly["Year_Month"] = monthly["Year_Month"].astype(str)

# --------------------------------------------------
# MONTHLY REVENUE
# --------------------------------------------------

st.markdown("### 📈 Monthly Revenue Trend")

fig_revenue = px.line(
    monthly,
    x="Year_Month",
    y="Revenue",
    markers=True,
    title="Monthly Revenue"
)

fig_revenue.update_layout(
    xaxis_title="Month",
    yaxis_title="Revenue (₹)"
)

st.plotly_chart(
    fig_revenue,
    use_container_width=True
)

# --------------------------------------------------
# MONTHLY CONVERSIONS
# --------------------------------------------------

st.markdown("### 📈 Monthly Conversion Trend")

fig_conversion = px.line(
    monthly,
    x="Year_Month",
    y="Conversions",
    markers=True,
    title="Monthly Conversions"
)

fig_conversion.update_layout(
    xaxis_title="Month",
    yaxis_title="Conversions"
)

st.plotly_chart(
    fig_conversion,
    use_container_width=True
)

# --------------------------------------------------
# REVENUE VS COST
# --------------------------------------------------

st.markdown("### 💰 Revenue vs Acquisition Cost")

revenue_cost = monthly.melt(
    id_vars="Year_Month",
    value_vars=["Revenue", "Acquisition_Cost"],
    var_name="Metric",
    value_name="Amount"
)

fig_cost = px.bar(
    revenue_cost,
    x="Year_Month",
    y="Amount",
    color="Metric",
    barmode="group",
    title="Monthly Revenue vs Acquisition Cost"
)

fig_cost.update_layout(
    xaxis_title="Month",
    yaxis_title="Amount (₹)"
)

st.plotly_chart(
    fig_cost,
    use_container_width=True
)

# ==================================================
# CHANNEL ANALYSIS
# ==================================================

st.markdown("---")
st.title("📢 Channel Performance Analysis")

st.write(
    "Compare revenue, conversions, conversion rate, "
    "ROAS and ROI across different marketing channels."
)

# --------------------------------------------------
# CHANNEL FILTER
# --------------------------------------------------

channel_options = sorted(df["Channel_Used"].dropna().unique())

selected_channels = st.multiselect(
    "Select Marketing Channels",
    options=channel_options,
    default=channel_options
)

channel_df = filtered_df[
    filtered_df["Channel_Used"].isin(selected_channels)
]

# --------------------------------------------------
# CHANNEL KPI TABLE
# --------------------------------------------------

channel_analysis = (
    channel_df
    .groupby("Channel_Used")
    .agg(
        Revenue=("Revenue", "sum"),
        Acquisition_Cost=("Acquisition_Cost", "sum"),
        Conversions=("Conversions", "sum"),
        Clicks=("Clicks", "sum"),
        Impressions=("Impressions", "sum")
    )
    .reset_index()
)

channel_analysis["CTR"] = (
    channel_analysis["Clicks"] * 100 /
    channel_analysis["Impressions"]
)

channel_analysis["Conversion_Rate"] = (
    channel_analysis["Conversions"] * 100 /
    channel_analysis["Clicks"]
)

channel_analysis["ROAS"] = (
    channel_analysis["Revenue"] /
    channel_analysis["Acquisition_Cost"]
)

channel_analysis["ROI"] = (
    (channel_analysis["Revenue"] -
     channel_analysis["Acquisition_Cost"]) * 100 /
    channel_analysis["Acquisition_Cost"]
)

# --------------------------------------------------
# CHANNEL TABLE
# --------------------------------------------------

st.markdown("### 📊 Channel Performance Summary")

st.dataframe(
    channel_analysis[
        [
            "Channel_Used",
            "Revenue",
            "Acquisition_Cost",
            "Conversions",
            "CTR",
            "Conversion_Rate",
            "ROAS",
            "ROI"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# REVENUE BY CHANNEL
# --------------------------------------------------

st.markdown("### 💰 Revenue by Marketing Channel")

fig_channel_revenue = px.bar(
    channel_analysis.sort_values(
        "Revenue",
        ascending=False
    ),
    x="Channel_Used",
    y="Revenue",
    title="Revenue by Marketing Channel",
    text_auto=".2s"
)

fig_channel_revenue.update_layout(
    xaxis_title="Marketing Channel",
    yaxis_title="Revenue (₹)"
)

st.plotly_chart(
    fig_channel_revenue,
    use_container_width=True
)

# --------------------------------------------------
# CONVERSION RATE BY CHANNEL
# --------------------------------------------------

st.markdown("### 🎯 Conversion Rate by Channel")

fig_channel_conversion = px.bar(
    channel_analysis.sort_values(
        "Conversion_Rate",
        ascending=False
    ),
    x="Channel_Used",
    y="Conversion_Rate",
    title="Conversion Rate by Marketing Channel",
    text_auto=".2f"
)

fig_channel_conversion.update_layout(
    xaxis_title="Marketing Channel",
    yaxis_title="Conversion Rate (%)"
)

st.plotly_chart(
    fig_channel_conversion,
    use_container_width=True
)

# --------------------------------------------------
# ROAS BY CHANNEL
# --------------------------------------------------

st.markdown("### 📈 ROAS by Channel")

fig_channel_roas = px.bar(
    channel_analysis.sort_values(
        "ROAS",
        ascending=False
    ),
    x="Channel_Used",
    y="ROAS",
    title="ROAS by Marketing Channel",
    text_auto=".2f"
)

fig_channel_roas.update_layout(
    xaxis_title="Marketing Channel",
    yaxis_title="ROAS"
)

st.plotly_chart(
    fig_channel_roas,
    use_container_width=True
)

# ==================================================
# CUSTOMER SEGMENT & TARGET AUDIENCE ANALYSIS
# ==================================================

st.markdown("---")
st.title("👥 Customer & Target Audience Analysis")

st.write(
    "Analyze marketing performance across customer segments "
    "and target audience groups."
)

# --------------------------------------------------
# CUSTOMER SEGMENT FILTER
# --------------------------------------------------

customer_options = sorted(
    df["Customer_Segment"].dropna().unique()
)

selected_customers = st.multiselect(
    "Select Customer Segments",
    options=customer_options,
    default=customer_options
)

customer_df = filtered_df[
    filtered_df["Customer_Segment"].isin(selected_customers)
]

# --------------------------------------------------
# CUSTOMER SEGMENT ANALYSIS
# --------------------------------------------------

customer_analysis = (
    customer_df
    .groupby("Customer_Segment")
    .agg(
        Revenue=("Revenue", "sum"),
        Conversions=("Conversions", "sum"),
        Website_Visits=("website_visits", "sum"),
        Clicks=("Clicks", "sum"),
        Impressions=("Impressions", "sum")
    )
    .reset_index()
)

customer_analysis["Conversion_Rate"] = (
    customer_analysis["Conversions"] * 100 /
    customer_analysis["Clicks"]
)

# --------------------------------------------------
# CUSTOMER SEGMENT TABLE
# --------------------------------------------------

st.markdown("### 📊 Customer Segment Performance")

st.dataframe(
    customer_analysis[
        [
            "Customer_Segment",
            "Revenue",
            "Conversions",
            "Website_Visits",
            "Conversion_Rate"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# REVENUE BY CUSTOMER SEGMENT
# --------------------------------------------------

st.markdown("### 💰 Revenue by Customer Segment")

fig_customer_revenue = px.bar(
    customer_analysis.sort_values(
        "Revenue",
        ascending=False
    ),
    x="Customer_Segment",
    y="Revenue",
    title="Revenue by Customer Segment",
    text_auto=".2s"
)

fig_customer_revenue.update_layout(
    xaxis_title="Customer Segment",
    yaxis_title="Revenue (₹)"
)

st.plotly_chart(
    fig_customer_revenue,
    use_container_width=True
)

# --------------------------------------------------
# CONVERSION RATE BY CUSTOMER SEGMENT
# --------------------------------------------------

st.markdown("### 🎯 Conversion Rate by Customer Segment")

fig_customer_conversion = px.bar(
    customer_analysis.sort_values(
        "Conversion_Rate",
        ascending=False
    ),
    x="Customer_Segment",
    y="Conversion_Rate",
    title="Conversion Rate by Customer Segment",
    text_auto=".2f"
)

fig_customer_conversion.update_layout(
    xaxis_title="Customer Segment",
    yaxis_title="Conversion Rate (%)"
)

st.plotly_chart(
    fig_customer_conversion,
    use_container_width=True
)

# ==================================================
# TARGET AUDIENCE ANALYSIS
# ==================================================

st.markdown("## 🎯 Target Audience Analysis")

# --------------------------------------------------
# TARGET AUDIENCE FILTER
# --------------------------------------------------

audience_options = sorted(
    df["Target_Audience"].dropna().unique()
)

selected_audiences = st.multiselect(
    "Select Target Audiences",
    options=audience_options,
    default=audience_options
)

audience_df = filtered_df[
    filtered_df["Target_Audience"].isin(selected_audiences)
]

# --------------------------------------------------
# TARGET AUDIENCE ANALYSIS
# --------------------------------------------------

audience_analysis = (
    audience_df
    .groupby("Target_Audience")
    .agg(
        Revenue=("Revenue", "sum"),
        Conversions=("Conversions", "sum"),
        Website_Visits=("website_visits", "sum"),
        Clicks=("Clicks", "sum"),
        Impressions=("Impressions", "sum")
    )
    .reset_index()
)

audience_analysis["Conversion_Rate"] = (
    audience_analysis["Conversions"] * 100 /
    audience_analysis["Clicks"]
)

# --------------------------------------------------
# TARGET AUDIENCE TABLE
# --------------------------------------------------

st.markdown("### 📊 Target Audience Performance")

st.dataframe(
    audience_analysis[
        [
            "Target_Audience",
            "Revenue",
            "Conversions",
            "Website_Visits",
            "Conversion_Rate"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# REVENUE BY TARGET AUDIENCE
# --------------------------------------------------

st.markdown("### 💰 Revenue by Target Audience")

fig_audience_revenue = px.bar(
    audience_analysis.sort_values(
        "Revenue",
        ascending=False
    ),
    x="Target_Audience",
    y="Revenue",
    title="Revenue by Target Audience",
    text_auto=".2s"
)

fig_audience_revenue.update_layout(
    xaxis_title="Target Audience",
    yaxis_title="Revenue (₹)"
)

st.plotly_chart(
    fig_audience_revenue,
    use_container_width=True
)

# --------------------------------------------------
# CONVERSION RATE BY TARGET AUDIENCE
# --------------------------------------------------

st.markdown("### 🎯 Conversion Rate by Target Audience")

fig_audience_conversion = px.bar(
    audience_analysis.sort_values(
        "Conversion_Rate",
        ascending=False
    ),
    x="Target_Audience",
    y="Conversion_Rate",
    title="Conversion Rate by Target Audience",
    text_auto=".2f"
)

fig_audience_conversion.update_layout(
    xaxis_title="Target Audience",
    yaxis_title="Conversion Rate (%)"
)

st.plotly_chart(
    fig_audience_conversion,
    use_container_width=True
)

# ==================================================
# CAMPAIGN ANALYSIS
# ==================================================

st.markdown("---")
st.title("📣 Campaign Performance Analysis")

st.write(
    "Analyze individual campaign performance and compare "
    "different campaign types."
)

# --------------------------------------------------
# CAMPAIGN TYPE FILTER
# --------------------------------------------------

campaign_type_options = sorted(
    df["Campaign_Type"].dropna().unique()
)

selected_campaign_types = st.multiselect(
    "Select Campaign Types",
    options=campaign_type_options,
    default=campaign_type_options
)

campaign_df = filtered_df[
    filtered_df["Campaign_Type"].isin(selected_campaign_types)
]

# --------------------------------------------------
# CAMPAIGN PERFORMANCE
# --------------------------------------------------

campaign_analysis = (
    campaign_df
    .groupby("Campaign_ID")
    .agg(
        Revenue=("Revenue", "sum"),
        Acquisition_Cost=("Acquisition_Cost", "sum"),
        Conversions=("Conversions", "sum"),
        Clicks=("Clicks", "sum"),
        Impressions=("Impressions", "sum"),
        Leads=("Leads", "sum")
    )
    .reset_index()
)

campaign_analysis["Conversion_Rate"] = (
    campaign_analysis["Conversions"] * 100 /
    campaign_analysis["Clicks"]
)

campaign_analysis["ROAS"] = (
    campaign_analysis["Revenue"] /
    campaign_analysis["Acquisition_Cost"]
)

campaign_analysis["ROI"] = (
    (campaign_analysis["Revenue"] -
     campaign_analysis["Acquisition_Cost"]) * 100 /
    campaign_analysis["Acquisition_Cost"]
)

# --------------------------------------------------
# TOP 10 CAMPAIGNS BY REVENUE
# --------------------------------------------------

st.markdown("### 💰 Top 10 Campaigns by Revenue")

top_revenue_campaigns = (
    campaign_analysis
    .sort_values("Revenue", ascending=False)
    .head(10)
)

fig_top_revenue = px.bar(
    top_revenue_campaigns.sort_values("Revenue"),
    x="Revenue",
    y="Campaign_ID",
    orientation="h",
    title="Top 10 Campaigns by Revenue",
    text_auto=".2s"
)

fig_top_revenue.update_layout(
    xaxis_title="Revenue (₹)",
    yaxis_title="Campaign ID"
)

st.plotly_chart(
    fig_top_revenue,
    use_container_width=True
)

# --------------------------------------------------
# TOP 10 CAMPAIGNS BY CONVERSIONS
# --------------------------------------------------

st.markdown("### 🎯 Top 10 Campaigns by Conversions")

top_conversion_campaigns = (
    campaign_analysis
    .sort_values("Conversions", ascending=False)
    .head(10)
)

fig_top_conversions = px.bar(
    top_conversion_campaigns.sort_values("Conversions"),
    x="Conversions",
    y="Campaign_ID",
    orientation="h",
    title="Top 10 Campaigns by Conversions",
    text_auto=".2s"
)

fig_top_conversions.update_layout(
    xaxis_title="Conversions",
    yaxis_title="Campaign ID"
)

st.plotly_chart(
    fig_top_conversions,
    use_container_width=True
)

# --------------------------------------------------
# CAMPAIGN TYPE ANALYSIS
# --------------------------------------------------

campaign_type_analysis = (
    campaign_df
    .groupby("Campaign_Type")
    .agg(
        Revenue=("Revenue", "sum"),
        Acquisition_Cost=("Acquisition_Cost", "sum"),
        Conversions=("Conversions", "sum"),
        Clicks=("Clicks", "sum"),
        Impressions=("Impressions", "sum")
    )
    .reset_index()
)

campaign_type_analysis["Conversion_Rate"] = (
    campaign_type_analysis["Conversions"] * 100 /
    campaign_type_analysis["Clicks"]
)

campaign_type_analysis["ROAS"] = (
    campaign_type_analysis["Revenue"] /
    campaign_type_analysis["Acquisition_Cost"]
)

campaign_type_analysis["ROI"] = (
    (campaign_type_analysis["Revenue"] -
     campaign_type_analysis["Acquisition_Cost"]) * 100 /
    campaign_type_analysis["Acquisition_Cost"]
)

# --------------------------------------------------
# CAMPAIGN TYPE TABLE
# --------------------------------------------------

st.markdown("### 📊 Campaign Type Performance")

st.dataframe(
    campaign_type_analysis[
        [
            "Campaign_Type",
            "Revenue",
            "Acquisition_Cost",
            "Conversions",
            "Conversion_Rate",
            "ROAS",
            "ROI"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# REVENUE BY CAMPAIGN TYPE
# --------------------------------------------------

st.markdown("### 💰 Revenue by Campaign Type")

fig_campaign_revenue = px.bar(
    campaign_type_analysis.sort_values(
        "Revenue",
        ascending=False
    ),
    x="Campaign_Type",
    y="Revenue",
    title="Revenue by Campaign Type",
    text_auto=".2s"
)

fig_campaign_revenue.update_layout(
    xaxis_title="Campaign Type",
    yaxis_title="Revenue (₹)"
)

st.plotly_chart(
    fig_campaign_revenue,
    use_container_width=True
)

# --------------------------------------------------
# CONVERSION RATE BY CAMPAIGN TYPE
# --------------------------------------------------

st.markdown("### 🎯 Conversion Rate by Campaign Type")

fig_campaign_conversion = px.bar(
    campaign_type_analysis.sort_values(
        "Conversion_Rate",
        ascending=False
    ),
    x="Campaign_Type",
    y="Conversion_Rate",
    title="Conversion Rate by Campaign Type",
    text_auto=".2f"
)

fig_campaign_conversion.update_layout(
    xaxis_title="Campaign Type",
    yaxis_title="Conversion Rate (%)"
)

st.plotly_chart(
    fig_campaign_conversion,
    use_container_width=True
)

# --------------------------------------------------
# ROAS BY CAMPAIGN TYPE
# --------------------------------------------------

st.markdown("### 📈 ROAS by Campaign Type")

fig_campaign_roas = px.bar(
    campaign_type_analysis.sort_values(
        "ROAS",
        ascending=False
    ),
    x="Campaign_Type",
    y="ROAS",
    title="ROAS by Campaign Type",
    text_auto=".2f"
)

fig_campaign_roas.update_layout(
    xaxis_title="Campaign Type",
    yaxis_title="ROAS"
)

st.plotly_chart(
    fig_campaign_roas,
    use_container_width=True
)

# ==================================================
# GEOGRAPHIC / CITY ANALYSIS
# ==================================================

st.markdown("---")
st.title("📍 Geographic & City Performance")

st.write(
    "Analyze marketing performance across Indian cities "
    "using revenue, conversions and conversion rate."
)

# --------------------------------------------------
# CITY FILTER
# --------------------------------------------------

city_options = sorted(
    df["Indian_Cities"].dropna().unique()
)

selected_cities = st.multiselect(
    "Select Cities",
    options=city_options,
    default=city_options
)

city_df = filtered_df[
    filtered_df["Indian_Cities"].isin(selected_cities)
]

# --------------------------------------------------
# CITY PERFORMANCE
# --------------------------------------------------

city_analysis = (
    city_df
    .groupby("Indian_Cities")
    .agg(
        Revenue=("Revenue", "sum"),
        Acquisition_Cost=("Acquisition_Cost", "sum"),
        Conversions=("Conversions", "sum"),
        Clicks=("Clicks", "sum"),
        Impressions=("Impressions", "sum"),
        Website_Visits=("website_visits", "sum")
    )
    .reset_index()
)

city_analysis["Conversion_Rate"] = (
    city_analysis["Conversions"] * 100 /
    city_analysis["Clicks"]
)

city_analysis["ROAS"] = (
    city_analysis["Revenue"] /
    city_analysis["Acquisition_Cost"]
)

# --------------------------------------------------
# CITY PERFORMANCE TABLE
# --------------------------------------------------

st.markdown("### 📊 City Performance Summary")

st.dataframe(
    city_analysis[
        [
            "Indian_Cities",
            "Revenue",
            "Conversions",
            "Website_Visits",
            "Conversion_Rate",
            "ROAS"
        ]
    ].sort_values(
        "Revenue",
        ascending=False
    ),
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# TOP 10 CITIES BY REVENUE
# --------------------------------------------------

st.markdown("### 💰 Top 10 Cities by Revenue")

top_cities_revenue = (
    city_analysis
    .sort_values("Revenue", ascending=False)
    .head(10)
)

fig_city_revenue = px.bar(
    top_cities_revenue.sort_values("Revenue"),
    x="Revenue",
    y="Indian_Cities",
    orientation="h",
    title="Top 10 Cities by Revenue",
    text_auto=".2s"
)

fig_city_revenue.update_layout(
    xaxis_title="Revenue (₹)",
    yaxis_title="City"
)

st.plotly_chart(
    fig_city_revenue,
    use_container_width=True
)

# --------------------------------------------------
# TOP 10 CITIES BY CONVERSIONS
# --------------------------------------------------

st.markdown("### 🎯 Top 10 Cities by Conversions")

top_cities_conversions = (
    city_analysis
    .sort_values("Conversions", ascending=False)
    .head(10)
)

fig_city_conversions = px.bar(
    top_cities_conversions.sort_values("Conversions"),
    x="Conversions",
    y="Indian_Cities",
    orientation="h",
    title="Top 10 Cities by Conversions",
    text_auto=".2s"
)

fig_city_conversions.update_layout(
    xaxis_title="Conversions",
    yaxis_title="City"
)

st.plotly_chart(
    fig_city_conversions,
    use_container_width=True
)

# --------------------------------------------------
# CONVERSION RATE BY CITY
# --------------------------------------------------

st.markdown("### 📈 Conversion Rate by City")

top_cities_rate = (
    city_analysis
    .sort_values("Conversion_Rate", ascending=False)
    .head(10)
)

fig_city_rate = px.bar(
    top_cities_rate.sort_values("Conversion_Rate"),
    x="Conversion_Rate",
    y="Indian_Cities",
    orientation="h",
    title="Top 10 Cities by Conversion Rate",
    text_auto=".2f"
)

fig_city_rate.update_layout(
    xaxis_title="Conversion Rate (%)",
    yaxis_title="City"
)

st.plotly_chart(
    fig_city_rate,
    use_container_width=True
)
