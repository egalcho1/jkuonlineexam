import datetime
from time import time

from django.db import models

from django.contrib.auth.models import User



types = [('employee','employee'),('visitor','visitor')]
class Profile(models.Model):
    first_name = models.CharField(max_length=70,null=True)
    last_name = models.CharField(max_length=70,null=True)
    date = models.DateField(null=True)
    phone = models.BigIntegerField(null=True)
    email = models.EmailField(null=True)
    ranking = models.IntegerField(null=True)
    profession = models.CharField(max_length=200,null=True)
    status = models.CharField(choices=types,max_length=20,null=True,blank=False,default='employee')
    present = models.BooleanField(default=False)
    image = models.ImageField(null=True)
    updated = models.DateTimeField(auto_now=True)
    shift = models.TimeField(null=True)
    username=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    fname=models.CharField(max_length=255,null=True,default="fn")
    lname=models.CharField(max_length=255,null=True,default="ln")
    gender=models.CharField(max_length=255,null=True)
    age=models.DateField(null=True)
    
    
    salary=models.IntegerField(null=True)
    exp=models.IntegerField(null=True)
    role=models.CharField(max_length=255,null=True)
    gfrom=models.CharField(max_length=255,null=True)
    gyear=models.DateField(null=True)
    bimage=models.ImageField(upload_to="image",null=True)
    certicate=models.ImageField(upload_to="certificate",null=True)
    valid=models.BooleanField(default=True)
    bcmgpa=models.IntegerField(null=True)
    bach=models.DateField(null=True)
    msc=models.DateField(null=True)
    phd=models.DateField(null=True)
    mimage=models.ImageField(upload_to="certificate",null=True)
    mvalid=models.BooleanField(default=True)
    pimage=models.ImageField(upload_to="certificate",null=True)
    pvalid=models.BooleanField(default=True)
    mcmgpa=models.IntegerField(null=True)
    pcmgpa=models.IntegerField(null=True)
    dt=models.DateField(auto_now=True)
    regby=models.BigIntegerField(null=True)
    type=models.CharField(max_length=255,null=True)
    adby=models.CharField(max_length=255,null=True)
    bonus=models.IntegerField(null=True)
    #adby=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.first_name +' '+self.last_name

    def __str__(self):
       
        return self.first_name +' '+self.last_name 


class LastFace(models.Model):
    last_face = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    username=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    user=models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        return self.last_face

