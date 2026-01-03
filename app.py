import streamlit as st
import pandas as pd

# 구글 시트 링크 (기존 것 그대로 사용)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1BxxUZkaEQIRArzKSAe24hTC0frxPEOivJ4ZCYqfH7-E"
# 탭(워크시트) 이름별로 데이터를 가져오는 주소 설정
FIRE_URL = f"{SHEET_URL}/export?format=csv&gid=0"
TOWN_URL = f"{SHEET_URL}/export?format=csv&gid=611290830"

st.set_page_config(page_title="총무 시스템", layout="wide")

# 사이드바에서 모임 선택
st.sidebar.header("📂 관리 모임 선택")
mode = st.sidebar.radio("어느 장부를 보실까요?", ["소방대", "마을"])

# 선택된 모임에 따라 데이터 주소 변경
current_url = FIRE_URL if mode == "소방대" else TOWN_URL

@st.cache_data(ttl=10)
def load_data(url):
    return pd.read_csv(url)

try:
    df = load_data(current_url)
    st.title(f"📒 {mode} 결산 시스템")
   
    # 이 아래는 기존 코드와 동일 (요약 대시보드 및 표 출력)
    total_in = df['수입'].sum()
    total_out = df['지출'].sum()
    balance = total_in - total_out
   
    col1, col2, col3 = st.columns(3)
    col1.metric("총 수입", f"{total_in:,.0f}원")
    col2.metric("총 지출", f"{total_out:,.0f}원")
    col3.metric("현재 잔액", f"{balance:,.0f}원")
   
    st.divider()
    st.subheader(f"📋 {mode} 상세 내역")
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"'{mode}' 탭을 찾을 수 없거나 데이터가 비어있습니다. 구글 시트의 탭 이름을 확인해주세요.")
