import pandas as pd

# Load the preprocessed file
df = pd.read_csv("preprocessed_combined_data.csv")

# Fill missing demographic fields
for col in ['gender', 'Age', 'income_group']:
    if col in df.columns:
        df[col] = df[col].fillna('Unknown')

# Engagement classification
def classify_engagement(events):
    if 'purchase' in events:
        return 'Purchaser'
    elif 'add_to_cart' in events:
        return 'Cart Abandoner'
    else:
        return 'Browser'

# Group by user to build segments
user_summary = df.groupby('user_pseudo_id').agg({
    'event_name': lambda x: list(x),
    'gender': lambda x: x.mode().iloc[0] if not x.mode().empty else 'Unknown',
    'Age': lambda x: x.mode().iloc[0] if not x.mode().empty else 'Unknown',
    'income_group': lambda x: x.mode().iloc[0] if not x.mode().empty else 'Unknown',
    'category': lambda x: x.mode().iloc[0] if not x.mode().empty else 'Unknown',
    'source': lambda x: x.mode().iloc[0] if not x.mode().empty else 'Unknown',
    'city': lambda x: x.mode().iloc[0] if not x.mode().empty else 'Unknown'
}).reset_index()

# Create segment labels
user_summary['engagement_type'] = user_summary['event_name'].apply(classify_engagement)
user_summary['demographic_segment'] = user_summary['gender'] + " | " + user_summary['Age'] + " | " + user_summary['income_group']
user_summary['geo_segment'] = user_summary['city']
user_summary['source_device'] = user_summary['source'] + " - " + user_summary['category']

# Drop raw event list
user_summary.drop(columns=['event_name'], inplace=True)

# Save segmentation results
user_summary.to_csv("user_segments.csv", index=False)

print("✅ User segmentation complete. Segments saved to 'user_segments.csv'")