
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import io

# 한글 폰트 설정 (Windows 기준)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(layout="wide")
st.title("📊 엑셀 기반 부동산 그래프 자동 생성기")

uploaded_excel = st.file_uploader("📁 부동산 관련 엑셀 파일 업로드", type=["xlsx", "xls"])

if uploaded_excel:
    # 시트 목록 선택
    xls = pd.ExcelFile(uploaded_excel)
    sheet_names = xls.sheet_names
    selected_sheet = st.selectbox("📄 시트를 선택하세요", sheet_names)

    # 시트 불러오기
    df_main = pd.read_excel(uploaded_excel, sheet_name=selected_sheet)

    # 날짜 추출
    date_series = pd.to_datetime(df_main.iloc[3:, 0], errors="coerce")
    filtered_indices = date_series >= pd.Timestamp("2012-01-01")
    region_labels = df_main.iloc[0, 1::3].dropna().tolist()

    # 지역 선택
    region = st.selectbox("📍 분석할 지역 선택", region_labels)

    # 그래프 처리
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

        # 그래프 출력
        fig, ax = plt.subplots(figsize=(14, 6))
        ax.plot(region_df["Date"], region_df["매도자많음"], label="매도자 많음", color="blue")
        ax.plot(region_df["Date"], region_df["매수자많음"], label="매수자 많음", color="red")
        ax.plot(region_df["Date"], region_df["매수우위지수"], label="매수우위지수", color="limegreen")
        ax.set_title(f"{region} 부동산 시장 지표 (2012년~)")
        ax.set_xlabel("날짜")
        ax.set_ylabel("지표 값")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

        # CSV 변환 및 다운로드
        csv = region_df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="💾 이 데이터 CSV로 저장하기",
            data=csv,
            file_name=f"{region}_지표.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"⚠️ 오류 발생: {e}")
