# from  products.models import Product


# products = [
#     # Electronics
#     {
#         "name": "Wireless Bluetooth Earbuds",
#         "description": "High-quality wireless earbuds with long battery life.",
#         "price": 59.99,
#         "previous_price": 79.99,
#         "product_type": "Electronics",
#         "brand": "TechSound",
#         "quantity": 100,
#         "section": "Electronics",
#         "category": "Audio Devices",
#     },
#     {
#         "name": "Smartwatch with Fitness Tracker",
#         "description": "Track your fitness and health with this versatile smartwatch.",
#         "price": 129.99,
#         "previous_price": 149.99,
#         "product_type": "Electronics",
#         "brand": "HealthTime",
#         "quantity": 50,
#         "section": "Wearables",
#         "category": "Fitness & Health",
#     },
#     {
#         "name": "USB-C Multiport Adapter",
#         "description": "Expand your laptop's connectivity with this multiport adapter.",
#         "price": 24.99,
#         "previous_price": 29.99,
#         "product_type": "Accessories",
#         "brand": "TechConnect",
#         "quantity": 200,
#         "section": "Electronics",
#         "category": "Computer Accessories",
#     },
#     {
#         "name": "Portable Solar Power Bank",
#         "description": "Charge your devices on the go with solar power.",
#         "price": 39.99,
#         "previous_price": 49.99,
#         "product_type": "Electronics",
#         "brand": "EcoCharge",
#         "quantity": 80,
#         "section": "Outdoor",
#         "category": "Power Banks",
#     },
#     {
#         "name": "RGB Gaming Keyboard",
#         "description": "Enhance your gaming experience with this colorful keyboard.",
#         "price": 74.99,
#         "previous_price": 89.99,
#         "product_type": "Electronics",
#         "brand": "GamePro",
#         "quantity": 150,
#         "section": "Gaming",
#         "category": "Gaming Accessories",
#     },
#     # Additional products (Add similar entries up to 200)
#     {
#         "name": "Noise-Canceling Headphones",
#         "description": "Immerse yourself in music with these noise-canceling headphones.",
#         "price": 199.99,
#         "previous_price": 249.99,
#         "product_type": "Electronics",
#         "brand": "QuietSound",
#         "quantity": 75,
#         "section": "Electronics",
#         "category": "Audio Devices",
#     },
#     {
#         "name": "4K Action Camera",
#         "description": "Capture your adventures in stunning 4K resolution.",
#         "price": 299.99,
#         "previous_price": 349.99,
#         "product_type": "Electronics",
#         "brand": "AdventureCam",
#         "quantity": 40,
#         "section": "Outdoor",
#         "category": "Cameras",
#     },
#     {
#         "name": "LED Ring Light for Content Creators",
#         "description": "Brighten your content creation setup with this LED ring light.",
#         "price": 59.99,
#         "previous_price": 79.99,
#         "product_type": "Electronics",
#         "brand": "BrightStudio",
#         "quantity": 120,
#         "section": "Electronics",
#         "category": "Lighting",
#     },
#     {
#         "name": "Mini Projector for Home Theater",
#         "description": "Transform your living room into a cinema with this mini projector.",
#         "price": 199.99,
#         "previous_price": 249.99,
#         "product_type": "Electronics",
#         "brand": "CinemaPro",
#         "quantity": 60,
#         "section": "Home Entertainment",
#         "category": "Projectors",
#     },
#     {
#         "name": "Smart Home Wi-Fi Plug",
#         "description": "Control your appliances remotely with this smart plug.",
#         "price": 19.99,
#         "previous_price": 24.99,
#         "product_type": "Electronics",
#         "brand": "SmartEase",
#         "quantity": 300,
#         "section": "Smart Home",
#         "category": "Home Automation",
#     },
#     # ... Repeat similar structures for other categories and products
# ]
# # You can generate more products programmatically if needed.
# # For example:
# import random
# def generate_random_products():
#     brands = ["BrandA", "BrandB", "BrandC", "BrandD"]
#     categories = ["Electronics", "Fashion", "Home Appliances", "Outdoor", "Gaming"]
#     product_types = ["Accessories", "Wearables", "Devices"]
#     sections = ["Electronics", "Fashion", "Home"]
#     products = []
#     for i in range(6, 1001):
#         Product.objects.create(
#             name=f"Product {i}",
#             description=f"Description for Product {i}",
#             price=round(random.uniform(10.0, 500.0), 2),
#             previous_price=round(random.uniform(20.0, 600.0), 2),
#             product_type=random.choice(product_types),
#             brand=random.choice(brands),
#             quantity=random.randint(10, 200),
#             section=random.choice(sections),
#             category=random.choice(categories),          
#         )
#     print('Successfully added')
#     return products
# # Add random products to the lisT