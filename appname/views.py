from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from decimal import Decimal
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import List_Of_Users, Bus, Booking,Feedback_Form
from django.contrib.auth import authenticate, login, logout,get_user_model

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        return render(request, 'home.html')
    
from django.shortcuts import render
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from .models import Bus

@login_required(login_url='login_page')
def findbus(request):
    context = {}
    if request.method == 'POST':
        source_r = request.POST.get('source')
        dest_r = request.POST.get('destination')
        date_r = request.POST.get('date')
        date_r = datetime.strptime(date_r,"%Y-%m-%d").date()
        year = date_r.strftime("%Y")
        month = date_r.strftime("%m")
        day = date_r.strftime("%d")
        bus_list = Bus.objects.filter(source=source_r, destination=dest_r, date__year=year, date__month=month, date__day=day)
        if bus_list:
            return render(request, 'lists.html', locals())
        else:
            context['data'] = request.POST
            context["error"] = "No available Bus Schedule for entered Route and Date"
            return render(request, 'findbus.html', context)
    else:
        return render(request, 'findbus.html')
    


from django.shortcuts import render, redirect
from django.contrib.auth.models import User

def registration_page(request):
    if request.method == 'POST':
        full_name = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            error_message = "Passwords do not match. Please try again."
            return render(request, 'registration_page.html', {'error_message': error_message})

        # Additional form validation can be added here

        try:
            new_user = User.objects.create_user(username=email, email=email, password=password)
            # You can add additional fields like full name to the user object if needed
            new_user.full_name = full_name
            new_user.save()
            
            # Redirect to a success page or login page after successful registration
            return redirect('login_page')  # Change 'login' to the name of your login URL pattern
        except Exception as e:
            error_message = "An error occurred during registration. Please try again."
            return render(request, 'registration_page.html', {'error_message': error_message})
    
    return render(request, 'registration_page.html')

from django.contrib.auth import authenticate, login

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
import logging

logger = logging.getLogger(__name__)

def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                logger.info("User authenticated successfully")
                login(request, user)
                # Redirect to a specific page after successful login
                return redirect('home.html')  # Change 'home' to your desired URL name
            else:
                error_message = "Invalid username or password. Please try again."
                logger.error("Authentication failed for user: %s", username)
                return render(request, 'login_page.html', {'error_message': error_message})
        else:
            error_message = "Invalid form data. Please check your input."
            logger.error("Form validation failed for user input")
            return render(request, 'login_page.html', {'error_message': error_message})
    
    return render(request, 'login_page.html', {'form': AuthenticationForm()})
    
def success(request):
    context = {}
    context['user'] = request.user
    return render(request, 'success.html', context)

def logout_page(request):
    context = {}
    logout(request)
    context['error'] = "You have been logged out"
    return render(request, 'home.html', context)

    
def thank(request):
    return render(request,'thank.htmml')

# views.py
from django.shortcuts import render
from django.http import HttpResponse
from .models import Feedback_Form

def Feedback_Form1(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        feedback_text = request.POST.get('feedback')

        if not name or not email or not feedback_text:
            error_message = "Please fill in all the required fields."
            return render(request, 'Feedback_Form1.html', {'error_message': error_message})

        try:
            feedback = Feedback_Form(name=name, email=email, feedback=feedback_text)
            feedback.save()
            return HttpResponse("Thank you for your feedback!")  # Display a success message
        except Exception as e:
            error_message = "An error occurred while saving the feedback. Please try again."
            return render(request, 'Feedback_Form1.html', {'error_message': error_message})
    else:
        return render(request, 'Feedback_Form1.html')
    

@login_required(login_url='login_page')
def bookings(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('bus_id')
        seats_r = int(request.POST.get('no_seats'))
        bus = Bus.objects.get(id=id_r)
        if bus:
            if bus.remaining_seats > int(seats_r):
                name_r = bus.bus_name
                cost = int(seats_r) * bus.price
                source_r = bus.source
                dest_r = bus.destination
                nos_r = Decimal(bus.no_of_seats)
                price_r = bus.price
                date_r = bus.date
                time_r = bus.time
                username_r = request.user.username
                email_r = request.user.email
                userid_r = request.user.id
                rem_r = bus.remaining_seats - seats_r
                Bus.objects.filter(id=id_r).update(remaining_seats=rem_r)
                book = Booking.objects.create(name=username_r, email=email_r, userid=userid_r, bus_name=name_r,
                                           source=source_r, busid=id_r,
                                           dest=dest_r, price=price_r, nos=seats_r, date=date_r, time=time_r,
                                           status='BOOKED')
                print('------------book id-----------', book.id)
                # book.save()
                return render(request, 'bookings.html', locals())
            else:
                context["error"] = "Sorry select fewer number of seats"
                return render(request, 'findbus.html', context)

    else:
        return render(request, 'findbus.html')
    
@login_required(login_url='signin')
def cancellings(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('bus_id')
        #seats_r = int(request.POST.get('no_seats'))

        try:
            book = Booking.objects.get(id=id_r)
            bus = Bus.objects.get(id=book.busid)
            rem_r = bus.remaining_seats + book.nos
            Bus.objects.filter(id=book.busid).update(remaining_seats=rem_r)
            #nos_r = book.nos - seats_r
            Booking.objects.filter(id=id_r).update(status='CANCELLED')
            Booking.objects.filter(id=id_r).update(nos=0)
            messages.success(request, "Booked Bus has been cancelled successfully.")
            return redirect(orders)
        except Booking.DoesNotExist:
            context["error"] = "Sorry You have not booked that bus"
            return render(request, 'error.html', context)
    else:
        return render(request, 'findbus.html')
    
@login_required(login_url='login_page')
def orders(request,new={}):
    context = {}
    id_r = request.user.id
    book_list = Booking.objects.filter(userid=id_r)
    if book_list:
        return render(request, 'booklist.html', locals())
    else:
        context["error"] = "Sorry no buses booked"
        return render(request, 'findbus.html', context)
