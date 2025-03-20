from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.urls import reverse
from datetime import datetime
from travels.models import Travels, User, Messages, Trips, Account
from django.contrib.auth.decorators import login_required

from django.contrib.auth import login, authenticate

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

from django.db.models import Q

# Create your views here.
@login_required
def dashboard(request):
    user=request.user
    my_travels = Travels.objects.filter(user=request.user)
    my_messages = Messages.objects.filter(reciever_id=request.user) | Messages.objects.filter(sender_id=request.user)
    my_messages = my_messages.order_by('sent_at')

    completed_travels=Trips.objects.filter(travel__user=user, travel__status="Completed")
    ongoing_travels=Trips.objects.filter(travel__user=user, travel__status="In Progress")
    available_travels=Travels.objects.filter(user=user, status="available")

    ongoing_trip = Trips.objects.filter(traveler=user, travel__status="In Progress")
    completed_trip = Trips.objects.filter(traveler=user, travel__status="Completed")
   
    context={
        'my_travels': my_travels,   
        'my_messages': my_messages,
        'completed_travels': completed_travels,
        'ongoing_travels': ongoing_travels,
        'available_travels': available_travels,
        'ongoing_trip': ongoing_trip,
        'completed_trip': completed_trip,
    }
    return render(request, 'accounts/dashboard.html', context)

def profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    available_travels=Travels.objects.filter(user=user, status="available")
    
    completed_travels=Trips.objects.filter(travel__user=user, travel__status="Completed")
    ongoing_travels=Trips.objects.filter(travel__user=user, travel__status="In Progress")

    ongoing_trip = Trips.objects.filter(traveler=user, travel__status="In Progress")
    completed_trip = Trips.objects.filter(traveler=user, travel__status="Completed")
    context={
        'profile_user': user,
        'completed_travels': completed_travels,
        'ongoing_travels': ongoing_travels,
        'available_travels': available_travels,
        'ongoing_trip': ongoing_trip,
        'completed_trip': completed_trip,
    }
    return render(request, 'accounts/profile.html',context)

@login_required
def rate(request):
    
    if request.method == "POST":
        id=request.POST['trip_id']
        trip = get_object_or_404(Trips, pk=id, traveler=request.user)
        rating=int(request.POST['rate'])
        trip.rating=rating
        trip.save()
        
    return redirect(reverse('accounts:dashboard'))

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("accounts:finishup")
    template_name = "registration/signup.html"

def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save the user
            user = form.save()

            # Authenticate the user
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Log the user in
                login(request, user)
                return redirect('accounts:finishup')  # Replace 'home' with your desired redirect URL

    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form})

def finishup(request):

    if request.method == "POST":
        
        user=request.user
       
        name = request.POST['pn']
        email = request.POST['email']
        request.user.email=email
        
        is_organization = request.POST.get('org') == 'on'

        account=Account(
            user=user,
            name=name,
            organization=is_organization
            
        )
        account.save()
        request.user.save()

        return redirect(reverse('home'))
    context = {}
    return render(request, 'accounts/finishup.html', context)

@login_required
def available(request, travel_id):
    travel=get_object_or_404(Travels, pk=travel_id)
    users=User.objects.all()
    if request.method == "POST":
        
        
        title = request.POST.get('title', '')
        desc = request.POST.get('desc', '')
        location = request.POST.get('location', '')
        date = request.POST.get('date', '')
        url = request.POST.get('url', '')
        status = request.POST.get('status', '')
        traveler1=int(request.POST['traveler'])
        if not traveler1==0:
            traveler=get_object_or_404(User, pk=traveler1)


        
        
        if not title or not desc or not location or not date or not url or not status and traveler1=="0":
            context = {
            'travel': travel,
            'users': users,
             }
            return render(request, 'accounts/edit.html', context)

        if status == 'available':
            
           
            travel.title = title
            travel.desc = desc
            travel.location = location
            travel.date = date
            travel.photo = url
            travel.status=status
            
            travel.save()

        else:

            if traveler1==0:
                context = {
                    'travel': travel,
                    'users': users,
                    }
                return render(request, 'accounts/edit.html', context)
            travel.title = title
            travel.desc = desc
            travel.location = location
            travel.date = date
            travel.photo = url
            travel.status=status
            
            travel.save()
            trip=Trips(
                travel=travel,
                traveler=traveler
            )
            trip.save()
            
        return redirect(reverse('accounts:dashboard'))
    
    
    context = {
        'travel': travel,
        'users': users,
    }
    return render(request, 'accounts/edit.html', context)


