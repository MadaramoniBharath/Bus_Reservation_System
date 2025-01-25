from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name="home"),
    path('home.html',views.home,name="home"),
    path('login_page.html',views.login_page,name="login_page"),
    path('registration_page.html',views.registration_page,name="registration_page"),
    path('findbus.html',views.findbus,name="findbus"),
    path('success.html', views.success, name="success"),
    path('logout_page.html',views.logout_page,name="logout_page"),
    path('orders.html',views.orders,name="orders"),
    path('thank.html',views.thank,name="thank"),
    path('Feedback_Form1.html',views.Feedback_Form1,name="Feedback_Form1"),
    path('logout_page.html',views.logout_page,name="logout_page"),
    path('bookings.html',views.bookings,name="bookings"),
    path('cancellings', views.cancellings, name="cancellings"),


    
    
    
]