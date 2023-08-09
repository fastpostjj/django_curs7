from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from habits.serializer import Habits_pleasantSerializer, \
    Habits_usefulSerializer
from habits.models import Habits_useful, Habits_pleasant
from habits.paginations import PaginationClass
from habits.permissions import OwnerOrStaffOrAdminUseful, \
    OwnerOrStaffOrAdminPleasant


# Create your views here.
class Habits_PleasantListView(generics.ListAPIView):
    """
    list view pleasant habits
    Выводит список приятных привычек. Для просмотра требуется авторизация.
    Администратор или менеджер могут просматривать все привычки, обычный
    пользователь - только свои.
    """
    permission_classes = [OwnerOrStaffOrAdminPleasant, IsAuthenticated]
    serializer_class = Habits_pleasantSerializer
    queryset = Habits_pleasant.objects.all()
    pagination_class = PaginationClass

    def get(self, request):
        queryset = Habits_pleasant.objects.all()
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = Habits_pleasantSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        if not self.request:
            return Habits_pleasant.objects.none()
        if not self.request.user.is_authenticated:
            return Habits_pleasant.objects.none()
        else:
            if self.request.user.is_staff or self.request.user.is_superuser:
                # Пользователь с правами персонала или администратора может видеть все привычки
                queryset = queryset.order_by('time')
            else:
                # Обычный пользователь - только свои
                queryset = queryset.filter(
                    user=self.request.user).order_by('time')
            return queryset


class Habits_UsefulListView(generics.ListAPIView):
    """
    list view useful habits
    Выводит список полезных привычек. Для просмотра требуется авторизация.
    Администратор или менеджер могут просматривать все привычки, обычный
    пользователь - только свои.
    """
    permission_classes = [OwnerOrStaffOrAdminUseful, IsAuthenticated]
    serializer_class = Habits_usefulSerializer
    queryset = Habits_useful.objects.all()
    pagination_class = PaginationClass

    def get(self, request):
        queryset = Habits_useful.objects.all()
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = Habits_usefulSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        if not self.request:
            return Habits_useful.objects.none()
        if not self.request.user.is_authenticated:
            return Habits_useful.objects.none()
        else:
            if self.request.user.is_staff or self.request.user.is_superuser:
                # Пользователь с правами персонала или администратора может видеть все привычки
                queryset = queryset.order_by('time')
            else:
                # Обычный пользователь - только свои
                queryset = queryset.filter(
                    user=self.request.user).order_by('time')
            return queryset


class Habits_UsefulCreateAPIView(generics.CreateAPIView):
    """
    create view Habits_useful
    """
    permission_classes = [IsAuthenticated]
    serializer_class = Habits_usefulSerializer
    queryset = Habits_useful.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self, *args, **kwargs):
        # Для совместимости с автодокументацией
        queryset = super().get_queryset()
        if not self.request:
            return Habits_useful.objects.none()
        else:
            return queryset


class Habits_PleasantCreateAPIView(generics.CreateAPIView):
    """
    create view Habits_pleasant
    """
    permission_classes = [IsAuthenticated]
    serializer_class = Habits_pleasantSerializer
    queryset = Habits_pleasant.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self, *args, **kwargs):
        # Для совместимости с автодокументацией
        queryset = super().get_queryset()
        if not self.request:
            return Habits_pleasant.objects.none()
        else:
            return queryset


class Habits_PleasantUpdateAPIView(generics.UpdateAPIView):
    """
    update view Habits_pleasant
    """
    permission_classes = [OwnerOrStaffOrAdminPleasant, IsAuthenticated]
    serializer_class = Habits_pleasantSerializer
    queryset = Habits_pleasant.objects.all()

    def get_queryset(self, *args, **kwargs):
        # Для совместимости с автодокументацией
        queryset = super().get_queryset()
        if not self.request:
            return Habits_pleasant.objects.none()
        else:
            return queryset


class Habits_UsefulUpdateAPIView(generics.UpdateAPIView):
    """
    update view Habits_useful
    """
    permission_classes = [OwnerOrStaffOrAdminPleasant, IsAuthenticated]
    serializer_class = Habits_usefulSerializer
    queryset = Habits_useful.objects.all()

    def get_queryset(self, *args, **kwargs):
        # Для совместимости с автодокументацией
        queryset = super().get_queryset()
        if not self.request:
            return Habits_useful.objects.none()
        else:
            return queryset


class Habits_PleasantDestroyAPIView(generics.DestroyAPIView):
    """
    destroy view Habits_pleasant
    """
    permission_classes = [OwnerOrStaffOrAdminPleasant, IsAuthenticated]
    serializer_class = Habits_pleasantSerializer
    queryset = Habits_pleasant.objects.all()

    def get_queryset(self, *args, **kwargs):
        # Для совместимости с автодокументацией
        queryset = super().get_queryset()
        if not self.request:
            return Habits_pleasant.objects.none()
        else:
            return queryset


class Habits_PleasantRetrieveAPIView(generics.RetrieveAPIView):
    """
    retrieve view Habits_pleasant
    """
    permission_classes = [OwnerOrStaffOrAdminUseful, IsAuthenticated]
    serializer_class = Habits_pleasantSerializer
    queryset = Habits_pleasant.objects.all()

    def get_queryset(self, *args, **kwargs):
        # Для совместимости с автодокументацией
        queryset = super().get_queryset()
        if not self.request:
            return Habits_pleasant.objects.none()
        else:
            return queryset


class Habits_UsefulDestroyAPIView(generics.DestroyAPIView):
    """
    destroy view Habits_pleasant
    """
    permission_classes = [OwnerOrStaffOrAdminUseful, IsAuthenticated]
    serializer_class = Habits_pleasantSerializer
    queryset = Habits_pleasant.objects.all()

    def get_queryset(self, *args, **kwargs):
        # Для совместимости с автодокументацией
        queryset = super().get_queryset()
        if not self.request:
            return Habits_pleasant.objects.none()
        else:
            return queryset


class Habits_UsefulRetrieveAPIView(generics.RetrieveAPIView):
    """
    retrieve view Habits_useful
    """
    permission_classes = [OwnerOrStaffOrAdminUseful, IsAuthenticated]
    serializer_class = Habits_usefulSerializer
    queryset = Habits_useful.objects.all()

    def get_queryset(self, *args, **kwargs):
        # Для совместимости с автодокументацией
        queryset = super().get_queryset()
        if not self.request:
            return Habits_useful.objects.none()
        else:
            return queryset
