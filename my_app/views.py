from django.shortcuts import render
from django.http import JsonResponse


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