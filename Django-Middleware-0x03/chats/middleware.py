import logging
import time
from datetime import datetime
from django.http import HttpResponseForbidden
#from django.http import HttpResponseTooManyRequests 
from django.http import HttpResponse

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

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        current_hour = datetime.now().hour

        # We deny access if the hour is 21 (9 PM) or later, OR 6 AM or earlier.
        if ((current_hour >= 21) or (current_hour <= 6)):

            # Short-circuit the request and return a 403 Forbidden response
            return HttpResponseForbidden("Chat access is restricted between 9 PM and 6 AM.")

        # Proceed to the next middleware/view ONLY if access is allowed
        response = self.get_response(request)

        return response

class OffensiveLanguageMiddleware:
    # Class-level dictionary to store state: { 'ip_address': [timestamp1, timestamp2, ...] }
    IP_REQUEST_TIMES = {} 
    RATE_LIMIT = 5    # Max messages per time window
    TIME_WINDOW = 60  # Time window in seconds (1 minute)

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        # 1. Safely extract the client IP address (Fixing Typo)
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR') 
        if x_forwarded_for:
            # Fix: Added the dot before .split()
            ip_address = x_forwarded_for.split(',')[0].strip() 
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        # 2. Only apply rate limit logic to POST requests (new messages)
        if request.method == 'POST':
            current_time = time.time()

            # A) Ensure the IP address has an entry in our dictionary
            if ip_address not in self.IP_REQUEST_TIMES:
                self.IP_REQUEST_TIMES[ip_address] = []

            # B) Cleanup: Remove old timestamps that are outside the 60-second window
            cutoff_time = current_time - self.TIME_WINDOW
            self.IP_REQUEST_TIMES[ip_address] = [
                t for t in self.IP_REQUEST_TIMES[ip_address] if t > cutoff_time
            ]

            # C) Check Limit: If the count of recent requests is too high
            if len(self.IP_REQUEST_TIMES[ip_address]) >= self.RATE_LIMIT:
                # D) Short-circuit and return the 429 error
                #return HttpResponseTooManyRequests("Rate limit exceeded: 5 messages per minute.")
                return HttpResponse("Rate limit exceeded: 5 messages per minute.", status=429)
            else:
                # E) Record: If not limited, record the current time for the successful POST
                self.IP_REQUEST_TIMES[ip_address].append(current_time) 

        # Proceed to the next middleware/view
        response = self.get_response(request)
        return response

class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        user = request.user

        if user.is_authenticated and (not user.is_superuser and not user.is_staff):
            return HttpResponseForbidden("You do not have the required role permissions (Admin/Moderator) to access this action.")
        
        # Proceed to the next middleware
        response = self.get_response(request)
        return response  


class RestrictByMethodMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self,request):

        UNSAFE_methods = ['DELETE','POST','PUT','PATCH']

        if (request.method in UNSAFE_methods and not request.user.is_authenticated):            
            return HttpResponseForbidden("You are not Authorirized to perform this action")

         # Proceed to the next middleware/view ONLY if access is allowed
        response = self.get_response(request)

        return response
