from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    # Now add the custom error handling
    if response is not None:
        response.data['custom_error'] = 'Something went Wrong! Please Try later.'

    return response