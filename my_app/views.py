from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Workout, Profile, Goal
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.forms import ModelForm
from django.db import models


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'height', 'weight', 'birthday', 'gender']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['birthday'].required = False


class WorkoutForm(ModelForm):
    class Meta:
        model = Workout
        fields = ['exercise', 'duration']


class GoalForm(ModelForm):  # Should be here, globally defined
    class Meta:
        model = Goal
        fields = ['description', 'target_minutes', 'deadline']



#static list of exercises

COMMON_EXERCISES = [
    'Running', 'Push-ups', 'Sit-ups', 'Squats', 'Cycling',
    'Jumping Jacks', 'Plank', 'Lunges', 'Burpees', 'Yoga',
    'Swimming', 'Weight Lifting', 'Pull-ups', 'Stretching', 'Rowing'
]





# Create your views here.

@login_required
def welcome(request):
    today = datetime.now().strftime("%B %d, %Y")  # e.g., "April 9, 2025"
    return render(request, 'my_app/welcome.html', {
        'username': request.user.username,
        'today': today
    })






def default_greet(request):
    return render(request, "greet.html")


def greet(request): 

    name = request.GET.get('name', '').strip()

    if name: 
        greeting = f"Hello {name}!"
    else:
        greeting = "Hello stranger!"

    return JsonResponse({"greeting": greeting})




@login_required
def dashboard(request):
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.user = request.user  # Tie to logged-in user
            workout.save()
            return redirect('dashboard')
    else:
        form = WorkoutForm()
    workouts = Workout.objects.filter(user=request.user).order_by('-date')[:5]  # Last 5 workouts
    return render(request, 'my_app/dashboard.html', {'form': form, 'workouts': workouts})


@login_required
def analytics(request):
    today = datetime.now().date()
    
    # Summary stats
    workouts = Workout.objects.filter(user=request.user)
    total_minutes = sum(w.duration for w in workouts)
    workout_count = workouts.count()
    avg_duration = total_minutes / workout_count if workout_count > 0 else 0
    
    # Daily workout data (last 7 days)
    week_ago = today - timedelta(days=6)
    daily_data = []
    for i in range(7):
        day = week_ago + timedelta(days=i)
        day_workouts = workouts.filter(date=day)
        daily_data.append({
            'date': day.strftime('%Y-%m-%d'),
            'minutes': sum(w.duration for w in day_workouts)
        })
    
    # Weekly trends (last 4 weeks)
    four_weeks_ago = today - timedelta(days=27)
    weekly_data = []
    for i in range(4):
        week_start = four_weeks_ago + timedelta(days=i*7)
        week_end = week_start + timedelta(days=6)
        week_workouts = workouts.filter(date__gte=week_start, date__lte=week_end)
        weekly_data.append({
            'week': f"Week {i+1}",
            'minutes': sum(w.duration for w in week_workouts)
        })
    
    # Top exercises
    exercise_counts = workouts.values('exercise').annotate(count=models.Count('exercise')).order_by('-count')[:3]
    
    # Active goals snapshot
    active_goals = Goal.objects.filter(user=request.user, deadline__gte=today)
    for goal in active_goals:
        goal_workouts = workouts.filter(date__gte=goal.start_date, date__lte=goal.deadline)
        goal.progress = sum(w.duration for w in goal_workouts)
    
    return render(request, 'my_app/analytics.html', {
        'total_minutes': total_minutes,
        'workout_count': workout_count,
        'avg_duration': avg_duration,
        'daily_data': daily_data,
        'weekly_data': weekly_data,
        'top_exercises': exercise_counts,
        'active_goals': active_goals
    })




@login_required
def goals(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect('goals')
    else:
        form = GoalForm()
    
    # Get active goals (not past deadline)
    today = datetime.now().date()
    active_goals = Goal.objects.filter(user=request.user, deadline__gte=today)
    
    # Calculate progress and percentage for each goal
    for goal in active_goals:
        workouts = Workout.objects.filter(
            user=request.user, date__gte=goal.start_date, date__lte=goal.deadline
        )
        goal.progress = sum(workout.duration for workout in workouts)
        # Calculate percentage (0-100), cap at 100%
        goal.progress_percentage = min(100, (goal.progress / goal.target_minutes * 100) if goal.target_minutes > 0 else 0)
    
    # Get profile for extra context
    profile = Profile.objects.get_or_create(user=request.user)[0]
    
    return render(request, 'my_app/goals.html', {
        'form': form,
        'goals': active_goals,
        'profile': profile
    })












def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Creates the user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)  # Logs them in
            return redirect('dashboard')  # Redirects to dashboard
    else:
        form = UserCreationForm()
    return render(request, 'my_app/signup.html', {'form': form})



@login_required
def profile(request):
    # Get or create the user's profile
    profile, created = Profile.objects.get_or_create(user=request.user)
    print(f"Profile exists: {not created}, Data: {profile.first_name}, {profile.height}")  # Debug
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        print("POST request received")  # Debug
        if form.is_valid():
            print("Form is valid, saving:", form.cleaned_data)  # Debug
            form.save()
            return redirect('profile')
        else:
            print("Form errors:", form.errors)  # Debug
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'my_app/profile.html', {'form': form})


#handle ajax request
@login_required
def search_exercises(request):
    query = request.GET.get('q', '')
    print("Query:", query)  # Debug what’s being typed
    # Get user's logged exercises
    user_exercises = Workout.objects.filter(
        user=request.user, exercise__icontains=query
    ).values('exercise').distinct()
    user_exercise_list = [exercise['exercise'] for exercise in user_exercises]
    print("User exercises:", user_exercise_list)  # Debug
    
    # Filter static exercises
    static_exercises = [ex for ex in COMMON_EXERCISES if query.lower() in ex.lower()]
    print("Static exercises:", static_exercises)  # Debug
    
    # Combine and remove duplicates, limit to 5
    combined_exercises = list(dict.fromkeys(user_exercise_list + static_exercises))[:5]
    print("Combined exercises:", combined_exercises)  # Debug
    
    return JsonResponse({'exercises': combined_exercises})   