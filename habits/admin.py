from django.contrib import admin
from habits.models import Habits, TelegramUser


# Register your models here.
@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'chat_id',
        'phone',
        'is_subscripted'
    )
    list_display_links = (
        'id',
        'chat_id',
        'phone',
        'is_subscripted'
    )
    list_filter = (
        'id',
        'chat_id',
        'phone',
        'is_subscripted'
    )
    search_fields = (
        'id',
        'chat_id',
        'phone',
        'is_subscripted'
    )


@admin.register(Habits)
class HabitsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'activity',
        'time',
        'place',
        'period',
        'is_pleasant',
        'is_public',
        'compensation'
    )
    list_display_links = (
        'id',
        'user',
        'activity',
        'time',
        'place',
        'period',
        'is_pleasant',
        'is_public',
        'compensation'
    )
    list_filter = (
        'id',
        'user',
        'activity',
        'time',
        'place',
        'period',
        'is_pleasant',
        'is_public',
        'compensation'
    )
    search_fields = (
        'id',
        'user',
        'activity',
        'time',
        'place',
        'period',
        'is_pleasant',
        'is_public',
        'compensation'
    )
