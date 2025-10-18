import logging
from datetime import datetime

# get an instance of your logger
request_logger = logging.getLogger('request_logger')

class RequestLoggingMiddleware:
    def __init__(self,get_response):
        # Django passes the next calable middleware or view
        self.get_response = get_response

    def __call__(self, request):
        # This is the main request/response hook. 
        log_message = f"{datetime.now()} - User:{request.user}- Path:{request.path}"

        # log the message t the logger instance
        request_logger.info(log_message) 
        
        # Proceed to the next middleware/view
        response = self.get_response(request)

        # The Response Phase logic would go here, but for this task,
        # logging the request is usually done in the Request Phase.

        return response

