from os import name
from django.db import models
import os

def DSfolder(instance, filename):
    ext = filename.split('.')[-1]
    name = str(filename).replace('-','_').split('.')[0]
    return 'static/DSfolder/{}.{}'.format(name, ext)

def bombardierDS(instance, filename):
    ext = filename.split('.')[-1]
    name = str(filename).replace('-','_').split('.')[0]
    return 'static/bombardierDS/{}.{}'.format(name, ext)
# Create your models here.
class sampletb(models.Model):
    name = models.CharField(max_length=15,default="image")
    image = models.FileField(upload_to='static/media')

class DSmodel(models.Model):
    name = models.CharField(max_length=15,default="index")
    image = models.FileField(upload_to='static/dataset')

class ImageTB(models.Model):
    image = models.FileField(upload_to='static/DSfolder',null=True)


