from django.contrib import admin
from .models import (
    Member, WorkoutPlan, Attendance, ExerciseLog,
    FoodLog, Slider, FAQ, Payment,FoodPlan
)

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'subscription_end', 'is_active')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone')
    list_filter = ('is_active',)

@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ('member', 'date', 'description')
    list_filter = ('date',)
    search_fields = ('member__user__username', 'description')

@admin.register(FoodPlan)
class FoodPlanAdmin(admin.ModelAdmin):
    list_display = ('member', 'date', 'description')
    list_filter = ('date',)
    search_fields = ('member__user__username', 'description')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('member', 'date')
    list_filter = ('date',)
    search_fields = ('member__user__username',)

@admin.register(ExerciseLog)
class ExerciseLogAdmin(admin.ModelAdmin):
    list_display = ('member', 'activity_type', 'date')
    list_filter = ('activity_type', 'date')
    search_fields = ('member__user__username', 'activity_type')

@admin.register(FoodLog)
class FoodLogAdmin(admin.ModelAdmin):
    list_display = ('member', 'food_name', 'calories', 'protein', 'carbs', 'fat', 'date')
    list_filter = ('date',)
    search_fields = ('member__user__username', 'food_name')

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question',)
    search_fields = ('question', 'answer')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('member', 'amount', 'method', 'date')
    list_filter = ('method', 'date')
    search_fields = ('member__user__username',)
