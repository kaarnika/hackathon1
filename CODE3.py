import pandas as pd

# Load preprocessed combined data
df = pd.read_csv("preprocessed_combined_data.csv")

# Only keep rows with valid item/category info
valid_products = df[df['ItemCategory'].notna() & df['event_name'].isin(['view_item', 'add_to_cart', 'purchase'])]

# --- TOP PICKS by Location ---
top_by_city = valid_products.groupby(['city', 'ItemCategory']).size().reset_index(name='count')
top_by_city = top_by_city.sort_values(['city', 'count'], ascending=[True, False])

# --- TOP PICKS by Demographics ---
valid_products['gender'] = valid_products['gender'].fillna("Unknown")
valid_products['Age'] = valid_products['Age'].fillna("Unknown")
valid_products['income_group'] = valid_products['income_group'].fillna("Unknown")

valid_products['demo_key'] = valid_products['gender'] + "_" + valid_products['Age'] + "_" + valid_products['income_group']
top_by_demo = valid_products.groupby(['demo_key', 'ItemCategory']).size().reset_index(name='count')
top_by_demo = top_by_demo.sort_values(['demo_key', 'count'], ascending=[True, False])

# --- TOP PICKS by Source + Device ---
valid_products['source'] = valid_products['source'].fillna("Unknown")
valid_products['category'] = valid_products['category'].fillna("Unknown")
valid_products['source_device'] = valid_products['source'] + "_" + valid_products['category']

top_by_source_device = valid_products.groupby(['source_device', 'ItemCategory']).size().reset_index(name='count')
top_by_source_device = top_by_source_device.sort_values(['source_device', 'count'], ascending=[True, False])

# --- GLOBAL TOP PICKS ---
global_top = valid_products.groupby('ItemCategory').size().reset_index(name='count').sort_values(by='count', ascending=False)

# Save all maps
top_by_city.to_csv("top_categories_by_city.csv", index=False)
top_by_demo.to_csv("top_categories_by_demographics.csv", index=False)
top_by_source_device.to_csv("top_categories_by_source_device.csv", index=False)
global_top.to_csv("top_categories_overall.csv", index=False)

print("✅ Cold start recommendation fallback data created.")