from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response



class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'status': 200,
            'message': 'Data reterived successfully!!!',
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        },status=200)



def get_paginated_queryset(queryset,request,serializer_class):
    paginator = CustomPagination()
    result_page = paginator.paginate_queryset(queryset,request)
    serializer = serializer_class(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)
