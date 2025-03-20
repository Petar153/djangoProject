from django.urls import path
from . import views

app_name="accounts"
urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('profile/', views.dashboard, name="profile_login"),
    path('profile/<int:user_id>', views.profile, name="profile"),
    path('profile/rate/', views.rate, name="create-rate"),
    path("signup/", views.signup_view, name="signup"),
    path("finishup/", views.finishup, name="finishup"),
    path("dashboard/<int:travel_id>/edit", views.available, name='available'),
    path("dashboard/<int:trip_id>/edit2", views.edit2, name='edit2'),
    path("dashboard/<int:travel_id>/delete", views.delete, name='delete'),
    path('messages/', views.messages, name="messages"),
    path('messages/<int:user_id>', views.chat, name="chat"),
    path('message/<int:user_id>', views.create_message, name="create-message"),
]