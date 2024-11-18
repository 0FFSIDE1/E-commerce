
def get_products_response(product, queryset):
    """Response Data for GET request i.e all Product record"""
    data = {
        "status": "success",
        "code": 200,
        "message": "List of all Products retrieved successfully.",
        "count": queryset,
        "Products": product,
    }
    return data

def post_products_response(product):
    """Response Data for POST request i.e create new Product record"""
    data = {
        "status": "success",
        "code": 201,
        "message": "Product record added successfully.",
        "Product": product,
    }
    
    return data

def retrieve_product_response_data(product):
    """Response Data for GET request i.e single Product record"""
    data = {
        "status": "success",
        "code": 200,
        "message": "Product record retrieved successfully.",
        "Product": product,
    }
    return data

def update_product_response_data(product):
    """Response Data for PUT or PATCH request i.e update single Product record"""
    data = {
        "status": "success",
        "code": 200,
        "message": "Product record updated successfully.",
        "Product": product,
    }
    return data

def destroy_product_response_data():
    """Response Data for Delete request i.e Delete single Product record"""
    data = {
        "status": "success",
        "code": 204,
        "message": "Product record deleted successfully.",
    }
    return data

