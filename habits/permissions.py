from rest_framework.permissions import BasePermission
from habits.models import Habits


class OwnerOrStaffOrAdminHabits(BasePermission):
    # проверка привычек

    def has_permission(self, request, view):
        if request.method in ['GET', 'PUT', 'PATCH']:
            # для списка не проверяем владельца
            if request.user.is_staff or request.user.is_superuser:
                return True
            elif 'pk' in view.kwargs:
                # это не список
                try:
                    habits_id = view.kwargs['pk']
                    habits = Habits.objects.get(id=habits_id)
                    if request.user == habits.user:
                        return True
                    else:
                        return False
                except Habits.DoesNotExist:
                    return False
        elif request.method in ['DELETE']:
            if request.user.is_staff or request.user.is_superuser:
                return True
            elif 'pk' in view.kwargs:
                # это не список
                try:
                    habits_id = view.kwargs['pk']
                    habits = Habits.objects.get(id=habits_id)
                    if request.user == habits.user:
                        return True
                    else:
                        return False
                except Habits.DoesNotExist:
                    return False

        return False


class OwnerOrStaffOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.user:
            return True
        elif request.user.is_staff:
            return True
        elif request.user.is_superuser:
            return True
        return False
