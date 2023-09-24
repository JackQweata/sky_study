from rest_framework.response import Response
from users.models import Course


class ManagerRestrictionsMixin:
    def create(self, request, *args, **kwargs):
        if self.request.user.groups.filter(name='manager').exists():
            return Response('Нет прав', status=403)
        return super().create(request, *args, **kwargs)


class OwnerProductsMixin:
    def get_queryset(self):
        if self.request.user.groups.filter(name='manager').exists():
            queryset = Course.objects.all().order_by('title')
        else:
            queryset = Course.objects.filter(owner=self.request.user).order_by('title')
        return queryset
