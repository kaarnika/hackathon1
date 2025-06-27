import pandas as pd

# Step 1: Load your Excel file
df = pd.read_excel("dataset2_final.xlsx")  # Replace with your actual file name

# Step 2: Define real items, brands, categories
categories = ['Electronics', 'Fashion', 'Home & Kitchen', 'Beauty & Personal Care', 'Sports & Outdoors']
brands = ['Nexon', 'UrbanCart']
items = [
    "Bluetooth Speaker", "Wireless Earbuds", "Power Bank", "Smartwatch", "LED Monitor", "Gaming Mouse",
    "Mechanical Keyboard", "Wi-Fi Router", "USB-C Charger", "External SSD", "Laptop Stand", "Webcam 1080p",
    "Smart TV Remote", "HDMI Cable", "Screen Cleaner Kit", "Portable Projector", "Smart Plug", "Phone Tripod",
    "MicroSD Card", "Bluetooth Tracker", "Wireless Charger Pad", "Laptop Backpack", "Earphone Case", "Action Camera",
    "Noise Cancelling Headphones", "Webcam Cover Slide", "VR Headset", "LED Strip Lights", "Mini Drone",
    "Solar Power Bank", "Bluetooth Receiver", "USB Fan", "Car Phone Mount", "USB Hub", "Laptop Cooling Pad",
    "Dash Cam", "TV Wall Mount", "Gaming Controller", "Smart Doorbell", "E-book Reader", "Streaming Stick",
    "USB Desk Lamp", "Wireless Presenter", "HDMI Splitter", "RFID Wallet", "LCD Writing Pad", "Rechargeable Batteries",
    "USB Mic", "Electric Screwdriver", "Cable Organizer", "Cotton T-Shirt", "Slim Fit Jeans", "Sports Shoes",
    "Denim Jacket", "Sunglasses", "Leather Wallet", "Wrist Watch", "Beanie Cap", "Travel Duffel Bag", "Ankle Socks",
    "Formal Shirt", "Tie & Cufflinks Set", "Hoodie", "Backpack", "Cargo Pants", "Flip Flops", "Rain Jacket",
    "Joggers", "Tank Top", "Fedora Hat", "Aviator Sunglasses", "Printed Scarf", "Designer Belt", "Graphic Tee",
    "Trench Coat", "Leather Boots", "Polo Shirt", "Knit Sweater", "Swim Trunks", "Gym Shorts", "Maxi Dress",
    "Chinos", "Loafers", "Leggings", "Denim Skirt", "Bomber Jacket", "Tracksuit", "Gloves", "Silk Tie", "Blazer",
    "Woven Hat", "Sports Bra", "Yoga Pants", "Flats", "Crop Top", "Wide-Leg Trousers", "Ripped Jeans",
    "Faux Fur Coat", "Lace Top", "Halter Neck Dress", "Electric Kettle", "Coffee Mug Set", "Blender", "Gas Stove",
    "Frying Pan", "Air Fryer", "Vacuum Cleaner", "Dish Rack", "Water Purifier", "Wall Clock", "Table Lamp",
    "Storage Bins", "Dish Towels", "Microwave Oven", "Chopping Board", "Spice Rack", "Laundry Basket",
    "Non-stick Cookware", "Bed Sheets", "Room Heater", "Electric Rice Cooker", "Cutlery Set", "Floor Mop",
    "Pressure Cooker", "Curtain Set", "Bathroom Mirror", "Shoe Rack", "Room Diffuser", "Thermos Flask",
    "Electric Toaster", "Hand Blender", "Wall Art Frame", "Tissue Box Holder", "Cloth Hangers", "Sandwich Maker",
    "Digital Weighing Scale", "Kitchen Apron", "Oven Mitts", "Mixing Bowls", "Napkin Holder", "Steam Iron",
    "Garbage Bin", "Doormat", "Teapot", "Induction Cooktop", "Storage Jars", "Table Fan", "Egg Boiler",
    "Wall Hooks", "Reading Lamp", "Face Wash", "Shampoo", "Lip Balm", "Body Lotion", "Hair Dryer", "Eyeliner Pen",
    "Compact Powder", "Beard Trimmer", "Electric Toothbrush", "Nail Polish", "Perfume Spray", "Lipstick Set",
    "Face Serum", "Razor Blades", "Facial Cleanser", "Sheet Mask", "Hair Straightener", "Sunscreen Lotion",
    "Deodorant Stick", "Shower Gel", "Facial Steamer", "Hair Brush", "Cotton Pads", "Moisturizer", "Eye Cream",
    "Nail File", "Makeup Remover", "Shaving Cream", "Massage Oil", "Eyebrow Kit", "Hand Cream", "Teeth Whitening Kit",
    "Hair Color", "Cuticle Scissors", "Face Roller", "Makeup Pouch", "Nose Strips", "Lip Scrub", "Tanning Lotion",
    "Anti-aging Cream", "Makeup Brush Set", "Hair Serum", "Foot Scrub", "Blackhead Remover Tool", "Hair Cap",
    "Scalp Massager", "Lip Tint", "Travel Toiletry Bag", "Facial Cleanser Brush", "Beard Oil", "Yoga Mat",
    "Dumbbell Set", "Water Bottle", "Camping Tent", "Hiking Shoes", "Resistance Bands", "Bicycle Helmet",
    "Sports Watch", "Badminton Racket", "Cricket Bat", "Tennis Ball Pack", "Jump Rope", "Travel Backpack",
    "Gym Gloves", "Sports Towel", "Sleeping Bag", "Treadmill Lubricant", "Bicycle Lock", "Flashlight Torch",
    "Hiking Stick", "Insect Repellent Spray", "Sweatband", "Bike Pump", "Compass", "First Aid Kit", "Bike Bell",
    "Energy Bar Pack", "Fishing Rod", "Sports Cap", "Climbing Rope", "Binoculars", "Yoga Block", "Skipping Rope",
    "Foldable Chair", "Football", "Basketball", "Cricket Gloves", "Swimming Goggles", "Sports Armband",
    "Camping Lantern", "Exercise Ball", "Gym Bag", "Knee Support", "Bike Saddle Cover", "Table Tennis Bat",
    "Rain Poncho", "Resistance Tube"
]

# Step 3: Replace placeholders
# Replace item1, item2, etc. with items list (assumes items are labeled as "item1", "item2", ..., up to "item247")
for i in range(1, 248):
    df['ItemName'] = df['ItemName'].replace(f'ITEM{i}', items[i - 1])

# Replace brand1, brand2
df['ItemBrand'] = df['ItemBrand'].replace({
    'ITEM_BRAND1': brands[0],
    'ITEM_BRAND2': brands[1]
})

# Replace category1 to category5
for i in range(1, 6):
    df['ItemCategory'] = df['ItemCategory'].replace(f'CATEGORY_{i}', categories[i - 1])

# Step 4: Save the updated file
df.to_excel("updated_items.xlsx", index=False)
print("✅ Items replaced and saved to 'updated_items.xlsx'")