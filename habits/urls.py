from django.urls import path
from rest_framework.routers import DefaultRouter
from habits.views import HabitsListView, HabitsCreateAPIView, \
    HabitsUpdateAPIView, HabitsRetrieveAPIView, \
    HabitsDestroyAPIView, HabitsPublicListView, CheckMessageBotView,\
    SendMessagBotView

router = DefaultRouter()

urlpatterns = [
    path('habits/retrieve/<int:pk>/',
         HabitsRetrieveAPIView.as_view(),
         name='habits_retrieve'),
    path('habits/update/<int:pk>/',
         HabitsUpdateAPIView.as_view(),
         name='habits_update'),
    path('habits/create/', HabitsCreateAPIView.as_view(),
         name='habits_create'),
    path('habits/', HabitsListView.as_view(),
         name='habits_list'),
    path('habits/destroy/<int:pk>/',
         HabitsDestroyAPIView.as_view(),
         name='habits_destroy'),
    path('public/', HabitsPublicListView.as_view(),
         name='habits_public_list'),
    path('check_message_bot/',
         CheckMessageBotView.as_view(),
         name='check_message'),
    path('send_message_bot/',
         SendMessagBotView.as_view(),
         name='send_message'),

] + router.urls
