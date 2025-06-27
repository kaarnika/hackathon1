import pandas as pd

# --- Load Data ---
activity_df = pd.read_excel("User activity dataset.xlsx")  # Your uploaded file
transaction_df = pd.read_excel("updated_items.xlsx")    # Your uploaded file

# --- Clean Data Types ---
# Convert IDs to string for safe merging
activity_df['transaction_id'] = activity_df['transaction_id'].astype(str)
transaction_df['Transaction_ID'] = transaction_df['Transaction_ID'].astype(str)

# Convert timestamps
activity_df['eventTimestamp'] = pd.to_datetime(activity_df['eventTimestamp'], errors='coerce')
activity_df['eventDate'] = pd.to_datetime(activity_df['eventDate'], errors='coerce')
transaction_df['Date'] = pd.to_datetime(transaction_df['Date'], errors='coerce')

# --- Fill Missing Values ---
# For demographic columns
for col in ['gender', 'Age', 'income_group']:
    if col in activity_df.columns:
        activity_df[col] = activity_df[col].fillna("Unknown")

# For categorical columns like city/region/country/source
for col in ['city', 'region', 'country', 'source', 'medium']:
    if col in activity_df.columns:
        activity_df[col] = activity_df[col].fillna("Unknown")

# --- Merge Activity and Transaction Data ---
merged_df = activity_df.merge(transaction_df, how='left',
                               left_on='transaction_id',
                               right_on='Transaction_ID')

# --- Construct Sessions ---
# Sort for session flow
merged_df.sort_values(by=['user_pseudo_id', 'eventTimestamp'], inplace=True)

# Create session_id using cumulative count of 'session_start' per user
merged_df['session_start_flag'] = (merged_df['event_name'] == 'session_start').astype(int)
merged_df['session_id'] = merged_df.groupby('user_pseudo_id')['session_start_flag'].cumsum()

# --- Save Cleaned Dataset ---
merged_df.to_csv("preprocessed_combined_data.csv", index=False)

# Optional: quick checks
print("Final shape:", merged_df.shape)
print("Sample columns with missing values:")
print(merged_df.isnull().sum().sort_values(ascending=False).head(10))