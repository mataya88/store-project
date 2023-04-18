from rest_framework.pagination import PageNumberPagination

# to make specific paginations other than the global

class DefaultPagination(PageNumberPagination):
    page_size = 20