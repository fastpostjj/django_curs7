from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from habits.serializer import HabitsSerializer
from habits.models import Habits
from habits.paginations import PaginationClass


# Create your views here.
class HabitsListView(generics.ListAPIView):
    """
    list view habits
    Выводит список привычек. Для просмотра требуется авторизация.
    Администратор или менеджер могут просматривать все привычки, обычный
    пользователь - только свои.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = HabitsSerializer
    queryset = Habits.objects.all()
    pagination_class = PaginationClass

    def get(self, request):
        queryset = Habits.objects.all()
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = HabitsSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        if not self.request:
            return Habits.objects.none()
        if not self.request.user.is_authenticated:
            return Habits.objects.none()
        else:
            if self.request.user.is_staff or self.request.user.is_superuser:
                # Пользователь с правами персонала или администратора может видеть все привычки
                queryset = queryset.order_by('time')
            else:
                # Обычный пользователь - только свои
                queryset = queryset.filter(user=self.request.user).order_by('time')
            return queryset



class HabitsCreateAPIView(generics.CreateAPIView):
    pass


class HabitsUpdateAPIView(generics.UpdateAPIView):
    pass


class HabitsDestroyAPIView(generics.DestroyAPIView):
    pass


class HabitsRetrieveAPIView(generics.RetrieveAPIView):
    pass
