from django.db import models
from django.contrib.auth.models import User
cat=(('1','Computer Science'),('3','Natural Resource Management'),('4','Agri-business and value chain management')
     ,('5','Animal Scince'),('6','Plant Science'),('7','Horticulture'),('8','Veterinary Science'),(' 9',' Chemistry')
    ,('10','Biology'),('11','Mathematics'),('12','Statics'),('13','Agricultural Economics'),('14','Physics'),('15','Accounting and finance'),('16','management')
    ,('17','Economics'),('18','Veterinary Medicine'),('19','Turism and Hotel Management'),('20','psychology'),('19','Turism and Hotel Management'),('20','psychology')
    ,('21','Geograpy'),('22','Civic'),('23','Social Anthrophology'),('24','History And Heritage management'),('25',' English Languege'),('26','Law'),('27','Midwifery'),('20','Nursing')
    ,('20','Public Health'))
class Teacher(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/Teacher/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    status= models.BooleanField(default=False)
    salary=models.PositiveIntegerField(null=True)
    depart=models.CharField(max_length=255,choices=cat,null=True)
    #dep=models.CharField(max_length=255,choices=cat)
    course=models.CharField(max_length=255,null=True)
    type=models.IntegerField(default=0)
    
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name
class Schedule(models.Model):
     exam=models.IntegerField(null=True)
     time=models.TimeField(null=True)
     tim=models.CharField(null=True,max_length=100)
     dat=models.DateField(null=True)
     dur=models.IntegerField(null=True)
     adby=models.IntegerField(null=True)
       