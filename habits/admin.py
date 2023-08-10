from django.contrib import admin
from habits.models import Habits, BotMessages


# Register your models here.
@admin.register(BotMessages)
class BotMessageAdmin(admin.ModelAdmin):
    list_display = (
        'message_id',
        'message_text',
        'user'
    )
    list_display_links = (
        'message_id',
        'message_text',
        'user'
    )
    list_filter = (
        'message_id',
        'message_text',
        'user'
    )
    search_fields = (
        'message_id',
        'message_text',
        'user'
    )

@admin.register(Habits)
class HabitsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'activity',
        'datetime_start',
        
        'time',
        'place',
        'period',
        # 'is_pleasant',
        'is_public',
        'linked_habit',
        'compensation',
        'last_time_send'
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
        'compensation',
        'last_time_send'
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
        'compensation',
        'last_time_send'
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
        'compensation',
        'last_time_send'
    )

# @admin.register(Habits_useful)
# class Habits_usefulAdmin(admin.ModelAdmin):
#     list_display = (
#         'id',
#         'user',
#         'activity',
#         'time',
#         'place',
#         'period',
#         # 'is_pleasant',
#         'is_public',
#         'linked_habit',
#         'compensation'
#     )
#     list_display_links = (
#         'id',
#         'user',
#         'activity',
#         'time',
#         'place',
#         'period',
#         # 'is_pleasant',
#         'is_public',
#         'linked_habit',
#         'compensation'
#     )
#     list_filter = (
#         'id',
#         'user',
#         'activity',
#         'time',
#         'place',
#         'period',
#         # 'is_pleasant',
#         'is_public',
#         'linked_habit',
#         'compensation'
#     )
#     search_fields = (
#         'id',
#         'user',
#         'activity',
#         'time',
#         'place',
#         'period',
#         # 'is_pleasant',
#         'is_public',
#         'linked_habit',
#         'compensation'
#     )
