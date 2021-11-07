from os import name
from django.db import models
import os

def fp(instance, filename):
    ext = filename.split('.')[-1]
    name = str(filename).replace('-','_')
    return 'static/plantdataset/{}.{}'.format(name, ext)

def fa(instance, filename):
    ext = filename.split('.')[-1]
    name = str(filename).replace('-','_')
    return 'static/animaldataset/{}.{}'.format(name, ext)
# Create your models here.
class sampletb(models.Model):
    name = models.CharField(max_length=15,default="image")
    image = models.FileField(upload_to='static/media')

class indextbplant(models.Model):
    name = models.CharField(max_length=15,default="index")
    image = models.FileField(upload_to='static/dataset')

class indextbanimal(models.Model):
    name = models.CharField(max_length=15,default="index")
    image = models.FileField(upload_to='static/dataset')

# class imagetb(models.Model):
#     name = models.CharField(max_length=15,default="index")
#     image = models.FileField(upload_to='static/dataset',null=True)

class PlantTB(models.Model):
    image = models.FileField(upload_to=fp,null=True)

class AnimalTB(models.Model):
    image = models.FileField(upload_to=fa,null=True)
    
# import json
# class dataModel(models.Model):
#     name = models.CharField(max_length=15,default="demo")
#     data = models.TextField()

#     def set_foo(self, x):
#         self.data = json.dumps(x)

#     def get_foo(self):
#         return json.loads(self.data)

