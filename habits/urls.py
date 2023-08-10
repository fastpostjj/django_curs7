from django.urls import path
from rest_framework.routers import DefaultRouter
# from habits.views import Habits_PleasantListView, Habits_UsefulCreateAPIView,\
#     Habits_PleasantUpdateAPIView, \
#     Habits_PleasantDestroyAPIView, Habits_PleasantRetrieveAPIView,\
from habits.views import HabitsListView, HabitsCreateAPIView, \
    HabitsUpdateAPIView, HabitsRetrieveAPIView, \
    HabitsDestroyAPIView, HabitsPublicListView

router = DefaultRouter()
# router.register(r'curs', CursViewSet, basename='curs')

urlpatterns = [
    #     path('habits_pleasant/', Habits_PleasantListView.as_view(),
    #          name='habits_pleasant_list'),
    #     path('habits_pleasant/create/', Habits_PleasantCreateAPIView.as_view(),
    #          name='habits_pleasant_create'),
    #     path('habits_pleasant/update/<int:pk>/',
    #          Habits_PleasantUpdateAPIView.as_view(),
    #          name='habits_pleasant_update'),
    #     path('habits_pleasant/destroy/<int:pk>/',
    #          Habits_PleasantDestroyAPIView.as_view(),
    #          name='habits_pleasant_destroy'),
    #     path('habits_pleasant/retrieve/<int:pk>/',
    #          Habits_PleasantRetrieveAPIView.as_view(),
    #          name='habits_pleasant_retrieve'),

    #     path('habits_useful/retrieve/<int:pk>/',
    #          Habits_UsefulRetrieveAPIView.as_view(),
    #          name='habits_useful_retrieve'),
    #     path('habits_useful/update/<int:pk>/',
    #          Habits_UsefulUpdateAPIView.as_view(),
    #          name='habits_useful_update'),
    #     path('habits_useful/create/', Habits_UsefulCreateAPIView.as_view(),
    #          name='habits_useful_create'),
    #     path('habits_useful/', Habits_UsefulListView.as_view(),
    #          name='habits_useful_list'),
    #     path('habits_useful/destroy/<int:pk>/',
    #          Habits_UsefulDestroyAPIView.as_view(),
    #          name='habits_useful_destroy'),

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

] + router.urls
