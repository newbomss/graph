
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

st.set_page_config(layout="wide")
st.title("지역별 부동산 시장 그래프 생성기")

uploaded_main = st.file_uploader("매수/매도 우위 데이터 CSV 파일 업로드", type="csv")
uploaded_trade = st.file_uploader("매매거래지수 CSV 파일 업로드", type="csv")

if uploaded_main and uploaded_trade:
    df_main = pd.read_csv(uploaded_main)
    df_trade = pd.read_csv(uploaded_trade)

    # 날짜 시리즈 생성
    date_series = pd.to_datetime(df_main.iloc[3:, 0], errors="coerce")
    filtered_indices = date_series >= pd.Timestamp("2012-01-01")
    region_labels = df_main.iloc[0, 1::3].dropna().tolist()

    region = st.selectbox("지역 선택", region_labels)

    # 매수/매도 데이터 처리
    try:
        region_idx = df_main.iloc[0, :].tolist().index(region)
        region_df = df_main.iloc[3:, [region_idx, region_idx+1, region_idx+2]].copy()
        region_df.columns = ["매도자많음", "매수자많음", "매수우위지수"]
        region_df["Date"] = date_series
        region_df = region_df[filtered_indices]
        region_df = region_df.dropna()
        region_df["매도자많음"] = pd.to_numeric(region_df["매도자많음"], errors="coerce")
        region_df["매수자많음"] = pd.to_numeric(region_df["매수자많음"], errors="coerce")
        region_df["매수우위지수"] = pd.to_numeric(region_df["매수우위지수"], errors="coerce")
        region_df = region_df.dropna()

        # 매매거래지수 처리
        trade_idx = df_trade.iloc[0, :].tolist().index(region) + 1
        trade_series = pd.to_numeric(df_trade.iloc[3:, trade_idx], errors="coerce")[filtered_indices].reset_index(drop=True)
        trade_dates = pd.to_datetime(df_trade.iloc[3:, 0], errors="coerce")[filtered_indices].reset_index(drop=True)
        trade_df = pd.DataFrame({"Date": trade_dates, "매매거래지수": trade_series}).dropna()

        # 병합
        region_df = region_df.reset_index(drop=True)
        plot_df = pd.merge(region_df, trade_df, on="Date", how="inner")

        # 그래프 출력
        fig, ax = plt.subplots(figsize=(14, 6))
        ax.fill_between(plot_df["Date"].values, plot_df["매매거래지수"].values, color="gray", alpha=0.3, label="매매거래지수")
        ax.plot(plot_df["Date"], plot_df["매도자많음"], label="매도자 많음", color="blue")
        ax.plot(plot_df["Date"], plot_df["매수자많음"], label="매수자 많음", color="red")
        ax.plot(plot_df["Date"], plot_df["매수우위지수"], label="매수우위지수", color="limegreen")
        ax.set_title(f"{region} 부동산 시장 지표 (2012년~)")
        ax.set_xlabel("날짜")
        ax.set_ylabel("지표 값")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

    except Exception as e:
        st.error(f"오류 발생: {e}")
