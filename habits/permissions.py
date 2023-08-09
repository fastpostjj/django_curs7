from rest_framework.permissions import BasePermission

# from university.models import Lesson, Curs, Subscription
from habits.models import Habits_pleasant, Habits_useful


class OwnerOrStaffOrAdminPleasant(BasePermission):
    # проверка для приятных привычек

    def has_permission(self, request, view):
        pass
        if request.method == 'GET':
            # для списка не проверяем владельца
            if request.user.is_staff or request.user.is_superuser:
                return True
            elif 'pk' in view.kwargs:
                # это не список
                habits_pleasant_id = view.kwargs['pk']
                habits_pleasant = Habits_pleasant.objects.get(id=habits_pleasant_id)
                if request.user == Habits_pleasant.user:
                    return True
        return False


class OwnerOrStaffOrAdminUseful(BasePermission):
    # проверка для полезных привычек

    def has_permission(self, request, view):
        if request.method == 'GET':
            # для списка не проверяем владельца
            if request.user.is_staff or request.user.is_superuser:
                return True
            elif 'pk' in view.kwargs:
                # это не список
                habits_useful_id = view.kwargs['pk']
                habits_useful = Habits_useful.objects.get(id=habits_useful_id)
                if request.user == Habits_useful.user:
                    return True
        return False


# class OwnerOrAdmin(BasePermission):

#     def has_permission(self, request, view):
#         if request.user == view.get_object().user:
#             return True
#         elif request.user.is_superuser:
#             return True
#         return False


class OwnerOrStafOrAdminView(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.user:
            return True
        elif request.user.is_staff:
            return True
        elif request.user.is_superuser:
            return True
        return False


# class OwnerOrAdminChange(BasePermission):
#     # для вьюсета для объектов курса
#     def has_object_permission(self, request, view, obj):
#         if request.method.upper() == 'POST':
#             if request.user:
#                 return True
#         elif request.method.upper() in ['PUT', 'PATCH', 'DELETE']:
#             if request.user == obj.owner:
#                 return True
#             elif request.user.is_superuser:
#                 return True
#         elif request.method.upper() == 'GET':
#             # для списка не проверяем владельца
#             if request.user.is_staff or request.user.is_superuser:
#                 return True
#             elif 'pk' in view.kwargs:
#                 # это не список
#                 curs_id = view.kwargs['pk']
#                 curs = Curs.objects.get(id=curs_id)
#                 if request.user == curs.owner:
#                     return True
#         return False

# class OwnerOrAdminChangeSubscribe(BasePermission):
#     # для вьюсета для объектов подписки
#     def has_object_permission(self, request, view, obj):
#         if request.method.upper() == 'POST':
#             if request.user:
#                 return True
#         elif request.method.upper() in ['PUT', 'PATCH', 'DELETE']:
#             if request.user == obj.user:
#                 return True
#             elif request.user.is_superuser:
#                 return True
#         elif request.method.upper() == 'GET':
#             # для списка не проверяем владельца
#             if request.user.is_staff or request.user.is_superuser:
#                 return True
#             elif 'pk' in view.kwargs:
#                 # это не список
#                 sub_id = view.kwargs['pk']
#                 subs = Subscription.objects.get(id=sub_id)
#                 if request.user == subs.user:
#                     return True
#         return False
