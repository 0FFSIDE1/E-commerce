from asgiref.sync import sync_to_async    

@sync_to_async
def create_session_if_not_exists(request):
    """ This function creates a session if it does not exist """
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key