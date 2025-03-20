from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.urls import reverse


from .models import Account, Travels, Messages, User, Trips
# Create your views here.
def home(request):
    formatted_time = timezone.now().strftime("%H:%M:%S.%f")
    context = {
        'current_time': formatted_time,
    }
    return render(request,  'travels/home.html', context)

def list(request):
    travels = Travels.objects.filter(status="available")
    context={
        'travels': travels,
    }
    return render(request, 'travels/list.html', context)


def create_trip(request, travel_id):

    if request.method == "POST" and request.user.is_authenticated:
        # Get the travel instance
        travel = get_object_or_404(Travels, id=travel_id)
        
        # Create a new trip
        trip = Trips.objects.create(
            travel=travel,
            traveler=request.user
        )
        
        # Update the status of the travel
        travel.status = "In Progress"
        travel.save()
        trip.save()
        
    return redirect(reverse('list'))  


def create_travel(request):

    if request.method == "POST" and request.user.is_authenticated:
        
        title=request.POST['title']
        desc=request.POST['desc']
        location = request.POST['location']
        date = request.POST.get('date', '')
        url=request.POST['url']

        if not title and not desc and not location and not date and not url:
            return render(request, 'travels/create_travel.html', context = {})
        
        if date=="":
         return render(request, 'travels/create_travel.html', context = {})
        


        travel=Travels(
            user=request.user,
            title = title,
            desc = desc,
            location = location,
            date = date,
            photo = url
        )
        travel.save()

        return redirect(reverse('list'))
    context = {}
    return render(request, 'travels/create_travel.html', context)