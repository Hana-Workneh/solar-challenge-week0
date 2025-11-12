import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("🌞 Cross-Country Solar Data Dashboard")

st.markdown("""
Upload your cleaned CSV files for **Benin**, **Sierra Leone**, and **Togo** below.
Make sure each CSV includes a `Timestamp` column.
""")

# File uploaders for the three datasets
benin_file = st.file_uploader("📂 Upload Benin Cleaned CSV", type=["csv"])
sierra_file = st.file_uploader("📂 Upload Sierra Leone Cleaned CSV", type=["csv"])
togo_file = st.file_uploader("📂 Upload Togo Cleaned CSV", type=["csv"])

dfs = []

# Read Benin file
if benin_file is not None:
    benin_df = pd.read_csv(benin_file, parse_dates=['Timestamp'])
    benin_df["country"] = "Benin"
    dfs.append(benin_df)
    st.success(f"✅ Benin dataset loaded ({benin_df.shape[0]} rows)")

# Read Sierra Leone file
if sierra_file is not None:
    sierra_df = pd.read_csv(sierra_file, parse_dates=['Timestamp'])
    sierra_df["country"] = "Sierra Leone"
    dfs.append(sierra_df)
    st.success(f"✅ Sierra Leone dataset loaded ({sierra_df.shape[0]} rows)")

# Read Togo file
if togo_file is not None:
    togo_df = pd.read_csv(togo_file, parse_dates=['Timestamp'])
    togo_df["country"] = "Togo"
    dfs.append(togo_df)
    st.success(f"✅ Togo dataset loaded ({togo_df.shape[0]} rows)")

# If all 3 datasets are uploaded, combine and show analysis
if len(dfs) == 3:
    combined_df = pd.concat(dfs, ignore_index=True)
    
    st.write("### Combined Dataset Preview")
    st.dataframe(combined_df.head())

    st.sidebar.header("🔍 Filters")
    selected_countries = st.sidebar.multiselect(
        "Select country(s):", 
        options=combined_df['country'].unique(),
        default=combined_df['country'].unique(),
        key="country_select"
    )

    metric = st.sidebar.selectbox(
        "Select Metric to Visualize:",
        options=["GHI", "DNI", "DHI", "Tamb"]
    )

    filtered_df = combined_df[combined_df['country'].isin(selected_countries)]

    st.write(f"### 📊 Boxplot of {metric} by Country")
    fig, ax = plt.subplots(figsize=(8, 5))
    filtered_df.boxplot(column=metric, by="country", ax=ax, grid=False)
    plt.suptitle("")
    plt.title(f"{metric} Distribution by Country")
    st.pyplot(fig)

    # Summary statistics
    st.write("### 📈 Summary Statistics by Country")
    summary = filtered_df.groupby("country")[metric].agg(["mean", "median", "std"]).reset_index()
    st.dataframe(summary)

else:
    st.info("⬆️ Please upload all three datasets to begin analysis.")
