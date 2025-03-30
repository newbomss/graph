import os
import requests
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

# ✅ GitHub에서 폰트 자동 다운로드
font_url = "https://raw.githubusercontent.com/newbomss/graph/main/NanumGothic.ttf"
font_path = "NanumGothic.ttf"

headers = {'User-Agent': 'Mozilla/5.0'}

if not os.path.exists(font_path):
    response = requests.get(font_url, headers=headers)
    if response.status_code == 200:
        with open(font_path, 'wb') as f:
            f.write(response.content)
    else:
        st.error(f"폰트 파일 다운로드 실패! 상태 코드: {response.status_code}")

# ✅ 폰트 등록
if os.path.exists(font_path):
    try:
        fm.fontManager.addfont(font_path)
        plt.rcParams['font.family'] = 'NanumGothic'
    except Exception as e:
        st.warning(f"폰트 등록 중 오류 발생: {e}")
        plt.rcParams['font.family'] = 'sans-serif'
else:
    st.warning("폰트 파일이 없어서 기본 폰트를 사용합니다.")
    plt.rcParams['font.family'] = 'sans-serif'

# Streamlit 앱
st.title("엑셀 그래프 시각화")

uploaded_file = st.file_uploader("엑셀 파일 업로드", type=["xlsx"])
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    st.write("데이터 미리보기:")
    st.dataframe(df)

    st.write("그래프:")
    fig, ax = plt.subplots()
    df.plot(ax=ax)
    st.pyplot(fig)
