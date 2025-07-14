from django.shortcuts import render,redirect,get_object_or_404
from . import models
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import  JsonResponse
import requests
from .forms import WorkoutPlanForm, FoodPlanForm, FoodLogForm, ExerciseLogForm, RegisterForm,LoginForm,MemberForm
from django.contrib import messages
from django.contrib.auth import login, logout
from datetime import timedelta, date
from django.utils.timezone import now


def home_view(request):
    questions = models.FAQ.objects.all()
    slides = models.Slider.objects.all()

    food_plans = []
    workouts = []

    if request.user.is_authenticated and hasattr(request.user, 'member'):
        member = request.user.member
        food_plans = models.FoodPlan.objects.filter(member=member, date=date.today())
        workouts = models.WorkoutPlan.objects.filter(member=member, date=date.today())

    context = {
        'questions': questions,
        'slides': slides,
        'food_plans': food_plans,
        'workouts': workouts,
    }
    return render(request, 'blog_app/index.html', context=context)

def profile_view(request):
    return render(request, 'blog_app/profile.html')

def workouts_view(request):
    if not hasattr(request.user, 'member'):
        return redirect('profile')
    workouts = models.WorkoutPlan.objects.filter(member=request.user.member)
    context = {
        'workouts': workouts
    }
    return render(request, 'blog_app/workouts.html',context=context)

def exercise_detail_view(request,workout_id):
    workout = get_object_or_404(models.WorkoutPlan, id=workout_id, member=request.user.member)
    exercises = models.ExerciseLog.objects.filter(workout=workout_id)
    context = {
        'exercises': exercises,
        'workout': workout,
    }
    return render(request, 'blog_app/exercises.html', context=context)

@login_required
def create_workout_plan_view(request):
    if request.method == 'POST':
        form = WorkoutPlanForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.member = request.user.member
            workout.save()
            return redirect('workouts')
    else:
        form = WorkoutPlanForm()

    return render(request, 'blog_app/create_workout_plan.html', {'form': form})

@login_required
def create_exercise_view(request, workout_id):
    workout = get_object_or_404(models.WorkoutPlan, id=workout_id)
    if request.method == 'POST':
        form = ExerciseLogForm(request.POST)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.member = workout.member
            exercise.workout = workout
            exercise.save()
            return redirect('workout_detail', workout_id=workout.id)
    else:
        form = ExerciseLogForm()
    return render(request, 'blog_app/create_exercise.html', {'form': form, 'workout': workout})

def suggested_exercises_view(request):
    muscles = ['chest', 'back', 'biceps', 'triceps', 'legs', 'shoulders', 'abs']
    return render(request, 'blog_app/suggested_exercises.html', {'muscles': muscles})

def fetch_suggestions(request):
    muscle = request.GET.get('muscle')
    type_ = request.GET.get('type')
    difficulty = request.GET.get('difficulty')

    params = {}
    if muscle: params['muscle'] = muscle
    if type_: params['type'] = type_
    if difficulty: params['difficulty'] = difficulty

    headers = {'X-Api-Key': settings.API_NINJAS_KEY}
    try:
        response = requests.get('https://api.api-ninjas.com/v1/exercises', headers=headers, params=params)
        response.raise_for_status()
        return JsonResponse(response.json(), safe=False)
    except requests.RequestException as e:
        print("API error:", e)
        return JsonResponse({'error': 'Failed to fetch exercises.'}, status=500)

def attendance_view(request):
    attendances = models.Attendance.objects.filter(member=request.user.member).order_by('-date')
    return render(request, 'blog_app/attendance.html', {'attendances': attendances})

@login_required
def check_in_view(request):
    member = request.user.member
    today = now().date()

    attendance, created = models.Attendance.objects.get_or_create(
        member=member,
        date=today,
    )

    if not attendance.checked_in:
        attendance.checked_in = True
        attendance.check_in_time = now().time()
        attendance.save()

    return redirect('attendance')


