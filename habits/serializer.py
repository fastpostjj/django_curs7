from rest_framework import serializers
from habits.models import Habits, TelegramUser


class HabitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habits
        fields = '__all__'


class TelegramUserSerializers(serializers.ModelSerializer):

    class Meta:
        model = TelegramUser
        fields = (
            'chat_id',
            'phone',
            'is_subscripted'
        )


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
