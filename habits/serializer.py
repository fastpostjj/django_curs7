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
                message = f'У приятной привычки не может быть вознаграждения и связанной приятной привычки!'
                raise serializers.ValidationError(message)
        else:
            if (linked_habit is None) and (compensation is None):
                message = f'У полезной привычки должно быть вознаграждение или связанная приятная привычка!'
                raise serializers.ValidationError(message)
            else:
                if not (compensation is None or linked_habit is None):
                    message = f'У полезной привычки не может быть одновременно вознаграждения и связанной приятной привычки!'
                    raise serializers.ValidationError(message)


# class HabitsLinkedCustomValidator:
#     def __init__(self, field):
#         self.field = field

#     def __call__(self, value):
#         linked_habit = value.get('linked_habit')
#         compensation = value.get('compensation')

#         if not (compensation is None or linked_habit is None):
#             message = f'У полезной привычки не может быть одновременно вознаграждения и связанной приятной привычки!'
#             raise serializers.ValidationError(message)


# class Habits_pleasantSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Habits_pleasant
#         fields = '__all__'

#     validators = [HabitsTimeCustomValidator(field='time_for_action')]


class HabitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habits
        fields = '__all__'

    validators = [HabitsTimeCustomValidator(field='time_for_action'),
                #   HabitsLinkedCustomValidator(field='linked_habit'),
                #   HabitsLinkedCustomValidator(field='compensation'),
                  HabitsPleasantCustomValidator(field='is_pleasant')
                  ]


# class TelegramUserSerializers(serializers.ModelSerializer):

#     class Meta:
#         model = TelegramUser
#         fields = (
#             'chat_id',
#             'phone',
#             'is_subscripted'
#         )


# class MilageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Milage
#         fields = '__all__'


# class CarSerializer(serializers.ModelSerializer):
#     last_milage = serializers.IntegerField(source='milage_set.last.milage', default=0, read_only=True)
#     milage = MilageSerializer(many=True, read_only=True, source='milage_set')

#     class Meta:
#         model = Car
#         fields = '__all__'


# class MotorcycleSerializer(serializers.ModelSerializer):
#     last_milage = serializers.SerializerMethodField()

#     class Meta:
#         model = Motorcycle
#         fields = '__all__'

#     def get_last_milage(self, instance):
#         milage = instance.milage_set.all().last()
#         if milage:
#             return milage.milage
#         return 0


# class CarCreateSerializer(serializers.ModelSerializer):
#     milage = MilageSerializer(many=True)

#     class Meta:
#         model = Car
#         fields = '__all__'

#     def create(self, validated_data):
#         milage = validated_data.pop('milage')
#         car_instance = Car.objects.create(**validated_data)
#         for m in milage:
#             Milage.objects.create(car=car_instance, *m)
#         return car_instance
