
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

st.set_page_config(layout="wide")
st.title("📊 Excel-based Real Estate Graph Generator (EN Version)")

uploaded_excel = st.file_uploader("📁 Upload your real estate Excel file", type=["xlsx", "xls"])

if uploaded_excel:
    # 시트 자동 선택: "7.매수매도-표 1"
    fixed_sheet_name = "7.매수매도-표 1"

    try:
        xls = pd.ExcelFile(uploaded_excel)
        df_main = pd.read_excel(xls, sheet_name=fixed_sheet_name)

        date_series = pd.to_datetime(df_main.iloc[3:, 0], errors="coerce")
        filtered_indices = date_series >= pd.Timestamp("2012-01-01")
        region_labels = df_main.iloc[0, 1::3].dropna().tolist()
        region = st.selectbox("📍 Select a region", region_labels)

        region_idx = df_main.iloc[0, :].tolist().index(region)
        region_df = df_main.iloc[3:, [region_idx, region_idx+1, region_idx+2]].copy()
        region_df.columns = ["Sellers", "Buyers", "Buyer Index"]
        region_df["Date"] = date_series
        region_df = region_df[filtered_indices]
        region_df = region_df.dropna()
        region_df["Sellers"] = pd.to_numeric(region_df["Sellers"], errors="coerce")
        region_df["Buyers"] = pd.to_numeric(region_df["Buyers"], errors="coerce")
        region_df["Buyer Index"] = pd.to_numeric(region_df["Buyer Index"], errors="coerce")
        region_df = region_df.dropna()

        fig, ax = plt.subplots(figsize=(14, 6))
        ax.plot(region_df["Date"], region_df["Sellers"], label="Sellers", color="blue")
        ax.plot(region_df["Date"], region_df["Buyers"], label="Buyers", color="red")
        ax.plot(region_df["Date"], region_df["Buyer Index"], label="Buyer Index", color="limegreen")
        ax.set_title(f"{region} Real Estate Market Index (2012~)")
        ax.set_xlabel("Date")
        ax.set_ylabel("Value")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

        csv = region_df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("💾 Download this data as CSV", data=csv,
                           file_name=f"{region}_index.csv", mime="text/csv")
    except Exception as e:
        st.error(f"⚠️ Error: {e}")
