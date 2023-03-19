from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.db.models import Q
from django.core.mail import send_mail
from teacher import models as TMODEL
from student import models as SMODEL
from teacher import forms as TFORM
from student import forms as SFORM
from django.contrib.auth.models import User
from exam.models import Course,Collage,Departiment,Permision
from .forms import Departiment as depart


def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  
    return render(request,'exam/index.html')


def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

def afterlogin_view(request):
    if is_student(request.user):      
        return redirect('student/student-dashboard')
                
    elif is_teacher(request.user):
        accountapproval=TMODEL.Teacher.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('teacher/teacher-dashboard')
        else:
            return render(request,'teacher/teacher_wait_for_approval.html')
    else:
        return redirect('exam:admin-dashboard')



def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    dict={
    'total_student':SMODEL.Student.objects.all().count(),
    'total_teacher':TMODEL.Teacher.objects.all().filter(status=True).count(),
    'total_course':models.Course.objects.all().count(),
    'total_question':models.Question.objects.all().count(),
    }
    return render(request,'exam/admin_dashboard.html',context=dict)

@login_required(login_url='adminlogin')
def admin_teacher_view(request):
    dict={
    'total_teacher':TMODEL.Teacher.objects.all().filter(status=True).count(),
    'pending_teacher':TMODEL.Teacher.objects.all().filter(status=False).count(),
    'salary':TMODEL.Teacher.objects.all().filter(status=True).aggregate(Sum('salary'))['salary__sum'],
    }
    return render(request,'exam/admin_teacher.html',context=dict)

@login_required(login_url='adminlogin')
def admin_view_teacher_view(request):
    teachers= TMODEL.Teacher.objects.all().filter(status=True)
    return render(request,'exam/admin_view_teacher.html',{'teachers':teachers})


@login_required(login_url='adminlogin')
def update_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=TMODEL.User.objects.get(id=teacher.user_id)
    userForm=TFORM.TeacherUserForm(instance=user)
    teacherForm=TFORM.TeacherForm(request.FILES,instance=teacher)
    mydict={'userForm':userForm,'teacherForm':teacherForm}
    if request.method=='POST':
        userForm=TFORM.TeacherUserForm(request.POST,instance=user)
        teacherForm=TFORM.TeacherForm(request.POST,request.FILES,instance=teacher)
        if userForm.is_valid() and teacherForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            teacherForm.save()
            return redirect('admin-view-teacher')
    return render(request,'exam/update_teacher.html',context=mydict)



@login_required(login_url='adminlogin')
def delete_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return HttpResponseRedirect('/admin-view-teacher')




@login_required(login_url='adminlogin')
def admin_view_pending_teacher_view(request):
    teachers= TMODEL.Teacher.objects.all().filter(status=False)
    return render(request,'exam/admin_view_pending_teacher.html',{'teachers':teachers})


@login_required(login_url='adminlogin')
def approve_teacher_view(request,pk):
    teacherSalary=forms.TeacherSalaryForm()
    if request.method=='POST':
        teacherSalary=forms.TeacherSalaryForm(request.POST)
        if teacherSalary.is_valid():
            crs=request.POST.get('course',False)
            dep=request.POST.get('dep',False)
            teacher=TMODEL.Teacher.objects.get(id=pk)
            teacher.salary=teacherSalary.cleaned_data['salary']
            teacher.course=crs
            teacher.depart=dep
            teacher.status=True
            teacher.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-pending-teacher')
    depart=models.Departiment.objects.all()
    course=Course.objects.all()
    return render(request,'exam/salary_form.html',{'teacherSalary':teacherSalary,'course':course,'depart':depart})

@login_required(login_url='adminlogin')
def reject_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return HttpResponseRedirect('/admin-view-pending-teacher')

@login_required(login_url='adminlogin')
def admin_view_teacher_salary_view(request):
    teachers= TMODEL.Teacher.objects.all().filter(status=True)
    return render(request,'exam/admin_view_teacher_salary.html',{'teachers':teachers})




@login_required(login_url='adminlogin')
def admin_student_view(request):
    dict={
    'total_student':SMODEL.Student.objects.all().count(),
    }
    return render(request,'exam/admin_student.html',context=dict)

@login_required(login_url='adminlogin')
def admin_view_student_view(request):
    students= SMODEL.Student.objects.all()
    return render(request,'exam/admin_view_student.html',{'students':students})
