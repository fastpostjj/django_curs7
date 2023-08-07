from django.urls import path
from rest_framework.routers import DefaultRouter
from habits.views import HabitsListView, HabitsCreateAPIView, HabitsUpdateAPIView,\
    HabitsDestroyAPIView, HabitsRetrieveAPIView

router = DefaultRouter()
# router.register(r'curs', CursViewSet, basename='curs')

urlpatterns = [
    path('habitss/', HabitsListView.as_view(), name='habits_list'),
    path('habitss/create/', HabitsCreateAPIView.as_view(), name='habits_create'),
    path('habitss/update/<int:pk>/', HabitsUpdateAPIView.as_view(), name='habits_update'),
    path('habitss/destroy/<int:pk>/', HabitsDestroyAPIView.as_view(), name='habits_destroy'),
    path('habitss/retrieve/<int:pk>/', HabitsRetrieveAPIView.as_view(), name='habits_retrieve'),

              ] + router.urls
