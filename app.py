from flask import Flask, render_template, request
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# --- Load data ---
top_by_city = pd.read_csv("top_categories_by_city.csv")
top_by_demo = pd.read_csv("top_categories_by_demographics.csv")
top_by_source_device = pd.read_csv("top_categories_by_source_device.csv")
global_top = pd.read_csv("top_categories_overall.csv")
user_segments = pd.read_csv("user_segments.csv")

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

    return []

def match_guest_to_segment(city, gender, age, income, source, device):
    demo_segment = f"{gender} | {age} | {income}"
    source_device = f"{source} - {device}"

    match = user_segments[
        (user_segments['demographic_segment'] == demo_segment) &
        (user_segments['geo_segment'].str.lower() == city.lower()) &
        (user_segments['source_device'] == source_device)
    ]
    return match.iloc[0].to_dict() if not match.empty else None

def get_trending_today():
    df = pd.read_csv("data/preprocessed_combined_data.csv")
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

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        city = request.form["city"]
        gender = request.form["gender"]
        age = request.form["age"]
        income = request.form["income"]
        source = request.form["source"]
        device = request.form["device"]

        trending = get_trending_today()
        matched_segment = match_guest_to_segment(city, gender, age, income, source, device)

        guest_info = {
            "city": city,
            "gender": gender,
            "age": age,
            "income": income,
            "source": source,
            "device": device
        }

        if matched_segment:
            page = generate_landing_page(user_segment=matched_segment)
        else:
            page = generate_landing_page(cold_start_info=guest_info, trending_fallback=trending)

        return render_template("result.html", page=page)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
