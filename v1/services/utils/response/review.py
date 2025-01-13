
def get_reviews_response(review, queryset):
    """Response Data for GET request i.e all review record"""
    data = {
        "status": "success",
        "code": 200,
        "message": "List of all reviews retrieved successfully.",
        "count": queryset,
        "reviews": review,
    }
    return data

def post_reviews_response(review):
    """Response Data for POST request i.e create new review record"""
    data = {
        "status": "success",
        "code": 201,
        "message": "review record added successfully.",
        "review": review,
    }
    
    return data

def retrieve_review_response_data(review):
    """Response Data for GET request i.e single review record"""
    data = {
        "status": "success",
        "code": 200,
        "message": "review record retrieved successfully.",
        "review": review,
    }
    return data

def update_review_response_data(review):
    """Response Data for PUT or PATCH request i.e update single review record"""
    data = {
        "status": "success",
        "code": 200,
        "message": "review record updated successfully.",
        "review": review,
    }
    return data

def destroy_review_response_data():
    """Response Data for Delete request i.e Delete single review record"""
    data = {
        "status": "success",
        "code": 204,
        "message": "review record deleted successfully.",
    }
    return data

