from django.contrib import admin
from .models import Plans, Exercise, Workout, UserProfile, Messages
# Register your models here.

admin.site.register(Plans)
admin.site.register(Exercise)
admin.site.register(Workout)
admin.site.register(UserProfile)
admin.site.register(Messages)