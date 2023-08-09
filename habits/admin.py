from django.contrib import admin
from habits.models import Habits_useful, Habits_pleasant


# Register your models here.
# @admin.register(TelegramUser)
# class TelegramUserAdmin(admin.ModelAdmin):
#     list_display = (
#         'id',
#         'chat_id',
#         'phone',
#         'is_subscripted'
#     )
#     list_display_links = (
#         'id',
#         'chat_id',
#         'phone',
#         'is_subscripted'
#     )
#     list_filter = (
#         'id',
#         'chat_id',
#         'phone',
#         'is_subscripted'
#     )
#     search_fields = (
#         'id',
#         'chat_id',
#         'phone',
#         'is_subscripted'
#     )


@admin.register(Habits_pleasant)
class Habits_pleasantAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'activity',
        'time',
        'place',
        'period',
        # 'is_pleasant',
        'is_public',
        # 'linked_habit',
        # 'compensation'
    )
    list_display_links = (
        'id',
        'user',
        'activity',
        'time',
        'place',
        'period',
        # 'is_pleasant',
        'is_public',
        # 'linked_habit',
        # 'compensation'
    )
    list_filter = (
        'id',
        'user',
        'activity',
        'time',
        'place',
        'period',
        # 'is_pleasant',
        'is_public',
        # 'linked_habit',
        # 'compensation'
    )
    search_fields = (
        'id',
        'user',
        'activity',
        'time',
        'place',
        'period',
        # 'is_pleasant',
        'is_public',
        # 'linked_habit',
        # 'compensation'
    )

@admin.register(Habits_useful)
class Habits_usefulAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'activity',
        'time',
        'place',
        'period',
        # 'is_pleasant',
        'is_public',
        'linked_habit',
        'compensation'
    )
    list_display_links = (
        'id',
        'user',
        'activity',
        'time',
        'place',
        'period',
        # 'is_pleasant',
        'is_public',
        'linked_habit',
        'compensation'
    )
    list_filter = (
        'id',
        'user',
        'activity',
        'time',
        'place',
        'period',
        # 'is_pleasant',
        'is_public',
        'linked_habit',
        'compensation'
    )
    search_fields = (
        'id',
        'user',
        'activity',
        'time',
        'place',
        'period',
        # 'is_pleasant',
        'is_public',
        'linked_habit',
        'compensation'
    )
