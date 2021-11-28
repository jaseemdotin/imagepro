from django.contrib import admin
from .models import  sampletb,DSmodel,ImageTB

# Register your models here.

admin.site.register(sampletb)
# admin.site.register(imagetb)
admin.site.register(DSmodel)
# admin.site.register(dataModel)
admin.site.register(ImageTB)
