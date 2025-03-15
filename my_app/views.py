from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Workout, Profile
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.forms import ModelForm


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


#static list of exercises

COMMON_EXERCISES = [
    'Running', 'Push-ups', 'Sit-ups', 'Squats', 'Cycling',
    'Jumping Jacks', 'Plank', 'Lunges', 'Burpees', 'Yoga',
    'Swimming', 'Weight Lifting', 'Pull-ups', 'Stretching', 'Rowing'
]





# Create your views here.
@login_required
def welcome(request):
    today = datetime.now().strftime("%B %d, %Y")  # e.g., "March 04, 2025"
    message = "Keep pushing forward—you've got this!"
    return render(request, 'my_app/welcome.html', {
        'username': request.user.username,
        'today': today,
        'message': message
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
    return render(request, 'my_app/analytics.html')

@login_required
def goals(request):
    return render(request, 'my_app/goals.html')


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