def add_student_info(request,id):
    username=request.user.username
    
    dep=User.objects.get(username=username)
    
    #techer=TMODEL.Teacher.objects.get(user_id=dep.pk)
    student= SMODEL.Student.objects.filter(dep=id)
    userForm=SFORM.StudentUserForm()
    studentForm=SFORM.StudentForm()
    mydict={'userForm':userForm,'studentForm':studentForm,'students':student}
    if request.method=='POST':
        
        t_dep=User.objects.get(username=username)
        userForm=SFORM.StudentUserForm(request.POST)
        studentForm=SFORM.StudentForm(request.POST,request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            student=studentForm.save(commit=False)
            student.user=user
            student.regby=dep.id
            student.dep=id
            student.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
    
    return render(request,"exam/add_student_info.html",context=mydict)


@login_required(login_url='adminlogin')
def update_student_view(request,pk):
    student=SMODEL.Student.objects.get(id=pk)
    user=SMODEL.User.objects.get(id=student.user_id)
    userForm=SFORM.StudentUserForm(instance=user)
    studentForm=SFORM.StudentForm(request.FILES,instance=student)
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=SFORM.StudentUserForm(request.POST,instance=user)
        studentForm=SFORM.StudentForm(request.POST,request.FILES,instance=student)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            studentForm.save()
            username=request.user.username
    
            dep=User.objects.get(username=username)
            
            #techer=TMODEL.Teacher.objects.get(user_id=dep.pk)
            student= SMODEL.Student.objects.filter(dep=student.dep)
            userForm=SFORM.StudentUserForm()
            studentForm=SFORM.StudentForm()
            mydict={'students':student}
            return render(request,"exam/add_student_info.html",context=mydict)
    return render(request,'exam/update_student.html',context=mydict)



@login_required(login_url='adminlogin')
def delete_student_view(request,id):
    student=SMODEL.Student.objects.get(user_id=id)
    user=User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return redirect('exam:add_student')
    #return HttpResponseRedirect('exam:delete_student_view')


@login_required(login_url='adminlogin')
def admin_course_view(request,id):
    course=Course.objects.filter(dp_id=id)
    if request.method=="POST":
        course_name=request.POST.get('course',False)
        total_mark=request.POST.get('total_marks',False)
        sem=request.POST.get('sem',False)
        question=request.POST.get('question',False)
        code=request.POST.get('code',False)
        db=models.Departiment.objects.get(id=id)
        course=Course.objects.create(question_number=question,c_code=code,dep=db,course_name=course_name,total_marks=total_mark,sem=sem)
        course.save()
        course=Course.objects.filter(id=id)
        return render(request,'exam/admin_course.html',{'courses':course})
    return render(request,'exam/admin_course.html',{'courses':course})


@login_required(login_url='adminlogin')
def admin_add_course_view(request):
    courseForm=forms.CourseForm()
    if request.method=='POST':
        courseForm=forms.CourseForm(request.POST)
        if courseForm.is_valid():        
            courseForm.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-course')
    return render(request,'exam/admin_add_course.html',{'courseForm':courseForm})


@login_required(login_url='adminlogin')
def admin_view_course_view(request):
    courses = models.Course.objects.all()
    return render(request,'exam/admin_view_course.html',{'courses':courses})

@login_required(login_url='adminlogin')
def delete_course_view(request,pk):
    course=models.Course.objects.get(id=pk)
    course.delete()
    return HttpResponseRedirect('/admin-view-course')



@login_required(login_url='adminlogin')
def admin_question_view(request):
    return render(request,'exam/admin_question.html')


@login_required(login_url='adminlogin')
def admin_add_question_view(request,id):
    questions=models.Question.objects.all().filter(adby=request.user.id,course_id=id)
   
    
    

    if request.method=='POST':
        course=request.POST.get('course',False)
        question=request.POST.get('question',False)
        option1=request.POST.get('option1',False)
        option2=request.POST.get('option2',False)
        option3=request.POST.get('option3',False)
        option4=request.POST.get('option4',False)
        answer=request.POST.get('answer',False)
        mark=request.POST.get('mark',False)
        
        cv=Course.objects.get(id=id)
        
        t_dep=User.objects.get(id=request.user.id)
        qtn=models.Question(adby=t_dep,marks=mark,course=cv,question=question,option1=option1,option2=option2,option3=option3,option4=option4,answer=answer)
        qtn.save()
        print("form is invalid")
      
        return render(request,'exam/admin_add_question.html',{'questions':questions})
    return render(request,'exam/admin_add_question.html',{'questions':questions})


@login_required(login_url='adminlogin')
def admin_view_question_view(request):
    courses= models.Course.objects.all()
    return render(request,'exam/admin_view_question.html',{'courses':courses})

@login_required(login_url='adminlogin')
def view_question_view(request,pk):
    questions=models.Question.objects.all().filter(course_id=pk)
    return render(request,'exam/view_question.html',{'questions':questions})

@login_required(login_url='adminlogin')
def delete_question_view(request,pk):
    question=models.Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/admin-view-question')

@login_required(login_url='adminlogin')
def admin_view_student_marks_view(request):
    students= SMODEL.Student.objects.all()
    return render(request,'exam/admin_view_student_marks.html',{'students':students})

@login_required(login_url='adminlogin')
def admin_view_marks_view(request,pk):
    courses = models.Course.objects.all()
    response =  render(request,'exam/admin_view_marks.html',{'courses':courses})
    response.set_cookie('student_id',str(pk))
    return response

@login_required(login_url='adminlogin')
def admin_check_marks_view(request,pk):
    course = models.Course.objects.get(id=pk)
    student_id = request.COOKIES.get('student_id')
    student= SMODEL.Student.objects.get(id=student_id)

    results= models.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request,'exam/admin_check_marks.html',{'results':results})
    




