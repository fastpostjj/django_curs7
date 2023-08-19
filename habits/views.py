from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from habits.tasks import send_habits
from habits.serializer import HabitsSerializer
from habits.models import Habits
from habits.paginations import PaginationClass
from habits.permissions import OwnerOrStaffOrAdminHabits
from habits.services.services import check_message_bot, create_periodic_task, \
    update_periodic_task, del_periodic_task


# Create your views here.


class HabitsPublicListView(generics.ListAPIView):
    """
    view public habits list
    Выводит список публичных привычек всех пользователей.
    Доступно авторизованным пользователям.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = HabitsSerializer
    queryset = Habits.objects.all()
    pagination_class = PaginationClass

    def get(self, request):
        queryset = Habits.objects.filter(is_public=True).order_by('id')
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = HabitsSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)


class HabitsListView(generics.ListAPIView):
    """
    list view habits
    Выводит список привычек. Для просмотра требуется авторизация.
    Администратор или менеджер могут просматривать все привычки, обычный
    пользователь - только свои.
    """
    permission_classes = [OwnerOrStaffOrAdminHabits, IsAuthenticated]
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
                # Пользователь с правами персонала или администратора
                # может видеть все привычки
                queryset = queryset.order_by('time')
            else:
                # Обычный пользователь - только свои
                queryset = queryset.filter(
                    user=self.request.user).order_by('time')
            return queryset


class HabitsCreateAPIView(generics.CreateAPIView):
    """
    create view Habits
    """
    permission_classes = [IsAuthenticated]
    serializer_class = HabitsSerializer
    queryset = Habits.objects.all()

    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        instance = serializer.save(user=self.request.user)
        # создаем периодическую задачу по рассылке привычки
        return create_periodic_task(instance)

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        if not self.request:
            return Habits.objects.none()
        else:
            return queryset


class HabitsUpdateAPIView(generics.UpdateAPIView):
    """
    update view Habits
    """
    permission_classes = [OwnerOrStaffOrAdminHabits, IsAuthenticated]
    serializer_class = HabitsSerializer
    queryset = Habits.objects.all()

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        if not self.request:
            return Habits.objects.none()
        else:
            return queryset

    def perform_update(self, serializer):
        instance = self.get_object()
        old_instance = instance
        instance = serializer.save()

        # обновляем периодическую задачу по рассылке привычки
        update_periodic_task(old_instance, instance)
        return isinstance


class HabitsDestroyAPIView(generics.DestroyAPIView):
    """
    destroy view Habits
    """
    permission_classes = [OwnerOrStaffOrAdminHabits, IsAuthenticated]
    serializer_class = HabitsSerializer
    queryset = Habits.objects.all()

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        if not self.request:
            return Habits.objects.none()
        else:
            return queryset

    def perform_destroy(self, instance):
        # удаляем периодическую задачу по рассылке привычки
        del_periodic_task(instance)
        instance.delete()


class HabitsRetrieveAPIView(generics.RetrieveAPIView):
    """
    retrieve view Habits
    """
    permission_classes = [OwnerOrStaffOrAdminHabits, IsAuthenticated]
    serializer_class = HabitsSerializer
    queryset = Habits.objects.all()

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        if not self.request:
            return Habits.objects.none()
        else:
            return queryset


class CheckMessageBotView(APIView):
    """
    проверяем сообщения от бота и при необходимости
    создаем новых пользователей
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Success'),
            204: openapi.Response(description='Unsuccess'),

        }
    )
    def get(self, request):
        result = check_message_bot()

        if result:
            return Response(status.HTTP_200_OK)
        else:
            return Response(status.HTTP_204_NO_CONTENT)


class SendMessagBotView(APIView):
    """
    создаем задачи на рассылку привычек
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Success'),
        }
    )
    def get(self, request):
        send_habits()
        return Response(status.HTTP_200_OK)
