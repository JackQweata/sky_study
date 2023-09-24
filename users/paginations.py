from rest_framework.pagination import PageNumberPagination


class ListProductsPagination(PageNumberPagination):
    page_size = 10

