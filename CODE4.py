import pandas as pd
from datetime import datetime

# --- Load all necessary data files ---
top_by_city = pd.read_csv("top_categories_by_city.csv")
top_by_demo = pd.read_csv("top_categories_by_demographics.csv")
top_by_source_device = pd.read_csv("top_categories_by_source_device.csv")
global_top = pd.read_csv("top_categories_overall.csv")
user_segments = pd.read_csv("user_segments.csv")

# --- Functions ---
def cold_start_recommendation(city, gender, age, income, source, device):
    demo_key = f"{gender}_{age}_{income}"
    match = top_by_demo[top_by_demo['demo_key'] == demo_key]
    if not match.empty:
        return match['ItemCategory'].head(3).tolist()

    sd_key = f"{source}_{device}"
    match = top_by_source_device[top_by_source_device['source_device'] == sd_key]
    if not match.empty:
        return match['ItemCategory'].head(3).tolist()

    match = top_by_city[top_by_city['city'].str.lower() == city.lower()]
    if not match.empty:
        return match['ItemCategory'].head(3).tolist()

    return []  # leave it to trending fallback

def generate_landing_page(user_segment=None, cold_start_info=None, trending_fallback=None):
    if user_segment:
        demo_key = user_segment['demographic_segment'].replace(" ", "")
        match = top_by_demo[top_by_demo['demo_key'] == demo_key]
        categories = match['ItemCategory'].head(3).tolist() if not match.empty else global_top['ItemCategory'].head(3).tolist()
        engagement = user_segment['engagement_type']
    elif cold_start_info:
        categories = cold_start_recommendation(
            city=cold_start_info['city'],
            gender=cold_start_info['gender'],
            age=cold_start_info['age'],
            income=cold_start_info['income'],
            source=cold_start_info['source'],
            device=cold_start_info['device']
        )
        engagement = "New Visitor"
        if not categories and trending_fallback:
            categories = trending_fallback
    else:
        categories = trending_fallback or global_top['ItemCategory'].head(3).tolist()
        engagement = "New Visitor"

    return {
        "hero_banner": f"🌟 Explore Top Picks in {categories[0] if categories else 'our collection'}",
        "product_carousels": [f"🛍️ Recommended in {cat}" for cat in categories],
        "cta_module": {
            "Browser": "🔍 Explore More Products",
            "Cart Abandoner": "🛒 Complete Your Purchase",
            "Purchaser": "🎁 Buy Again or Refer a Friend",
            "New Visitor": "✨ Discover What’s Popular"
        }.get(engagement, "Check Out Our Offers")
    }

def match_guest_to_segment(city, gender, age, income, source, device):
    demo_segment = f"{gender} | {age} | {income}"
    source_device = f"{source} - {device}"

    match = user_segments[
        (user_segments['demographic_segment'] == demo_segment) &
        (user_segments['geo_segment'].str.lower() == city.lower()) &
        (user_segments['source_device'] == source_device)
    ]

    return match.iloc[0].to_dict() if not match.empty else None

def get_trending_today(preprocessed_file):
    df = pd.read_csv(preprocessed_file)
    df['eventDate'] = pd.to_datetime(df['eventDate'], errors='coerce')
    today = pd.Timestamp(datetime.today().date())

    valid_events = df[
        df['event_name'].isin(['view_item', 'add_to_cart', 'purchase']) &
        df['eventDate'].notna() &
        (df['eventDate'].dt.date == today.date()) &
        df['ItemCategory'].notna()
    ]

    top = (
        valid_events.groupby('ItemCategory')
        .size()
        .reset_index(name='count')
        .sort_values(by='count', ascending=False)
        .head(3)
    )
    return top['ItemCategory'].tolist()

# --- CLI Interface ---
def main():
    print("🧠 Hyper-Personalized Landing Page Generator")
    print("Select User Type:")
    print("1. Existing User")
    print("2. New User / Guest")
    choice = input("Enter 1 or 2: ")

    trending_today = get_trending_today("preprocessed_combined_data.csv")

    if choice == "1":
        user_id = input("Enter User ID (user_pseudo_id): ")
        try:
            user_id = float(user_id)
        except ValueError:
            print("Invalid User ID")
            return

        match = user_segments[user_segments['user_pseudo_id'] == user_id]
        if not match.empty:
            print("✅ Known user matched.")
            segment = match.iloc[0].to_dict()
            page = generate_landing_page(user_segment=segment)
        else:
            print("🧊 User ID not found. Falling back to trending.")
            page = generate_landing_page(trending_fallback=trending_today)

    elif choice == "2":
        print("📌 Enter Guest Info")
        city = input("City (e.g. Mumbai): ")
        gender = input("Gender (male/female): ")
        age = input("Age Group (e.g. 18-24, 25-34): ")
        income = input("Income Group (e.g. below 50%, 11-20%, Top 10%): ")
        source = input("Traffic Source (e.g. Facebook, Instagram, (direct), Email): ")
        device = input("Device (mobile/desktop): ")

        guest_info = {
            "city": city,
            "gender": gender,
            "age": age,
            "income": income,
            "source": source,
            "device": device
        }

        matched_segment = match_guest_to_segment(city, gender, age, income, source, device)

        if matched_segment:
            print("🔍 Guest matched to a known segment.")
            page = generate_landing_page(user_segment=matched_segment)
        else:
            print("⚠️ No segment match found. Checking cold start fallback...")
            page = generate_landing_page(cold_start_info=guest_info, trending_fallback=trending_today)
    else:
        print("Invalid choice.")
        return

    # --- Output ---
    print("\n🖼️ Hero Banner:")
    print(page["hero_banner"])

    print("\n🛒 Product Carousels:")
    for item in page["product_carousels"]:
        print(item)

    print("\n🚀 Call-To-Action:")
    print(page["cta_module"])

if __name__ == "__main__":
    main()
