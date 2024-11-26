def post_notifications_response(notification):
    """Response Data for POST request i.e create new notification record"""
    data = {
        "status": "success",
        "code": 201,
        "message": "notification record added successfully.",
        "notification": notification,
    }
    
    return data

def retrieve_notification_response_data(notification):
    """Response Data for GET request i.e single notification record"""
    data = {
        "status": "success",
        "code": 200,
        "message": "notification record retrieved successfully.",
        "notification": notification,
    }
    return data

def update_notification_response_data(notification):
    """Response Data for PUT or PATCH request i.e update single notification record"""
    data = {
        "status": "success",
        "code": 200,
        "message": "notification record updated successfully.",
        "notification": notification,
    }
    return data

def destroy_notification_response_data():
    """Response Data for Delete request i.e Delete single notification record"""
    data = {
        "status": "success",
        "code": 204,
        "message": "notification record deleted successfully.",
    }
    return data

