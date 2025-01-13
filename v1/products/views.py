from django.http import JsonResponse
from django.shortcuts import redirect
from services.utils.cloudinary import upload_image, get_image_urls
from django.views import View
import asyncio
from products.models import Product
from django.contrib import messages
import logging
from services.utils.product import create_product, get_product
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import sync_to_async
from django.contrib.auth.decorators import login_required, user_passes_test
from services.utils.user import staff_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
# Set up logging
logger = logging.getLogger(__name__)



@login_required
@user_passes_test(staff_required,  login_url='login', redirect_field_name='login')
async def AddProductView(request):
    if request.method == "POST": 
        try:
            photo1 = request.FILES.get('photo1')
            photo2 = request.FILES.get('photo2')
            category = request.POST.get('category')
            product_type = request.POST.get('product_type')
            name = request.POST['name']
            description = request.POST['description']
            price = request.POST['price']
            quantity = request.POST['quantity']
            sizes = request.POST.getlist('available_sizes')
            colors = request.POST.getlist('available_colors')
            
            # Run the image uploads concurrently
            result = await asyncio.gather(
                upload_image(
                    photo1, 
                    f"Products/{category}/{product_type}"),

                upload_image(
                    photo2,
                    f"Products/{category}/{product_type}"),
            )

            # Extract the image URLs from the responses
            photo_1_url = result[0]['secure_url']
            photo_2_url = result[1]['secure_url']
            
            # Use the URLs to create the product
            await create_product(
                name=name, 
                description=description,
                quantity=quantity, 
                price=price, 
                photo_1=photo_1_url, 
                photo_2=photo_2_url, 
                category=category, 
                product_type=product_type,
                available_sizes=sizes,
                available_colors=colors,
                )

            # Log successful product creation
            logger.info(f"Product '{name}' created successfully.")
            messages.success(request, 'Product added to inventory successfully!')
            context = {
                'success': True,
                'message': 'Product added successfully'
            }
            return JsonResponse(context, safe=True)

        except Exception as e:
            # Log the exception for debugging purposes
            logger.error(f"Error adding product: {str(e)}")
            context = {
                'success': False,
                'message': f'Failed to add product {e}'
            }
            return JsonResponse(context, safe=True)



@login_required
@user_passes_test(staff_required,  login_url='login', redirect_field_name='login')
async def UpdateProductView(request, pk):
    if request.method == 'POST':
        try:
            # Retrieve the product asynchronously
            product = await get_product(pk=pk)
            photo_1 = request.FILES.get('photo_1')
            photo_2 = request.FILES.get('photo_2')

            # Prepare the upload tasks
            upload_tasks = []

            if photo_1:
                upload_tasks.append(upload_image(
                    photo_1,
                    f"Products/{request.POST.get('category')}/{request.POST.get('product_type')}"
                ))

            if photo_2:
                upload_tasks.append(upload_image(
                    photo_2,
                    f"Products/{request.POST.get('category')}/{request.POST.get('product_type')}"
                ))

            # Await the uploads concurrently
            result = await asyncio.gather(*upload_tasks)

            # Safely extract the image URLs from the responses
            photo_1_url, photo_2_url =  await get_image_urls(result, photo_1, photo_2)

            # Prepare the fields to update in the product
            fields_to_update = {
                'name': request.POST['name'],
                'price': request.POST['price'],
                'quantity': request.POST['quantity'],
                'description': request.POST['description'],
                'category': request.POST.get('category'),
                'product_type': request.POST.get('product_type'),
            }

            if photo_2_url:
                fields_to_update['photo_2'] = photo_2_url
            if photo_1_url:
                fields_to_update['photo_1'] = photo_1_url

            sizes = request.POST.getlist('available_sizes')
            colors = request.POST.getlist('available_colors')
          
            
            if len(sizes) > 0:
                fields_to_update['available_sizes'] = sizes
            if len(colors) > 0:
                fields_to_update['available_colors'] = colors

            

            # Update the product instance
            for field, value in fields_to_update.items():
                setattr(product, field, value)
            # Save asynchronously
            await sync_to_async(product.save)()
  
            context = {
                'success': True,
                'message': 'Product Updated Successfully'
            }
            return JsonResponse(context, safe=True)
           
        except Exception as e:
            context = {
                'success': False,
                'message': f'Failed to update product {e}'
            }
            return JsonResponse(context, safe=True)
    

@login_required
@user_passes_test(staff_required,  login_url='login', redirect_field_name='login')
@csrf_exempt
def DeleteProductView(request, pk):
    if request.method == 'POST':
        try:
            product = Product.objects.get(item_id=pk)
            product.delete()
            messages.success(request, 'Product deleted successfully!')
            return JsonResponse({'success': True}, safe=True)
        except Exception as e:
            messages.error(request, f'Product deletion Failed! {str(e)}')
            return JsonResponse({'success': False}, safe=True)


