from rest_framework import pagination


class HabitPagination(pagination.PageNumberPagination):
    page_size = 5
    page_query_param = 'page'
    max_page_size = 100
