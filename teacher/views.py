from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from exam import models as QMODEL
from student import models as SMODEL
from exam import forms as QFORM
from .models import Teacher,Schedule
from django.contrib.auth.models import User
from exam.models import Question
from exam.models import Course,Departiment
from student import forms as sforms
from student import forms as SFORM
#for showing signup/login button for teacher
def teacherclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'teacher/teacherclick.html')

def teacher_signup_view(request):
    userForm=forms.TeacherUserForm()
    teacherForm=forms.TeacherForm()
    mydict={'userForm':userForm,'teacherForm':teacherForm}
    if request.method=='POST':
        userForm=forms.TeacherUserForm(request.POST)
        teacherForm=forms.TeacherForm(request.POST,request.FILES)
        if userForm.is_valid() and teacherForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            teacher=teacherForm.save(commit=False)
            teacher.user=user
            teacher.save()
            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)
        return HttpResponseRedirect('teacherlogin')
    return render(request,'teacher/teachersignup.html',context=mydict)



def is_teacher(user):
    
    return user.groups.filter(name='TEACHER').exists()

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_dashboard_view(request):
    request.session['username']=request.user.username
    teacher=User.objects.get(username=request.session['username'])
    tech=Teacher.objects.get(user_id=teacher.id)
    dict={
    
    'total_course':QMODEL.Course.objects.all().count(),
    'total_question':QMODEL.Question.objects.all().count(),
    'total_student':SMODEL.Student.objects.all().count(),
    'usertype':tech.type,
    }
    return render(request,'teacher/teacher_dashboard.html',context=dict)

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_exam_view(request):
    return render(request,'teacher/teacher_exam.html')


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_add_exam_view(request):
    courseForm=QFORM.CourseForm()
    if request.method=='POST':
        courseForm=QFORM.CourseForm(request.POST)
        if courseForm.is_valid():        
            courseForm.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/teacher/teacher-view-exam')
    return render(request,'teacher/teacher_add_exam.html',{'courseForm':courseForm})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_exam_view(request):
    courses = QMODEL.Course.objects.all()
    return render(request,'teacher/teacher_view_exam.html',{'courses':courses})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def delete_exam_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    course.delete()
    return HttpResponseRedirect('/teacher/teacher-view-exam')

@login_required(login_url='adminlogin')
def teacher_question_view(request):
    return render(request,'teacher/teacher_question.html')

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_add_question_view(request):
   
    if request.method=='POST':
       
        course=request.POST.get('course',False)
        question=request.POST.get('question',False)
        option1=request.POST.get('option1',False)
        option2=request.POST.get('option2',False)
        option3=request.POST.get('option3',False)
        option4=request.POST.get('option4',False)
        answer=request.POST.get('answer',False)
        mark=request.POST.get('mark',False)
        dep=request.POST.get('id',False)
        cv=Course.objects.get(id=course)
        username=request.session['username']
        t_dep=User.objects.get(username=username)
        qtn=Question(adby=t_dep,marks=mark,course=cv,question=question,option1=option1,option2=option2,option3=option3,option4=option4,answer=answer,dep=dep)
        qtn.save()
        print("form is invalid")
        return HttpResponseRedirect('/teacher/teacher-add-question')
        #return HttpResponseRedirect('/teacher/teacher-view-question')
    username=request.session['username']
    t_dep=User.objects.get(username=username)
    depart=t_dep.pk
    dep=Teacher.objects.get(user_id=depart)
    dp_id=dep.depart
    t_course=dep.course
    cours=Course.objects.get(id=t_course)
    course=cours.id
    course_name=cours.course_name
    cour=QMODEL.Course.objects.get(id=course)
    questions=QMODEL.Question.objects.all().filter(course=cour)
    student=QMODEL.Result.objects.filter(exam_id=course)
    #if request.method=='POST':
    #    pass
    #response= render(request,'student/start_exam.html',{'course':course,'questions':questions})
    #response.set_cookie('course_id',course.id)
    
    return render(request,'teacher/add_question.html',{'exam':student,'username':dp_id,'course':course,'questions':questions,'course_name':course_name})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_question_view(request):
    username=request.session['username']
    t_dep=User.objects.get(username=username)
    techer_id=Teacher.objects.get(user_id=t_dep.id)
    
    courses= QMODEL.Course.objects.filter(id=techer_id.course)
    return render(request,'teacher/teacher_view_question.html',{'courses':courses})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def see_question_view(request,pk):
    questions=QMODEL.Question.objects.all().filter(course_id=pk)
    return render(request,'teacher/see_question.html',{'questions':questions})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def remove_question_view(request,pk):
    question=QMODEL.Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/teacher/teacher-view-question')
def exam_schedule(request,id):
    username=request.session['username']
    t_dep=User.objects.get(username=username)
    depart=t_dep.id
    dep=Teacher.objects.get(user_id=depart)
    dp_id=dep.id
    dc=dep.depart
    t_course=dep.course
    cours=Course.objects.get(id=id)
    excourse=cours.id
    
    if request.method=="POST":
        time=request.POST.get('time',False)
        dat=request.POST.get('date',False)
        dur=request.POST.get('dr',False)
        sc=Schedule.objects.get(exam= excourse)
        sc.tim=time
        sc.dat=dat
        sc.dur=dur
        co=Course.objects.filter(dp=dc)
        for b in co:
          
           
            b.pre=0
            b.save()
        cours=Course.objects.get(id=id)
        cours.pre=1
        cours.save()
        sc.save()
        return redirect('teacher:teacher_manage_course')
    return render(request,"teacher/exam_schedule.html")
