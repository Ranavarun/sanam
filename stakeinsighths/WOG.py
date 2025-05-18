import streamlit as st
import pandas as pd
import sqlite3
import re

st.header("Management Information System")

with st.sidebar:
    file = st.file_uploader("Upload an Excel file", type=["xlsx","xlx"])

flag = -1

if file is not None:
    try:
       
        all_sheets = pd.read_excel(file, sheet_name=None, header=None)
        sheet_names = list(all_sheets.keys()) 

        
        with st.sidebar:
            selected_sheet = st.selectbox("Select Sheet", sheet_names)

        
        df = all_sheets[selected_sheet]
        classification_map = {
        "advance to vendor": "Advance Given",
        "sundry debtors": "Debtors",
        "sundry creditors": "Creditors",
        "retention money": "Retention",
        "secured loan":"Secured",
        "unsecured loan":"Unsecured",
        "od limit":"OD",
        "project wise billing":"sales"}
        flat_text = df.astype(str).apply(lambda x: ' '.join(x.dropna()), axis=1).str.lower()
        
        detected_classification = None
        for keyword, classification in classification_map.items():
            pattern = rf"\b{re.escape(keyword)}\b"
            if flat_text.str.contains(pattern, regex=True).any():
                detected_classification = classification
                st.info(f"🟢 '{keyword.title()}' found in data — setting classification: **{classification}**")
                break
                
        

              

        # Step 4: Extract report date from the first few rows using regex
        date_pattern = r"\b(?:\d{1,2}[-/thstndrd\s\.])?(?:\d{1,2}[-/\s\.])?(?:\d{2,4})\b"
        report_date = None
        # date format
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
            keywords = ["particulars", "party name", "lender's name", "item head"]
            target_index = None
            matched_keyword = None

            for index, row1 in df.iterrows():
                # Convert the row to lowercase, replace slashes and hyphens with space, and remove extra spaces
                row_values_str = ' '.join(
                    ''.join(map(str, row1.values))
                    .lower()
                    .replace('/', ' ')
                    .replace('-', ' ')
                    .split()
                )

                # Check if any keyword is in the normalized row string
                for kw in keywords:
                    if kw in row_values_str:
                        target_index = index
                        matched_keyword = kw
                        break

                # Break after finding the first match
                if target_index is not None:
                    break

            # Optional: Print result
            print(f"First match found at row {target_index} for keyword: '{matched_keyword}'")

        if target_index is not None:
            st.write(f"✅ Found header using keyword: `{matched_keyword}` at row {target_index}")
            df.columns = df.iloc[target_index]
            df = df.iloc[target_index + 1:].reset_index(drop=True)
        else:
            st.warning("No header row found with keywords: 'particulars', 'party name', or 'lender's name'")
        df = df.loc[:, df.columns.notna()]
        print(df)
        df = df.dropna(axis=1, how='all') 
        st.write(df.shape)
        # Step 6: Remove rows that contain 'total' in any column
        df = df[~df.apply(lambda row: row.astype(str).str.contains("total", case=False, na=False)).any(axis=1)]

        if "Total" in df.columns:
            df = df.drop("Total", axis=1)
            
            
        if "INstallment No" in df.columns:
          df = df.rename(columns={"INstallment No":"Installment No"})
          
        if "Rate of Interest" in df.columns:
          df = df.rename(columns={"Rate of Interest":"Interest"})
          df.insert(0, 'S. No.', range(1, len(df) + 1))

        
       
        if "Project / Item head" in df.columns:
          df = df.iloc[:,[0,1,-1]]
          df = df.rename(columns={df.columns[-1]: "Value"})
        st.subheader("Final Data")
        df['Date'] = report_date
        df['Classification'] = detected_classification
        
        # if detected_classification == 'Unsecured':
        #   df = df.drop("EMI DUE DATE", axis=1)
        df = df[df.isnull().sum(axis=1) <= 4]

        if detected_classification in ["Advance Given","Debtors","Creditors","Retention"]:
          if "Particulars" in df.columns:
            df = df.rename(columns={"Particulars":"Party Name"})
          df = df[df["Party Name"].notnull()]
          flag = 1
          df.columns = df.columns.str.replace("(", "", regex=False).str.replace(")", "", regex=False)

        elif detected_classification in ["Secured","Unsecured","OD"]:
          flag = 2
        elif detected_classification in ["sales"]:
          flag = 3
          df = df[df["Project / Item head"].notnull()]


        st.write(df)

        # Step 7: Push to SQLite if user clicks the button
        conn = sqlite3.connect('dummy_wog.db')
        cursor = conn.cursor()

        if st.button("Push to SQL"):
          # st.write(df.columns)
          if flag == 1:
            for _, row in df.iterrows():
              cursor.execute("""
                  INSERT INTO CurrentAsset_CurrentLiabilities (
                      "Serial Number", 
                      "Particulars", 
                      "Less Than 120 Days", 
                      "More Than 120 Days", 
                      "Date", 
                      "Classification"
                  ) VALUES (?, ?, ?, ?, ?, ?)
              """, (
                  row[0],  # S. No.
                  row[1],  # Particulars
                  row[2],  # Less Than 120 Days
                  row[3],  # More Than 120 Days
                  row[4],  # Date
                  row[5]   # Classification
              ))
          



          if 2 == flag:
            # Loop through DataFrame rows and insert mapped values
            if detected_classification == "Unsecured":
              for _, row in df.iterrows():
                  cursor.execute("""
                      INSERT INTO Loans (
                          "Serial Number","LENDER'S NAME ", "Loan Amount", "Interest", "Period", "Emi Amount" ,"Emi Due Date","Installment No","Principle Remaining","Principle Outstanding","Date","Classification"
                      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                  """, (
                      row['S. No.'],
                      row["LENDER'S NAME "],
                      row['Loan amount'],
                      row['Interest'],
                      row['Period (months)'],
                      row['EMI AMOUNT'],
                      row['EMI DUE DATE'],
                      row['Installment No'],
                      row['Principle Remaining'],
                      row['Principle Outstanding'],
                      row['Date'],
                      row['Classification']
                  ))
            if detected_classification == "OD":
              for _, row in df.iterrows():
                  cursor.execute("""
                      INSERT INTO Loans (
                          "Serial Number", "Interest", "LENDER'S NAME ","Utilisation Amount","Balance Unused","Classification"
                      ) VALUES (?, ?, ?, ?, ?, ?)
                  """, (
                      row['S. No.'],
                      row['Interest'],
                      row["LENDER'S NAME "],
                      row['Utilisation Amount'],
                      row['Balance Unused'],
                      row['Classification']
                  ))
            if detected_classification == "Secured":
              for _, row in df.iterrows():
                  cursor.execute("""
                      INSERT INTO Loans (
                          "Serial Number","LENDER'S NAME ", "Loan Amount", "Interest", "Period", "Emi Amount" ,"Installment No","Principle Remaining","Principle Outstanding","Date","Classification"
                      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                  """, (
                      row['S. No.'],
                      row["LENDER'S NAME "],
                      row['Loan amount'],
                      row['Interest'],
                      row['Period (months)'],
                      row['EMI AMOUNT'],
                      row['Installment No'],
                      row['Principle Remaining'],
                      row['Principle Outstanding'],
                      row['Date'],
                      row['Classification']
                  ))
                  
          if 3 == flag:
            for _, row in df.iterrows():
                  cursor.execute("""
                      INSERT INTO Sales (
                          "Serial Number", 
                          "Item Head", 
                          "Value", 
                          "Date", 
                          "Classification"
                      ) VALUES (
                          ?,?,?,?,?
                      ) """, (
                      row['S.No'],
                      row['Project / Item head'],
                      row['Value'],
                      row['Date'],
                      row['Classification']
                      
                  ))
          conn.commit()
          conn.close()
          st.success("Data saved to SQLite database successfully!")

    except Exception as e:
        st.warning("Something went wrong")
        st.text(f"Error: {e}")
