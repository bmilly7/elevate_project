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
    workouts = Workout.objects.all()[:5]  # Show last 5 workouts
    return render(request, 'my_app/dashboard.html', {'workouts': workouts})

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