import streamlit as st
from PIL import Image
import exchange_rate

# 사이드바 화면
st.sidebar.header("로그인")
user_id = st.sidebar.text_input('아이디(ID) 입력', value="streamlit", max_chars=15)
user_password = st.sidebar.text_input('패스워드(Password) 입력', value="", type="password")

if user_id == 'admin' and user_password == '1234':

    st.sidebar.header("Exchange_rate Project")
    selectbox_options = ['환율조회', '데이터분석'] # 셀렉트 박스의 선택 항목
    your_option = st.sidebar.selectbox('Menu', selectbox_options) # 셀렉트박스의 항목 선택 결과
    st.sidebar.write('**당신의 선택**:', your_option)

    if your_option == '환율조회':
        st.subheader('환율조회')
        exchange_rate.fx_rate()

    elif your_option == '데이터분석':
        st.subheader('데이터분석')

    else:
        pass


    
