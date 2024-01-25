from django.urls import path
from .views import RoomList, RoomDetail, PlayerDetail, PlayerList

urlpatterns = [
    path('rooms/', RoomList.as_view()),
    path('rooms/<int:pk>/', RoomDetail.as_view()),
    path('players/', PlayerList.as_view()),
    path('players/<int:pk>/', PlayerDetail.as_view()),
]
