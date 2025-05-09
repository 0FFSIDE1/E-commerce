from products.models import Color, Product, ProductImage, ProductVariation, Size
from asgiref.sync import sync_to_async
from django.db import transaction
from django.db.models import Q

# Convert the product creation function into an async callable
@sync_to_async
def create_product(name, section, description, price, quantity, category, product_type, photo_1, photo_2, available_sizes, available_colors):
    product = Product.objects.create(
        name=name.upper(),
        description=description,
        price=price,
        quantity=quantity,
        category=category,
        section=section,
        product_type=product_type,
        photo_1=photo_1,
        photo_2=photo_2,
        available_sizes=available_sizes,
        available_colors=available_colors,
    )
    product.save()
    return product

@sync_to_async
def create_product_variation(product, size, color, quantity, image):
    with transaction.atomic():  # Ensures atomicity to prevent partial saves
        size_product, _ = Size.objects.get_or_create(name=size)
        color_product, _ = Color.objects.get_or_create(name=color)

        product_variation, created= ProductVariation.objects.get_or_create(
            product=product,
            size=size_product,
            color=color_product,
            quantity=quantity,  
        )
        if not created:
            return None
        # Use `exists()` efficiently
        if not ProductImage.objects.filter(color=color_product, product=product).exists():
            ProductImage.objects.create(
                color=color_product,
                product=product,
                image=image,
            )
    return product_variation

async def get_product(pk):
    return await sync_to_async(Product.objects.get)(item_id=pk)

async def update_product(pk, fields):
    product = Product.objects.filter(item_id=pk).update(**fields)
    return product

@sync_to_async
def get_all_products(category=None, product_type=None, min_price=None, max_price=None, name=None, section=None):
    products = Product.objects.prefetch_related(
        "variations__size", "variations__color", "color_images__color"
    ).all()

    # 🧠 Dynamic filtering
    filters = Q()
    if category:
        filters &= Q(category__iexact=category)

    if product_type:
        filters &= Q(product_type__iexact=product_type)
    
    if section:
        filters &= Q(section__icontains=section)

    if min_price:
        filters &= Q(price__gte=min_price)

    if max_price:
        filters &= Q(price__lte=max_price)

    if name:
        filters &= Q(name__icontains=name)

    products = products.filter(filters)
    product_list = []

    for product in products:
        # Map color name to its image URL for quick lookup
        color_image_map = {
            image.color.name: image.image
            for image in product.color_images.all()
        }
        # Group colors by size
        size_map = {}
        for variation in product.variations.all():
            size = variation.size.name
            color_name = variation.color.name
            color_data = {
                "name": color_name,
                "instock": variation.instock,
                "image_url": color_image_map.get(color_name)  # May be None
            }
            if size not in size_map:
                size_map[size] = {
                    "size": size,
                    "colors": [color_data]
            }
            else:
                if not any(c["name"] ==  color_name for c in size_map[size]["colors"]):
                    size_map[size]["colors"].append(color_data)

        available_options = list(size_map.values())

        # # Optional: Still include all available product-level color images
        # all_colors = [
        #     {
        #         "color": color_name,
        #         "image_url": image_url
        #     }
        #     for color_name, image_url in color_image_map.items()
        # ]
        cover_image = product.photo_1 or next(iter(color_image_map.values()), None)
        product_list.append({
            "id": product.item_id,
            "name": product.name,
            "price": product.price,
            "description": product.description,
            "section": product.section,
            "category": product.category,
            'instock': product.in_stock,
            "product_type": product.product_type,
            "cover_image": cover_image,
            "photo_1": product.photo_1,
            "photo_2": product.photo_2,
            "available_options": available_options,     
        })
    return product_list
