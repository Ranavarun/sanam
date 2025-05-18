import pandas as pd

# Sample data
data = {
    'combined': ['/100/abc/200', '/101/def/300', '/102/ghi/400']
}

df = pd.DataFrame(data)
print(df)


# Split on '/' and remove the first empty element
split_cols = df['combined'].str.split('/', expand=True).iloc[:, 1:]
split_cols.columns = ['col_A', 'col_B', 'col_C']  # Rename immediately

df = pd.concat([df, split_cols], axis=1)
df = df.drop(columns=['combined'])  # Remove original column
print(df)


# Enforce types
df['col_A'] = pd.to_numeric(df['col_A'], errors='coerce').astype('Int64')  # Nullable Int
df['col_B'] = df['col_B'].astype(str)
df['col_C'] = pd.to_numeric(df['col_C'], errors='coerce')  # Mixed: numeric or NaN
print(df.dtypes)


df = pd.DataFrame({
    'name': ['Varun', 'Varun Rana', 'Varun Rana Thakur', 'Amit Kumar Sharma', 'Pooja']
})



df[['first', 'middle', 'last']] = df['name'].str.split(' ', n=2, expand=True)