from django.contrib import admin

from .models import *
# Register your models here.

myModels = [Post, City] 

admin.site.register(myModels)