def teacher_manage_course(request):
    courseForm=QFORM.CourseForm()
    user=request.session['username']
    teacher_id=User.objects.get(username=user)
    depart=Teacher.objects.get(user_id=teacher_id.pk)
    dp_id=depart.depart
    if request.method=='POST':
        courseForm=QFORM.CourseForm(request.POST)
        if courseForm.is_valid():        
            courseForm.save()
            c_c=courseForm.cleaned_data['c_code']
            c_name=courseForm.cleaned_data['course_name']
           
            qd=QMODEL.Course.objects.get(course_name=c_name)
            dat="2023-03-19"
            time="11:17"
            dur=120
            dpe_id=QMODEL.Departiment.objects.get(id=depart.depart)
            qd.dp=dpe_id
            qd.save()
            sc=Schedule(dat=dat,tim=time,dur=dur,adby=dp_id,exam= qd.id)
            sc.save()
        else:
            print("form is invalid")
        return redirect('teacher:teacher_manage_course')
    username=request.session['username']
    t_dep=User.objects.get(username=username)
    depart=t_dep.id
    dep=Teacher.objects.get(user_id=depart)
    course=Course.objects.filter(dp=dep.depart)
    return render(request,'teacher/teacher_manage_course.html',{'courseForm':courseForm,'coures':course})
def qtdelete(request,id):
    question=QMODEL.Question.objects.get(id=id)
    question.delete()
    return HttpResponseRedirect('/teacher/teacher-add-question')
def teacher_wiew_course(request):
    courses = QMODEL.Course.objects.all()
    return render(request,"teacher_wiew_course.html",{'courses':courses})
def register_student_view(request):
    context={'total_student':SMODEL.Student.objects.all().count(),
              }
    return render(request,"teacher/register_student.html",context=context)
def teacher_add_student(request):
    username=request.session['username']
    t_dep=User.objects.get(username=username)
    
    techer=Teacher.objects.get(user_id=t_dep.id)
    student= SMODEL.Student.objects.filter(dep=techer.depart)
    userForm=SFORM.StudentUserForm()
    studentForm=forms.StudentForm()
    mydict={'userForm':userForm,'studentForm':studentForm,'students':student}
    if request.method=='POST':
        
        t_dep=User.objects.get(username=username)
        userForm=SFORM.StudentUserForm(request.POST)
        studentForm=forms.StudentForm(request.POST,request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            student=studentForm.save(commit=False)
            student.user=user
            student.regby=t_dep.id
            student.dep=techer.depart
            student.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
    return render(request,"teacher/teacher_add_student.html",context=mydict)

def delete_student(request,id):
    st= SMODEL.Student.objects.get(id=id)
    st.delete()
    user=User.objects.get(id=st.user_id)
    user.delete()
    return redirect('teacher:teacher_add_student')

def student_marks(request):
    user=request.user.id
    t_user=Teacher.objects.get(user_id=user)
    courses = QMODEL.Result.objects.filter(dep=t_user.depart)
    return render(request,"teacher/student_marks.html",{'courses':courses})
def update_student_view(request,pk):
    student=SMODEL.Student.objects.get(id=pk)
    user=SMODEL.User.objects.get(id=student.user_id)
    userForm=SFORM.StudentUserForm(instance=user)
    studentForm=SFORM.StudentForm(request.FILES,instance=student)
    username=request.session['username']
        
    t_dep=User.objects.get(username=username)
    techer=Teacher.objects.get(user_id=t_dep.id)
    stud= SMODEL.Student.objects.filter(dep=techer.depart)
    mydict={'userForm':userForm,'studentForm':studentForm,'students':stud}
 
    if request.method=='POST':
        userForm=SFORM.StudentUserForm(request.POST,instance=user)
        studentForm=SFORM.StudentForm(request.POST,request.FILES,instance=student)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            student.user=user
            student.regby=t_dep.id
            student.dep=techer.depart
            studentForm.save()
            return redirect('teacher:teacher_add_student')
    return render(request,'teacher/update_student.html',context=mydict)
def livestreaming(request):
    username=request.session['username']
        
    t_dep=User.objects.get(username=username)
    tcher=Teacher.objects.get(id=t_dep.pk)
    St=SMODEL.Student.objects.filter(dep=tcher.depart)
    return render(request,"teacher/livestreaming.html",{'st':St})
def assgine_lecturer(request,id):
    if request.method=="POST":
        cou_id=request.POST.get('course',False)
        lectur=request.POST.get('lectur',False)
        lec=Teacher.objects.get(id=lectur)
        lec.course=cou_id
        lec.save()
    dp=Course.objects.get(id=id)
    lec=Teacher.objects.filter(depart=dp.dp_id)
    return render(request,"teacher/assgine_lectur.html",{'lec':lec,'id':id})
    
    