import streamlit as st
import pandas as pd
from datetime import datetime

# ⚠️ 여기에 아까 복사한 구글 시트 링크를 붙여넣으세요!
SHEET_URL = "https://docs.google.com/spreadsheets/d/1BxxUZkaEQIRArzKSAe24hTC0frxPEOivJ4ZCYqfH7-E/edit?gid=0#gid=0"
CSV_URL = SHEET_URL.replace('/edit?usp=sharing', '/export?format=csv')

st.set_page_config(page_title="의용소방대 스마트 장부", layout="wide")
st.title("📂 의용소방대 & 마을 총무 결산 시스템")

# 데이터 불러오기 함수
@st.cache_data(ttl=60)
def load_data():
    return pd.read_csv(CSV_URL)

try:
    df = load_data()
    df['날짜'] = pd.to_datetime(df['날짜'])
    
    # 요약 정보
    total_in = df['수입'].sum()
    total_out = df['지출'].sum()
    balance = total_in - total_out
    
    col1, col2, col3 = st.columns(3)
    col1.metric("총 수입", f"{total_in:,.0f}원")
    col2.metric("총 지출", f"{total_out:,.0f}원")
    col3.metric("현재 잔액", f"{balance:,.0f}원")

    st.divider()

    # 메뉴 선택
    menu = st.sidebar.selectbox("메뉴", ["감사용 상세내역", "회원 보고용 요약"])

    if menu == "감사용 상세내역":
        st.subheader("📋 상세 금전출납부")
        st.dataframe(df.sort_values(by="날짜", ascending=False), use_container_width=True)
        csv_data = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 엑셀(CSV) 다운로드", csv_data, "감사보고서.csv")

    elif menu == "회원 보고용 요약":
        st.subheader("📊 지출 항목별 비중")
        exp_df = df[df['지출'] > 0].groupby('항목')['지출'].sum()
        if not exp_df.empty:
            st.pie_chart(exp_df)
        else:
            st.info("지출 내역이 없습니다.")

except Exception as e:
    st.error("구글 시트 연결을 확인해주세요. 공유 설정이 '링크가 있는 모든 사용자(뷰어)'여야 합니다.")
