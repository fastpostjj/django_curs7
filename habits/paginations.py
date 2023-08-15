from rest_framework.pagination import PageNumberPagination


class PaginationClass(PageNumberPagination):
    # Количество элементов на странице
    page_size = 5
    # Параметр запроса для указания количества элементов на странице
    page_size_query_param = 'page_size'
    # Максимальное количество элементов на странице
    max_page_size = 10
