def get_orders_response(order, count):
    data = {
        "status": "success",
        "code": 200,
        "message": "List of all Orders retrieved successfully.",
        "count": count,
        "orders": order,
    }
    return data

def post_order_response(order):
    data = {
        "status": "success",
        "code": 201,
        "message": "Order created successfully.",
        "order": order,
    }
    return data

def retrieve_order_response_data(order):
    data = {
        "status": "success",
        "code": 200,
        "message": "Order retrieved successfully.",
        "order": order,
    }
    return data

def update_order_response_data(order):
    data = {
        "status": "success",
        "code": 200,
        "message": "Order updated successfully.",
        "order": order,
    }
    return data

def destroy_order_response_data():
    data = {
        "status": "success",
        "code": 204,
        "message": "Order deleted successfully.",
    }
    return data
