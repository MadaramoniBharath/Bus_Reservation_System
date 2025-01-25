from django.contrib import admin
from .models import Bus,List_Of_Users,Booking,Feedback_Form

# Register your models here.
admin.site.register(Bus)
admin.site.register(List_Of_Users)
admin.site.register(Booking)
admin.site.register(Feedback_Form)