# import streamlit as st
# import pandas as pd

# st.header("Management Information System")
# with st.sidebar:
#     file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])

# if file is not None:
#     try:
#         df = pd.read_excel(file, header=None)  # Read without header
#         # Find the index of the row that contains the word "particular"
#         keyword = "particular"
#         target_index = None
          
#         for i, row in df.iterrows():
#             if row.astype(str).str.contains(keyword, case=False, na=False).any():
#                 target_index = i
#                 break

#         if target_index is not None:
#             # Set that row as column headers
#             df.columns = df.iloc[target_index]
#             # Drop all rows up to and including the header row
#             df = df.iloc[target_index + 1:].reset_index(drop=True)

#             st.subheader("Cleaned Data")
#             st.markdown("# print")
#             st.dataframe(df)
#         else:
#             st.warning(f"Could not find any row with keyword '{keyword}'.")

#     except Exception as e:
#         st.warning("Something went wrong")
#         st.text(f"Error: {e}")

# else:
#   st.warning("Please upload an excel file")





# import streamlit as st
# import pandas as pd
# import sqlite3 
# import re


# st.header("Management Information System")
# with st.sidebar:
#   file = st.file_uploader("Upload an Excel file")
  
# date_pattern = r"\b(?:\d{1,2}[-/thstndrd\s\.])?(?:\d{1,2}[-/\s\.])?(?:\d{2,4})\b"
# report_date = None

# if file is not None:
#     try:
#         df = pd.read_excel(file, header=None)
#         # st.subheader("Original Data")
#         # st.dataframe(df)
#         keyword = "particulars"
#         target_index = None
        
        
#         for i in range(10):
#         row = df.iloc[i].dropna().astype(str)
#         for val in row:
#             match = re.search(date_pattern, val)
#             if match:
#                 try:
#                     parsed_date = pd.to_datetime(match.group(), errors='coerce')
#                     if pd.notnull(parsed_date):
#                         report_date = parsed_date.date()
#                         break
#                 except:
#                     continue
#         if report_date:
#             break

#         for i, row in df.iterrows():
#             if row.astype(str).str.contains(keyword, case=False, na=False).any():
#                 target_index = i
#                 break

#         if target_index is not None:
#             df.columns = df.iloc[target_index]
#             df = df.iloc[target_index + 1:].reset_index(drop=True)

#         # st.subheader("Final Data")
#         # st.write(df)

#         # Now remove rows that contain "total" (case-insensitive) in any column
#         df = df[~df.apply(lambda row: row.astype(str).str.contains("total", case=False, na=False)).any(axis=1)]
#         df = df.drop('Total',axis=1)

#         st.subheader("Final Data")
#         st.write(df)
            
#         conn = sqlite3.connect('mis_data.db')  # Creates file in same directory
#         if st.button("Push to SQL"):
#           df.to_sql('mis_table', conn, if_exists='append', index=False)
#           conn.close()

#         st.success("Data saved to SQLite database successfully!")


#     except Exception as e:
#         st.warning("Something went wrong")
#         st.text(f"Error: {e}")



import streamlit as st
import pandas as pd
import sqlite3
import re

st.header("Management Information System")
with st.sidebar:
    file = st.file_uploader("Upload an Excel file")

# Regex pattern for date extraction
date_pattern = r"\b(?:\d{1,2}[-/thstndrd\s\.])?(?:\d{1,2}[-/\s\.])?(?:\d{2,4})\b"
report_date = None

if file is not None:
    try:
        df = pd.read_excel(file, header=None)
        
        # Detect date using regex in first 10 rows
        for i in range(10):
            row = df.iloc[i].dropna().astype(str)
            for val in row:
                match = re.search(date_pattern, val)
                if match:
                    try:
                        parsed_date = pd.to_datetime(match.group(), errors='coerce')
                        if pd.notnull(parsed_date):
                            report_date = parsed_date.date()
                            break
                    except:
                        continue
            if report_date:
                break

        st.write("📅 Report Date Detected:", report_date)

        # Find "particulars" row
        keyword = "particulars"
        target_index = None
        for i, row in df.iterrows():
            if row.astype(str).str.contains(keyword, case=False, na=False).any():
                target_index = i
                break

        # Clean and prepare data
        if target_index is not None:
            df.columns = df.iloc[target_index]
            df = df.iloc[target_index + 1:].reset_index(drop=True)

        # Remove rows containing "total"
        df = df[~df.apply(lambda row: row.astype(str).str.contains("total", case=False, na=False)).any(axis=1)]

        # Drop "Total" column if it exists
        if "Total" in df.columns:
            df = df.drop("Total", axis=1)

        st.subheader("Final Data")
        df['Date'] = report_date
        st.write(df)

        # Push to SQLite
        conn = sqlite3.connect('mis_data.db')
        if st.button("Push to SQL"):
            df.to_sql('mis_table', conn, if_exists='replace', index=False)
            conn.close()
            st.success("Data saved to SQLite database successfully!")
            

    except Exception as e:
        st.warning("Something went wrong")
        st.text(f"Error: {e}")
