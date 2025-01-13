from products.models import Product
from asgiref.sync import sync_to_async
from sellers.models import Vendor

# Convert the product creation function into an async callable
@sync_to_async
def create_product(name, description, price, quantity, category, product_type, photo_1, photo_2, available_sizes, available_colors, vendor):
    # vendor = Vendor.objects.get(user=vendor)
    product = Product.objects.create(
        name=name,
        description=description,
        price=price,
        quantity=quantity,
        category=category,
        product_type=product_type,
        photo_1=photo_1,
        photo_2=photo_2,
        available_sizes=available_sizes,
        available_colors=available_colors,
        # vendor=vendor,
    )
    product.save()
    return product



async def get_product(pk):
    return await sync_to_async(Product.objects.get)(item_id=pk)

async def update_product(pk, fields):
    product = Product.objects.filter(item_id=pk).update(**fields)
    return product