def aboutus_view(request):
    return render(request,'exam/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'exam/contactussuccess.html')
    return render(request, 'exam/contactus.html', {'form':sub})
def register_depart(request,id):
    
    if request.method=='POST':
       depart_name=request.POST.get('depart',False)
       descr=request.POST.get('descr',False)
       colage=Collage.objects.get(id=id)
       dep_create=models.Departiment.objects.create(name=depart_name,adby=request.user.id,cl_name=colage)
       dep_create.save()
       courses = models.Departiment.objects.filter(cl_name=id)
       return render(request,'exam/register_depart.html',{'id':id,'courses':courses})
    courses = models.Departiment.objects.filter(cl_name=id)
    return render(request,'exam/register_depart.html',{'id':id,'courses':courses})
def admin_view_departiment(request):
    if request.method=='POST':
       depart_name=request.POST.get('depart',False)
       cl=request.POST.get('cl',False)
       colage=Collage.objects.get(id=cl)
       dep_create=models.Departiment.objects.create(name=depart_name,adby=request.user.id,cl_name=colage)
       dep_create.save()
    courses = models.Departiment.objects.all()
    collage=models.Collage.objects.all()
    return render(request,'exam/admin_view_departiment.html',{'courses':courses,"colage":collage})
def head(request,id):
     tch=TMODEL.Teacher.objects.filter(depart=id)
     request.session['depid']=id
     return render(request,"exam/teacher_list.html",{'tch':tch})
def assgin_teacher(request,id):
    t= TMODEL.Teacher.objects.get(id=id)
    t.type=1
    ida=request.session['depid']
    dep=models.Departiment.objects.get(id=ida)
    dep.head=id
    t.save()
    dep.save()
    return redirect('exam:admin_view_departiment')
def register_collage(request):
    if request.method=="POST":
        name=request.POST.get('collage',False)
        descr=request.POST.get('descr',False)
        cl=Collage(name=name,descr=descr)
        cl.save()
        return redirect('exam:register_collage')
    colage=Collage.objects.filter()
    return render(request,"exam/register_collage.html",{'cl':colage})
def delete_colage(request,id):
    colage=Collage.objects.get(id=id)
    colage.delete()
    return redirect('exam:register_collage')
def permistion(request):
     if request.method=="POST":
        perm=request.POST.get('perm',False)
        type=request.POST.get('type',False)
        cl=Permision.objects.get(name=perm)
        cl.name=perm
        cl.perm=type
        cl.save()
        return redirect('exam:permistion')
     clas=Permision.objects.filter()
     return render(request,"exam/permision.html",{'cl':clas})
def first_exam(request,id):
    cour=Course.objects.get(id=id)
    cour.pre=1
    cour.save()
    return render(request,'exam/admin_course.html')
def add_student(request):
    courses = models.Departiment.objects.all()
    return render(request,'exam/add_student.html',{'courses':courses})

def view_student_marks(request):
    courses = models.Departiment.objects.all()
    return render(request,"exam/view_student_marks.html",{'courses':courses})
def student_marks(request,id):
    courses = models.Result.objects.filter(dep=id)
    return render(request,"exam/tudent_marks.html",{'courses':courses})
def livestreaming(request,id):
   
    St=SMODEL.Student.objects.filter(dep=id)
    return render(request,"teacher/livestreaming.html",{'st':St})
def sendmessage(request,id):
    return render(request,"sendemesage.html")
    
    
    
   
   
   


