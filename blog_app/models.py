from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta

def default_subscription_end():
    return date.today() + timedelta(days=30)

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=20)
    subscription_end = models.DateField(default=default_subscription_end)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    class Meta:
        verbose_name = 'Member'
        verbose_name_plural = 'Members'


class WorkoutPlan(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return f"{self.member} - {self.date}"

    class Meta:
        verbose_name = 'Workout Plan'
        verbose_name_plural = 'Workout Plans'
        ordering = ['-date']

class Attendance(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    checked_in = models.BooleanField(default=False)
    checked_out = models.BooleanField(default=False)
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.member} - {self.date}"

    class Meta:
        verbose_name = 'Attendance Record'
        verbose_name_plural = 'Attendance Records'
        ordering = ['-date']


class ExerciseLog(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    workout = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE, null=True, blank=True)
    activity_type = models.CharField(max_length=50)
    distance_km = models.FloatField(null=True, blank=True)
    weight_kg = models.FloatField(null=True, blank=True)
    reps = models.IntegerField(null=True, blank=True)
    duration_minutes = models.FloatField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member} - {self.activity_type} on {self.date.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name = 'Exercise Log'
        verbose_name_plural = 'Exercise Logs'
        ordering = ['-date']

class FoodPlan(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.TextField(help_text="List or description of meals for the day")

    def __str__(self):
        return f"{self.member} - {self.date}"

    class Meta:
        verbose_name = 'Food Plan'
        verbose_name_plural = 'Food Plans'
        ordering = ['-date']


class FoodLog(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    food_plan = models.ForeignKey(FoodPlan, on_delete=models.CASCADE, null=True, blank=True)
    food_name = models.CharField(max_length=100)
    calories = models.FloatField()
    protein = models.FloatField()
    fat = models.FloatField()
    carbs = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.member} - {self.food_name} on {self.date}"

    class Meta:
        verbose_name = 'Food Log'
        verbose_name_plural = 'Food Logs'
        ordering = ['-date']


class Slider(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField()
    image = models.ImageField(upload_to='slider/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Slide'
        verbose_name_plural = 'Slides'


class FAQ(models.Model):
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.question[:50]  # Show first 50 chars

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

class Payment(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=20)  # e.g., 'Stripe', 'Cash'

    def __str__(self):
        return f"{self.member.user.username} - {self.amount}"
