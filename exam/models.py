from django.db import models
from teacher.models import Teacher
from student.models import Student
from django.contrib.auth.models import User
import uuid

class Collage(models.Model):
    name=models.CharField(max_length=255,null=True)
    descr=models.TextField(null=True)
    def __str__(self):
        return self.name

class Departiment(models.Model):
    name=models.CharField(max_length=255,null=True)
    colage_name=models.CharField(max_length=255,null=True)
    adby=models.IntegerField(null=True)
    cl_name=models.ForeignKey(Collage,on_delete=models.CASCADE,null=True)
    head=models.IntegerField(null=True)
    def __str__(self):
        return self.name

class Course(models.Model):
   course_name = models.CharField(max_length=50)
   question_number = models.PositiveIntegerField()
   total_marks = models.PositiveIntegerField()
   dep=models.IntegerField(null=True)
   c_code=models.CharField(max_length=255,null=True)
   year=models.IntegerField(null=True)
   sem=models.IntegerField(null=True)
   dp=models.ForeignKey(Departiment,on_delete=models.CASCADE,null=True)
   pre=models.IntegerField(default=0)
   def __str__(self):
        return self.course_name

class Question(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    marks=models.PositiveIntegerField()
    question=models.CharField(max_length=600)
    option1=models.CharField(max_length=200)
    option2=models.CharField(max_length=200)
    option3=models.CharField(max_length=200)
    option4=models.CharField(max_length=200)
    cat=(('Option1','A'),('Option2','B'),('Option3','C'),('Option4','D'))
    answer=models.CharField(max_length=200,choices=cat)
    dep=models.IntegerField(null=True)
    adby=models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True)
    examid=models.IntegerField(null=True)
class Result(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    exam = models.ForeignKey(Course,on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)
    dep=models.IntegerField(null=True)
class Permision(models.Model):
      name=models.CharField(max_length=255,null=True)
      perm=models.CharField(max_length=255,null=True)


