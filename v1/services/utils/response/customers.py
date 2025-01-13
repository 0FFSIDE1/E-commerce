
def get_customers_response(customer, queryset):
    """Response Data for GET request i.e all Customer record"""
    data = {
        "status": "success",
        "code": 200,
        "message": "List of all Customers retrieved successfully.",
        "count": queryset,
        "Customers": customer,
    }
    return data

def post_customers_response(customer):
    """Response Data for POST request i.e create new Customer record"""
    data = {
        "status": "success",
        "code": 201,
        "message": "Customer record added successfully.",
        "Customer": customer,
    }
    
    return data

def retrieve_customer_response_data(customer):
    """Response Data for GET request i.e single Customer record"""
    data = {
        "status": "success",
        "code": 200,
        "message": "Customer record retrieved successfully.",
        "Customer": customer,
    }
    return data

def update_customer_response_data(customer):
    """Response Data for PUT or PATCH request i.e update single Customer record"""
    data = {
        "status": "success",
        "code": 200,
        "message": "Customer record updated successfully.",
        "Customer": customer,
    }
    return data

def destroy_customer_response_data():
    """Response Data for Delete request i.e Delete single Customer record"""
    data = {
        "status": "success",
        "code": 204,
        "message": "Customer record deleted successfully.",
    }
    return data

