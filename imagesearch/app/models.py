from os import name
from django.db import models
import os

# Create your models here.
class sampletb(models.Model):
    name = models.CharField(max_length=15,default="image")
    image = models.FileField(upload_to='static/media')

class indextb(models.Model):
    name = models.CharField(max_length=15,default="index")
    image = models.FileField(upload_to='static/dataset')

class imagetb(models.Model):
    name = models.CharField(max_length=15,default="index")
    image = models.FileField(upload_to='static/dataset',null=True)
    
import json
class dataModel(models.Model):
    name = models.CharField(max_length=15,default="demo")
    data = models.TextField()

    def set_foo(self, x):
        self.data = json.dumps(x)

    def get_foo(self):
        return json.loads(self.data)

