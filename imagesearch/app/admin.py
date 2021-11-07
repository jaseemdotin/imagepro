from django.contrib import admin
from .models import  sampletb,indextbplant,indextbanimal,PlantTB,AnimalTB

# Register your models here.

admin.site.register(sampletb)
# admin.site.register(imagetb)
admin.site.register(indextbanimal)
admin.site.register(indextbplant)
# admin.site.register(dataModel)
admin.site.register(PlantTB),
admin.site.register(AnimalTB)
