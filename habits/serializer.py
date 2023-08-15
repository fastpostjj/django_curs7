from rest_framework import serializers
from datetime import timedelta
from habits.models import Habits


class HabitsTimeCustomValidator:
    """
    Валидатор длительности времени на выполнение действия.
    Не более 120 секунд.
    """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        time = value.get('time_for_action')
        if time > timedelta(seconds=120):
            message = f'Время на выполнение привычки не должно превышать 2 минуты (120 секунд)!'
            raise serializers.ValidationError(message)


class HabitsPleasantCustomValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        is_pleasant = value.get('is_pleasant')
        linked_habit = value.get('linked_habit')
        compensation = value.get('compensation')
        if is_pleasant:
            if linked_habit is not None or compensation is not None:
                message = f'У приятной привычки не может быть одновременно вознаграждения и связанной приятной привычки!'
                raise serializers.ValidationError(message)
        else:
            if (linked_habit is None) and (compensation is None):
                message = f'У полезной привычки должно быть вознаграждение или связанная приятная привычка!'
                raise serializers.ValidationError(message)
            else:
                if not (compensation is None or linked_habit is None):
                    message = f'У полезной привычки не может быть одновременно вознаграждения и связанной приятной привычки!'
                    raise serializers.ValidationError(message)


class HabitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habits
        fields = '__all__'

    validators = [HabitsTimeCustomValidator(field='time_for_action'),
                  HabitsPleasantCustomValidator(field='is_pleasant')
                  ]
