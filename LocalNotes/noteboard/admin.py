from django.contrib import admin

from .models import *
# Register your models here.

# myModels = [Post, City, User] 

# admin.site.register(myModels)

admin.site.register(Post)
admin.site.register(City)
