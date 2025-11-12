import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# Page config
st.set_page_config(page_title="Solar Dashboard", layout="wide")

# Title
st.title("🌞 Cross-Country Solar Data Dashboard")

# Load cleaned CSVs
benin = pd.read_csv('./data/benin_clean.csv', parse_dates=['Timestamp'])
sierra = pd.read_csv('./data/sierraleone_clean.csv', parse_dates=['Timestamp'])
togo = pd.read_csv('./data/togo_clean.csv', parse_dates=['Timestamp'])

# Add country column
benin['country'] = 'Benin'
sierra['country'] = 'SierraLeone'
togo['country'] = 'Togo'

# Combine datasets
combined_df = pd.concat([benin, sierra, togo], ignore_index=True)
combined_df = combined_df[['Timestamp', 'GHI', 'DNI', 'DHI', 'country']]

# Sidebar: Select country
selected_country = st.sidebar.multiselect(
    "Select country(s):",
    options=combined_df['country'].unique(),
    default=combined_df['country'].unique()
)

# Sidebar: Date range filter
min_date = combined_df['Timestamp'].min()
max_date = combined_df['Timestamp'].max()
start_date, end_date = st.sidebar.date_input(
    "Select date range:",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Filter data
filtered_df = combined_df[
    (combined_df['country'].isin(selected_country)) &
    (combined_df['Timestamp'].dt.date >= start_date) &
    (combined_df['Timestamp'].dt.date <= end_date)
]

# Tabs
tab1, tab2, tab3 = st.tabs(["📈 Time Series", "📊 Distribution", "🏆 Country Ranking"])

# ----------------- Tab 1: Time Series -----------------
with tab1:
    st.subheader("GHI over Time")
    fig, ax = plt.subplots(figsize=(10,4))
    for country in selected_country:
        country_data = filtered_df[filtered_df['country'] == country]
        ax.plot(country_data['Timestamp'], country_data['GHI'], label=country, alpha=0.7)
    ax.set_ylabel("GHI (W/m²)")
    ax.set_xlabel("Timestamp")
    ax.legend()
    st.pyplot(fig)

# ----------------- Tab 2: Distribution -----------------
with tab2:
    st.subheader("Distribution of GHI, DNI, DHI")
    metrics = ['GHI', 'DNI', 'DHI']
    for metric in metrics:
        fig, ax = plt.subplots(figsize=(6,4))
        filtered_df.boxplot(column=metric, by='country', ax=ax)
        ax.set_title(f'{metric} Distribution')
        ax.set_xlabel("Country")
        ax.set_ylabel(f'{metric} (W/m²)')
        st.pyplot(fig)

# ----------------- Tab 3: Country Ranking -----------------
with tab3:
    st.subheader("Average GHI Ranking")
    avg_ghi = filtered_df.groupby('country')['GHI'].mean().sort_values(ascending=False)
    st.dataframe(avg_ghi.round(2))

    # Bar chart
    fig, ax = plt.subplots(figsize=(6,4))
    avg_ghi.plot(kind='bar', color='skyblue', ax=ax)
    ax.set_ylabel("Average GHI (W/m²)")
    ax.set_xlabel("Country")
    ax.set_title("Average GHI by Country")
    st.pyplot(fig)