@login_required
def check_out_view(request):
    member = request.user.member
    today = now().date()

    try:
        attendance = models.Attendance.objects.get(member=member, date=today)
        if attendance.checked_in and not attendance.checked_out:
            attendance.checked_out = True
            attendance.check_out_time = now().time()
            attendance.save()
    except models.Attendance.DoesNotExist:
        pass

    return redirect('attendance')

def foodlog_view(request):
    if not hasattr(request.user, 'member'):
        return redirect('profile')
    food_plans = models.FoodPlan.objects.filter(member=request.user.member)
    context = {
        'food_plans': food_plans
    }
    return render(request, 'blog_app/foodlog.html',context=context)

def food_detail_view(request,foodlog_id):
    food_plan = get_object_or_404(models.FoodPlan, id=foodlog_id, member=request.user.member)
    foods = models.FoodLog.objects.filter(food_plan=food_plan)
    context = {
        'foods': foods,
        'food_plan': food_plan,
    }
    return render(request, 'blog_app/food_detail.html', context=context)

@login_required
def create_food_plan_view(request):
    if request.method == 'POST':
        form = FoodPlanForm(request.POST)
        if form.is_valid():
            food_plan = form.save(commit=False)
            food_plan.member = request.user.member
            food_plan.save()
            return redirect('foodlog')
    else:
        form = FoodPlanForm()
    return render(request, 'blog_app/create_food_plan.html', {'form': form})

@login_required
def create_food(request, food_plan_id):
    food_plan = get_object_or_404(models.FoodPlan, id=food_plan_id)
    if request.method == 'POST':
        form = FoodLogForm(request.POST)
        if form.is_valid():
            food_log = form.save(commit=False)
            food_log.member = food_plan.member
            food_log.food_plan = food_plan
            food_log.save()
            return redirect('foodlog_detail', foodlog_id=food_plan.id)
    else:
        form = FoodLogForm()
    return render(request, 'blog_app/create_food.html', {'form': form, 'food_plan': food_plan})

from django.db.models import Sum, Avg
from django.utils.timezone import now, timedelta
def charts_view(request):
    member = request.user.member

    # Last 7 days
    today = now().date()
    week_ago = today - timedelta(days=6)

    workouts = models.ExerciseLog.objects.filter(member=member, workout__date__range=[week_ago, today])
    food_logs = models.FoodLog.objects.filter(member=member, date__range=[week_ago, today])

    daily_workout_data = workouts.values('workout__date').annotate(total_duration=Sum('duration_minutes'))
    dates = [entry['workout__date'].strftime('%a') for entry in daily_workout_data]
    durations = [entry['total_duration'] for entry in daily_workout_data]

    macros = food_logs.aggregate(
        protein=Sum('protein'), fat=Sum('fat'), carbs=Sum('carbs')
    )

    context = {
        'dates': dates,
        'durations': durations,
        'macros': macros
    }
    return render(request, 'blog_app/charts.html', context)

def contacts_view(request):
    return render(request, 'blog_app/contacts.html')

def faq_view(request):
    questions = models.FAQ.objects.all()
    context = {
        'questions': questions
    }
    return render(request, 'blog_app/faq.html', context)

def render_register_page(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Registration passed successfully')
            return redirect('login')
    else:
        form = RegisterForm()

    context = {
        'form': form
    }
    return render(request, 'blog_app/register.html', context=context)


def render_login_page(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                messages.success(request, 'Вы успешно вошли в аккаунт')
                return redirect('home')
            else:
                messages.error(request, 'Пользователь не найден')
        else:
            messages.error(request, 'Неправильный логин или пароль')
    else:
        form = LoginForm()

    context = {
        'form': form
    }
    return render(request, 'blog_app/login.html', context)


@login_required
def register_membership(request):
    if hasattr(request.user, 'member'):
        return redirect('profile')  # Already subscribed

    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.user = request.user
            member.is_active = True
            member.subscription_end = date.today() + timedelta(days=30)
            member.save()
            return redirect('profile')
    else:
        form = MemberForm()

    return render(request, 'blog_app/register_membership.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')