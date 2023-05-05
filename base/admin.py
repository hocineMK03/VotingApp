from django.contrib import admin
from .models import Polls_details,Choice_poll,User_choices
# Register your models here.

admin.site.register(Polls_details)
admin.site.register(Choice_poll)
admin.site.register(User_choices)