from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Workout
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required



# Create your views here.
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