
import streamlit as st
import pandas as pd


st.header("varun ki duniya")
with st.sidebar:
  file = st.file_uploader("upload an excel file")
  if file is not None:
    try:
      all_sheets = pd.read_excel(file,sheet_name= None,header=None)
      #dictionary ki form arah ha data in all_sheets
      names = list(all_sheets.keys())
      st.write(all_sheets)
    except Exception as e:
      st.warning("something went wrong")
      st.text(f"error :{e}")
      