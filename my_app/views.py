from django.shortcuts import render
from django.http import JsonResponse
from .models import Workout


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





def dashboard(request):
    workouts = Workout.objects.all()[:5]  # Show last 5 workouts
    return render(request, 'my_app/dashboard.html', {'workouts': workouts})

def analytics(request):
    return render(request, 'my_app/analytics.html')

def goals(request):
    return render(request, 'my_app/goals.html')