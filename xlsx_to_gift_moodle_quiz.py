#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd
import os
import base64
from PIL import Image

def file_downloader(filename, file_label='File'):
    with open(filename, 'rb') as f:
        data = f.read()

st.title('Moodleクイズ変換君')
st.text('一行目に列ラベル，一列目に問題文，二列目に正答，三列目以降に誤答が入った\nエクセルファイルをGIFTフォーマットに変換します．')
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

    b64 = base64.b64encode(txt.encode()).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="GIFT_format.txt">download</a>'
    st.markdown(f"変換完了 ダウンロードする {href}", unsafe_allow_html=True)
else:
    st.warning("you need to upload a XLSX file.")
