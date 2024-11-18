def Error_Response(error, message):
    ERROR_RESPONSE = {
    "error": f"{error}",
    "message": f"{message} record not found with the provided ID.",
    "code": 404
}
    return ERROR_RESPONSE