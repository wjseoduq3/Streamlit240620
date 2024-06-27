from bs4 import BeautifulSoup
import requests

import pandas as pd  
import streamlit as st 
import matplotlib.pyplot as plt
import matplotlib
import time
import lxml

# from io import BytesIO

def fx_rate():

    def get_exchane(currency_code):

        # currency_code='USD'
        last_page_no= 10
        df = pd.DataFrame()

        for page_no in range(1, last_page_no+1):
            url=f"https://finance.naver.com/marketindex/exchangeDailyQuote.naver?marketindexCd=FX_{currency_code}KRW&page={page_no}"
            response = requests.get(url)
            html_content = response.content

            soup= BeautifulSoup(html_content, "html.parser")
            tables = soup.find_all('table')

            dfs = pd.read_html(str(tables[0]),header=1)
            time.sleep(0.5)

            # streamlit에서 하면 if 조건문 필요 없음
            # if dfs[0].empty:
            #     if (page_no==1):
            #         print(f"통화코드{currency_code}가 잘못 지정되었습니다.")
            #     else:
            #         print(f"{page_no} 마지막 페이지입니다.")
            #     break
            df = pd.concat([df, dfs[0]],ignore_index=False)

        return df

    currency_name_dict = {'미국 달러':'USD', '유럽연합 유로':'EUR', '일본 엔':'JPY', '중국 위안':'CNY'}
    # currency_name = st.sidebar.selectbox('통화선택', currency_name_dict.keys())
    # clicked = st.sidebar.button('환율데이터 가져오기')
    currency_name = st.selectbox('통화선택', currency_name_dict.keys())
    clicked = st.button('환율데이터 가져오기')

    if clicked:
        currency_code = currency_name_dict[currency_name]
        df_excange = get_exchane(currency_code)
        # print(df_excange)

        df_excange_rate = df_excange[['날짜','매매기준율','사실 때','받으실 때']]
        df_excange_rate2 = df_excange_rate.set_index('날짜')

        # df_excange_rate2.index = df_excange_rate2.index.astype(str)
        # df_excange_rate2.index = pd.to_datetime(df_excange_rate2.index, format='%Y-%m-%d')
        df_excange_rate2.index = pd.to_datetime(df_excange_rate2.index,format='%Y-%m-%d', errors='ignore')

        st.subheader(f"{currency_name} 환율 데이터")
        st.dataframe(df_excange_rate2.head(100))

        matplotlib.rcParams['font.family']='Malgun Gothic'
        # 차트 그리기
        ax = df_excange_rate2['매매기준율'].plot(figsize=(15,5),grid=True)
        ax.set_title('환율 매매기준율 그래프', fontsize=15)
        ax.set_xlabel('기간', fontsize=10)
        ax.set_xlabel(f'원화/{currency_name}', fontsize=10)
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        fig = ax.get_figure()
        st.pyplot(fig)

        # File Download
        st.text('** 환율 데이터파일 다운로드 **')
        csv_data = df_excange_rate.to_csv()

        excel_data = BytesIO()
        df_excange_rate.to_excel(excel_data)

        col = st.columns(2)
        with col[0]:
            st.download_button('CSV 파일 다운로드', csv_data, file_name='exchange_rate_data.csv')
        with col[1]:
            st.download_button('EXCEL 파일 다운로드', excel_data, file_name='exchange_rate_data.xlsx')
                

    # else:
    #     pass