@login_required
def edit2(request, trip_id):
    trip=get_object_or_404(Trips, pk=trip_id)
    users=User.objects.all()

    if request.method == "POST":
        
        
        title = request.POST.get('title', '')
        desc = request.POST.get('desc', '')
        location = request.POST.get('location', '')
        date = request.POST.get('date', '')
        url = request.POST.get('url', '')
        status = request.POST.get('status', '')
        traveler1=int(request.POST['traveler'])
        if not traveler1==0:
            traveler=get_object_or_404(User, pk=traveler1)
    

        
        
        if not title or not desc or not location or not date or not url or not status and traveler1=="0":
            context = {
            'trip': trip,
            'users': users,
             }
            return render(request, 'accounts/edit2.html', context)

        if status == 'available':
            trip.travel.title = title
            trip.travel.desc = desc
            trip.travel.location = location
            trip.travel.date = date
            trip.travel.photo = url
            trip.travel.status=status
            
            trip.travel.save()
            trip.delete()
            

        else:

            if traveler1==0:
                context = {
                    'trip': trip,
                    'users': users,
                    }
                return render(request, 'accounts/edit2.html', context)
            trip.travel.title = title
            trip.travel.desc = desc
            trip.travel.location = location
            trip.travel.date = date
            trip.travel.photo = url
            trip.travel.status=status

            trip.travel.save()
            trip.traveler=traveler
            trip.save()
            
        return redirect(reverse('accounts:dashboard'))
    
    
    context = {
        'trip': trip,
        'users': users,
    }
    return render(request, 'accounts/edit2.html', context)


@login_required
def delete(request, travel_id):

    travel=get_object_or_404(Travels, pk=travel_id)
    travel.delete()

    return redirect(reverse('accounts:dashboard'))


@login_required
def messages(request):


    my_messages = Messages.objects.filter(reciever_id=request.user)
    mess=Messages.objects.filter(sender_id=request.user)
    
    
    seen_senders = set()
    unique_messages = []

    uni_messages = []

    for message in my_messages:
        if message.sender_id.id not in seen_senders:
            unique_messages.append(message)
            seen_senders.add(message.sender_id.id)

    for message2 in mess:
        if message2.reciever_id.id not in seen_senders:
            uni_messages.append(message2)
            seen_senders.add(message2.reciever_id.id)

    context = {
        'my_messages': unique_messages,
        'messages2': uni_messages,
    }
    return render(request, 'accounts/messages.html', context)

@login_required
def chat(request, user_id):
    
    user1 = get_object_or_404(User, pk=user_id)

    #Da imam lijevo all messages listu
    my_messages = Messages.objects.filter(reciever_id=request.user)
    mess=Messages.objects.filter(sender_id=request.user)
    
    
    seen_senders = set()
    unique_messages = []

    uni_messages = []

    for message in my_messages:
        if message.sender_id.id not in seen_senders:
            unique_messages.append(message)
            seen_senders.add(message.sender_id.id)

    for message2 in mess:
        if message2.reciever_id.id not in seen_senders:
            uni_messages.append(message2)
            seen_senders.add(message2.reciever_id.id)

    
    
    #Message box
    chat = Messages.objects.filter(
        Q(sender_id=request.user, reciever_id=user1) |
        Q(sender_id=user1, reciever_id=request.user)
    ).order_by('sent_at')

    context = {
        'my_messages': unique_messages,
        'messages2': uni_messages,
        'chat': chat,
        'user1': user1,
        'user_id': user_id
    }
    return render(request, 'accounts/chat.html', context)


@login_required
def create_message(request, user_id):
    
    reciever=get_object_or_404(User, id=user_id)
    sender=request.user
    text=request.POST['message']


    if not text:
        return redirect(reverse('accounts:chat', args=[user_id,]))

    message=Messages(
        sender_id=sender,
        reciever_id=reciever,
        text=text
    )
    message.save()
    return redirect(reverse('accounts:chat', args=[user_id,]))