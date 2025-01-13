
def get_feedbacks_response(feedback, queryset):
    """Response Data for GET request i.e all Feedback record"""
    data = {
        "status": "success",
        "code": 200,
        "message": "List of all Feedbacks retrieved successfully.",
        "count": queryset,
        "Feedbacks": feedback,
    }
    return data

def post_feedbacks_response(feedback):
    """Response Data for POST request i.e create new Feedback record"""
    data = {
        "status": "success",
        "code": 201,
        "message": "Feedback record added successfully.",
        "Feedback": feedback,
    }
    
    return data

def retrieve_feedback_response_data(feedback):
    """Response Data for GET request i.e single Feedback record"""
    data = {
        "status": "success",
        "code": 200,
        "message": "Feedback record retrieved successfully.",
        "Feedback": feedback,
    }
    return data

def update_feedback_response_data(feedback):
    """Response Data for PUT or PATCH request i.e update single Feedback record"""
    data = {
        "status": "success",
        "code": 200,
        "message": "Feedback record updated successfully.",
        "Feedback": feedback,
    }
    return data

def destroy_feedback_response_data():
    """Response Data for Delete request i.e Delete single Feedback record"""
    data = {
        "status": "success",
        "code": 204,
        "message": "Feedback record deleted successfully.",
    }
    return data

