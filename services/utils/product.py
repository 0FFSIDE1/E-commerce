from products.models import Product
from asgiref.sync import sync_to_async
from sellers.models import Vendor
from django.core.exceptions import ObjectDoesNotExist

# Convert the product creation function into an async callable
@sync_to_async
def create_product(name, description, price, quantity, category, product_type, photo_1, photo_2, available_sizes, available_colors, request):
    try:
       
        product = Product.objects.create(
            name=name,
            description=description,
            price=float(price),
            quantity=int(quantity),
            category=category,
            product_type=product_type,
            photo_1=photo_1,
            photo_2=photo_2,
            available_sizes=available_sizes,
            available_colors=available_colors,
            vendor=request.user.vendor,
        )
        product.save()
        return product
    except ObjectDoesNotExist:
        raise ValueError("Vendor does not exist for the provided user.")

    except ValueError as ve:
        raise ValueError(f"Invalid data provided: {ve}")

    except Exception as e:
        raise RuntimeError(f"Error creating product: {e}")



async def get_product(pk):
    return await sync_to_async(Product.objects.get)(item_id=pk)

async def update_product(pk, fields):
    product = Product.objects.filter(item_id=pk).update(**fields)
    return product



