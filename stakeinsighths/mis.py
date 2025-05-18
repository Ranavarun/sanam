# # import streamlit as st
# # import pandas as pd
# # import sqlite3 
# # import re
# # st.header("Management Information System")
# # file =st.file_uploader("upload an excel file")
# # df = pd.read_excel(file, header=None)

# #         # --- Detect Date Using Regex ---
# # date_pattern = r"\b(?:\d{1,2}[-/thstndrd\s\.])?(?:\d{1,2}[-/\s\.])?(?:\d{2,4})\b"
# # report_date = None

# # for i in range(10):
# #     row = df.iloc[i].dropna().astype(str)
# #     for val in row:
# #         match = re.search(date_pattern, val)
# #         if match:
# #             try:
# #                 parsed_date = pd.to_datetime(match.group(), errors='coerce')
# #                 if pd.notnull(parsed_date):
# #                     report_date = parsed_date.date()
# #                     break
# #             except:
# #                 continue
# #     if report_date:
# #         break

# # st.write("📅 Report Date Detected:", report_date)







# import streamlit as st
# import pandas as pd
# import sqlite3
# import re

# st.header("Management Information System")
# with st.sidebar:
#     file = st.file_uploader("Upload an Excel file", type=["xlsx"])

# if file is not None:
#     try:
#         # Step 1: Read all sheets as a dictionary
#         all_sheets = pd.read_excel(file, sheet_name=None, header=None)
#         sheet_names = list(all_sheets.keys())

#         # Step 2: Show dropdown to select sheet
#         with st.sidebar:
#             selected_sheet = st.selectbox("Select Sheet", sheet_names)

#         # Step 3: Load selected sheet
#         df = all_sheets[selected_sheet]

#         # --- Detect Date Using Regex ---
#         date_pattern = r"\b(?:\d{1,2}[-/thstndrd\s\.])?(?:\d{1,2}[-/\s\.])?(?:\d{2,4})\b"
#         report_date = None

#         for i in range(10):
#             row = df.iloc[i].dropna().astype(str)
#             for val in row:
#                 match = re.search(date_pattern, val)
#                 if match:
#                     try:
#                         parsed_date = pd.to_datetime(match.group(), errors='coerce')
#                         if pd.notnull(parsed_date):
#                             report_date = parsed_date.date()
#                             break
#                     except:
#                         continue
#             if report_date:
#                 break

#         st.write("📅 Report Date Detected:", report_date)

#         # --- Find the row with "particulars" keyword ---
#         keyword = "particulars"
#         target_index = None
#         for i, row in df.iterrows():
#             if row.astype(str).str.contains(keyword, case=False, na=False).any():
#                 target_index = i
#                 break

#         # --- Set proper header and trim data ---
#         if target_index is not None:
#             df.columns = df.iloc[target_index]
#             df = df.iloc[target_index + 1:].reset_index(drop=True)

#         # --- Clean Data ---
#         df = df[~df.apply(lambda row: row.astype(str).str.contains("total", case=False, na=False)).any(axis=1)]
#         if "Total" in df.columns:
#             df = df.drop("Total", axis=1)

#         st.subheader("Final Data")
#         st.write(df)

#         # --- Save to SQLite ---
#         conn = sqlite3.connect('mis_data.db')
#         if st.button("Push to SQL"):
#             df.to_sql('mis_table', conn, if_exists='append', index=False)
#             conn.close()
#             st.success("Data saved to SQLite database successfully!")

#     except Exception as e:
#         st.warning("Something went wrong")
#         st.text(f"Error: {e}")

import streamlit as st
import pandas as pd
import sqlite3
import re

st.header("Management Information System")

with st.sidebar:
    file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if file is not None:
    try:
        # Step 1: Read all sheets
        # not first row is not in header 
        # receving the data from all sheet 
        # returning the data in dictonary key name and value ma data
        all_sheets = pd.read_excel(file, sheet_name=None, header=None)
        sheet_names = list(all_sheets.keys()) 

        # Step 2: Let user select a sheet
        with st.sidebar:
            selected_sheet = st.selectbox("Select Sheet", sheet_names)

        # Step 3: Load the selected sheet
        df = all_sheets[selected_sheet]
        # flat_text = df.astype(str).apply(lambda x: ' '.join(x.dropna()), axis=1).str.lower()
        # if flat_text.str.contains("sundry debtor").any():
        #     st.info("🟢 'Sundry Debtor' found in data — adding 'classification' column.")
        #     df["classification"] = "debtors"
        classification_map = {
        "advance to vendor": "Advance Given",
        "sundry debtor": "Debtors",
        "sundry creditor": "Creditors",
        "retention money": "Retention"}
        
        flat_text = df.astype(str).apply(lambda x: ' '.join(x.dropna()), axis=1).str.lower()
        
        
        detected_classification = None
        for keyword, classification in classification_map.items():
            if flat_text.str.contains(keyword).any():
                detected_classification = classification
                st.info(f"🟢 '{keyword.title()}' found in data — setting classification: **{classification}**")
                break
        
        

              

        # Step 4: Extract report date from the first few rows using regex
        date_pattern = r"\b(?:\d{1,2}[-/thstndrd\s\.])?(?:\d{1,2}[-/\s\.])?(?:\d{2,4})\b"
        report_date = None

        for i in range(min(10, len(df))):
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

        if report_date:
            st.write("📅 Report Date Detected:", report_date)

        # Step 5: Find the header row using keywords
        keywords = ["particulars", "party name"]
        target_index = None
        matched_keyword = None

        for i, row in df.iterrows():
            row_str = row.astype(str).str.lower()
            for kw in keywords:
                if row_str.str.contains(kw, na=False).any():
                    target_index = i
                    matched_keyword = kw
                    break
            if target_index is not None:
                break

        if target_index is not None:
            st.write(f"✅ Found header using keyword: `{matched_keyword}` at row {target_index}")
            df.columns = df.iloc[target_index]
            df = df.iloc[target_index + 1:].reset_index(drop=True)
        else:
            st.warning("No header row found with keywords: 'particulars' or 'party name'")
        df = df.dropna(axis=1, how='all') 
        # Step 6: Remove rows that contain 'total' in any column
        df = df[~df.apply(lambda row: row.astype(str).str.contains("total", case=False, na=False)).any(axis=1)]

        if "Total" in df.columns:
            df = df.drop("Total", axis=1)

        st.subheader("Final Data")
        df['Date'] = report_date
        df['Classification'] = detected_classification
        st.write(df)

        # Step 7: Push to SQLite if user clicks the button
        conn = sqlite3.connect('mis_data.db')
        if st.button("Push to SQL"):
            df.to_sql('mis_table', conn, if_exists='append', index=False)
            conn.close()
            st.success("Data saved to SQLite database successfully!")

    except Exception as e:
        st.warning("Something went wrong")
        st.text(f"Error: {e}")
