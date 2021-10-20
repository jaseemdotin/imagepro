from django.contrib import admin
from .models import dataModel, sampletb,imagetb,indextb

# Register your models here.

admin.site.register(sampletb)
admin.site.register(imagetb)
admin.site.register(indextb)
admin.site.register(dataModel)
