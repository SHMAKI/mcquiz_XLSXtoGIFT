#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd
import os
import base64
from PIL import Image
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb

# def file_downloader(filename, file_label='File'):
#     with open(filename, 'rb') as f:
#         data = f.read()

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data

st.title('Moodleクイズ変換君')
st.text('一行目に列ラベル，一列目に問題文，二列目に正答，三列目以降に誤答が入った\nエクセルファイルをGIFTフォーマットに変換します．')

df_sample = pd.DataFrame(data=[["日本一高い山は？", "富士山","天保山","八ヶ岳","北岳","桜島",],
                              ["日本一面積が広い県は？", "岩手県","長野県","静岡県","沖縄県","北海道",]],
                         columns=["問題文", "正答", "誤答１", "誤答２", "誤答３", "誤答４",])
df_xlsx = to_excel(df_sample)

st.download_button(label='📥 Download sample xlsx',
                                data=df_xlsx ,
                                file_name= 'sample.xlsx')
# b64_df = base64.b64encode(xlsx.encode()).decode()
# href = f'<a href="data:application/octet-stream;base64,{b64_df}" download="sample.xlsx">download</a>'
# st.markdown(f"サンプルxlsxファイルをダウンロードする： {href}", unsafe_allow_html=True)

image = Image.open("img/sample.png")
st.image(image, caption="sample", use_column_width=True)

uploaded_file = st.file_uploader("Choose a XLSX file", type="xlsx")

if uploaded_file is not None:
    #read csv
    #df=pd.read_csv(uploaded_file, encoding="utf8", errors='ignore')
    #read xls or xlsx
    df=pd.read_excel(uploaded_file)#, encoding="utf8", errors='ignore')
    st.success('データ変換を開始します．')
    st.dataframe(df)
    #st.table(df)
    txt = ""
    for i in range(df.shape[0]):
        txt = txt +"::"+str(i+1)+"::"+df.iloc[i,0]+"{\n"
        txt = txt +"="+df.iloc[i,1]+"\n"
        for j in range(2, df.shape[1]):
            txt = txt +"~"+df.iloc[i,j]+"\n"
        txt = txt +"}\n\n"

    #b64 = base64.b64encode(txt.encode()).decode()
    #href = f'<a href="data:application/octet-stream;base64,{b64}" download="GIFT_format.txt">download</a>'
    #st.markdown(f"GIFTフォーマットのテキストをダウンロードする： {href}", unsafe_allow_html=True)
    st.download_button(label='📥 Download GIFT format txt',
                                data=txt,
                                file_name= 'GIFT_format.txt')
else:
    st.warning("you need to upload a XLSX file.")
