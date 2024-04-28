from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.UserLogin, name='login'),
    path('logout/', views.UserLogout, name='logout'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('update-profile/<str:pk>', views.update_profile, name='update-profile'),

    path('registeration/', views.UserRegisteration, name='registeration'),

    path('', views.home, name='home'),
    path('room/<str:pk>', views.room, name='room'),
    path('create-room/', views.create_room, name='create_room'),
    path('update-room/<str:pk>', views.update_room, name='update_room'),
    path('delete_room/<str:pk>', views.delete_room, name='delete_room'),
    
    path('delete-message/<str:pk>', views.deleteMessage, name='delete-message'),
]