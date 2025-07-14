from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('profile/', views.profile_view, name='profile'),
    path('workouts/', views.workouts_view, name='workouts'),
    path('attendance/', views.attendance_view, name='attendance'),
    path('foodlog/', views.foodlog_view, name='foodlog'),
    path('charts/', views.charts_view, name='charts'),
    path('contacts',views.contacts_view, name='contacts'),
    path('faqs/',views.faq_view, name='faqs'),
    path('workouts/exercises/<int:workout_id>/', views.exercise_detail_view, name='workout_detail'),
    path('workouts/create/', views.create_workout_plan_view, name='create_workout_plan'),
    path('workouts/exercises/<int:workout_id>/create/', views.create_exercise_view, name='create_exercise'),
    path('workouts/exercises/suggested/', views.suggested_exercises_view, name='suggested_exercises'),
    path('workouts/exercises/suggested/fetch', views.fetch_suggestions, name='fetch_suggestions'),
    path('foodlog/<int:foodlog_id>/', views.food_detail_view, name='foodlog_detail'),
    path('foodlog/create/', views.create_food_plan_view, name='create_foodlog'),
    path('foodlog/<int:food_plan_id>/create/', views.create_food, name='create_food'),
    path('register/', views.render_register_page, name='register'),
    path('login/', views.render_login_page, name='login'),
    path('register/membership/', views.register_membership, name='register_membership'),
    path('logout/', views.user_logout, name='logout'),
    path('attendance/check-in/', views.check_in_view, name='check_in'),
    path('attendance/check-out/', views.check_out_view, name='check_out'),
]