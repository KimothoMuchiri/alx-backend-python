from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    # This sets the number of items per page for this specific class
    page_size = 20