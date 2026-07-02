import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Marketing Funnel Dashboard",
    layout="wide"
)

st.title("Marketing Funnel & Conversion Performance Dashboard")

df = pd.read_csv("bank-full.csv", sep=";")

df["Conversion"] = df["y"].map({
    "yes": 1,
    "no": 0
})

st.sidebar.header("Filters")

job_filter = st.sidebar.multiselect(
    "Job",
    sorted(df["job"].unique()),
    default=sorted(df["job"].unique())
)

month_filter = st.sidebar.multiselect(
    "Month",
    sorted(df["month"].unique()),
    default=sorted(df["month"].unique())
)

contact_filter = st.sidebar.multiselect(
    "Contact Type",
    sorted(df["contact"].unique()),
    default=sorted(df["contact"].unique())
)

filtered = df[
    (df["job"].isin(job_filter)) &
    (df["month"].isin(month_filter)) &
    (df["contact"].isin(contact_filter))
]

total_customers = len(filtered)
converted = filtered["Conversion"].sum()
not_converted = total_customers - converted
conversion_rate = converted / total_customers * 100
avg_campaign = filtered["campaign"].mean()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Customers Contacted", f"{total_customers:,}")
c2.metric("Converted Customers", f"{converted:,}")
c3.metric("Conversion Rate", f"{conversion_rate:.2f}%")
c4.metric("Avg Campaign Contacts", f"{avg_campaign:.2f}")

st.markdown("---")

funnel_df = pd.DataFrame({
    "Stage": ["Contacted", "Converted"],
    "Count": [total_customers, converted]
})

fig1 = px.funnel(
    funnel_df,
    x="Count",
    y="Stage",
    title="Marketing Funnel"
)

st.plotly_chart(fig1, use_container_width=True)

fig2 = px.pie(
    filtered,
    names="y",
    title="Conversion Distribution"
)

st.plotly_chart(fig2, use_container_width=True)

contact_conv = (
    filtered.groupby("contact")["Conversion"]
    .mean()
    .reset_index()
)

contact_conv["Conversion"] *= 100

fig3 = px.bar(
    contact_conv,
    x="contact",
    y="Conversion",
    title="Conversion Rate by Contact Type",
    labels={"Conversion": "Conversion Rate (%)"}
)

st.plotly_chart(fig3, use_container_width=True)

job_conv = (
    filtered.groupby("job")["Conversion"]
    .mean()
    .reset_index()
)

job_conv["Conversion"] *= 100

fig4 = px.bar(
    job_conv,
    x="job",
    y="Conversion",
    title="Conversion Rate by Job",
    labels={"Conversion": "Conversion Rate (%)"}
)

st.plotly_chart(fig4, use_container_width=True)

month_conv = (
    filtered.groupby("month")["Conversion"]
    .mean()
    .reset_index()
)

month_conv["Conversion"] *= 100

month_order = [
    "jan", "feb", "mar", "apr", "may", "jun",
    "jul", "aug", "sep", "oct", "nov", "dec"
]

month_conv["month"] = month_conv["month"].str.lower()

month_conv["month"] = pd.Categorical(
    month_conv["month"],
    categories=month_order,
    ordered=True
)

month_conv = month_conv.sort_values(by="month")

fig5 = px.line(
    month_conv,
    x="month",
    y="Conversion",
    markers=True,
    title="Conversion Rate by Month"
)

st.plotly_chart(fig5, use_container_width=True)

fig6 = px.histogram(
    filtered,
    x="age",
    color="y",
    nbins=30,
    title="Age Distribution by Conversion"
)

st.plotly_chart(fig6, use_container_width=True)

campaign_conv = (
    filtered.groupby("campaign")["Conversion"]
    .mean()
    .reset_index()
)

campaign_conv["Conversion"] *= 100

fig7 = px.scatter(
    campaign_conv,
    x="campaign",
    y="Conversion",
    title="Campaign Contacts vs Conversion Rate"
)

st.plotly_chart(fig7, use_container_width=True)

st.subheader("Dataset Preview")
st.dataframe(filtered.head(20))