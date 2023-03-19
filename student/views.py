from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from django.http import JsonResponse,HttpRequest
from datetime import date, timedelta
from exam import models as QMODEL
from teacher import models as TMODEL
from student import models as SModel
from django.contrib.auth.models import User
import cv2
import face_recognition 
import os
import numpy as np
import winsound
from django.db.models import Q
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading
#for showing signup/login button for student
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'student/studentclick.html')

def student_signup_view(request):
    userForm=forms.StudentUserForm()
    studentForm=forms.StudentForm()
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        username=request.session['username']
        t_dep=User.objects.get(username=username)
        userForm=forms.StudentUserForm(request.POST)
        studentForm=forms.StudentForm(request.POST,request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            student=studentForm.save(commit=False)
            student.user=user
            student.regby=t_dep.id
            student.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        return HttpResponseRedirect('studentlogin')
    return render(request,'student/studentsignup.html',context=mydict)

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    dict={
    
    'total_course':QMODEL.Course.objects.all().count(),
    'total_question':QMODEL.Question.objects.all().count(),
    }
    return render(request,'student/student_dashboard.html',context=dict)

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_exam_view(request):
    user=request.user
    name=User.objects.get(username=user)
    sid_id=name.id
    st=SModel.Student.objects.get(user_id=sid_id)
    print(st.dep)
    depid=st.dep
    depart=QMODEL.Departiment.objects.get(id=depid)
    cid=depart.pk
    courses=QMODEL.Course.objects.filter(dp=cid,pre=1)
    return render(request,'student/student_exam.html',{'courses':courses})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def take_exam_view(request,pk):
    perm=QMODEL.Permision.objects.get(name="camera")
    paerm=perm.perm
    request.session['c_id']=pk
    course=QMODEL.Course.objects.get(id=pk)
    request.session['course_id']=course.id
    total_questions=QMODEL.Question.objects.all().filter(course=course).count()
    questions=QMODEL.Question.objects.all().filter(course=course)
    total_marks=0
    for q in questions:
        total_marks=total_marks + q.marks
    
    return render(request,'student/take_exam.html',{'course':course,'total_questions':total_questions,'total_marks':total_marks,'perm':paerm})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def start_exam_view(request,pk):
    id=request.user.id 
   
    course=QMODEL.Course.objects.get(id=pk)
    
    questions=QMODEL.Question.objects.all().filter(course=course)
    
    if is_ajax(request=request):
        sc=TMODEL.Schedule.objects.get(exam=pk)
        time=sc.tim
        dat=sc.dat
        dur=sc.dur
        return JsonResponse({'dat':dat,'tim':time,'dur':dur},status=200)
    questions=QMODEL.Question.objects.all().filter(course=course)
    if request.method=='POST':
        pass
    response= render(request,'student/start_exam.html',{'course':course,'questions':questions,'id':id})
    response.set_cookie('course_id',course.id)
    return response


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def calculate_marks_view(request):
    #if request.is_ajax():
        
    if request.COOKIES.get('course_id') is not None:
        course_id = request.COOKIES.get('course_id')
        course=QMODEL.Course.objects.get(id=course_id)
        
        total_marks=0
        questions=QMODEL.Question.objects.all().filter(course=course)
        for i in range(len(questions)):
            
            selected_ans = request.COOKIES.get(str(i+1))
            actual_answer = questions[i].answer
           
            if selected_ans[i]== actual_answer[i]:
                total_marks+=1*questions[i].marks
                print(total_marks)
                
                #total_marks= total_marks+questions[i].marks
        student = models.Student.objects.get(user_id=request.user.id)
        result = QMODEL.Result()
        result.marks=total_marks
        result.exam=course
        result.student=student
        result.dep=student.dep
        result.save()
        print(total_marks)

        return HttpResponseRedirect('view-result')



@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def view_result_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/view_result.html',{'courses':courses})
    

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def check_marks_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    student = models.Student.objects.get(user_id=request.user.id)
    results= QMODEL.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request,'student/check_marks.html',{'results':results})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_marks_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/student_marks.html',{'courses':courses})



last_face = 'no_face'
current_path = os.path.dirname(__file__)
sound_folder = os.path.join(current_path, 'static/sound/')
face_list_file = os.path.join(current_path, 'face_list.txt')
sound = os.path.join(sound_folder, 'beep.wav')


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()
    def is_ajax(request):
        return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
   
    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
    
    def update(self):
        request=self
        known_face_encodings = []
        known_face_names = []
        profiles = SModel.Student.objects.all()
        for profile in profiles:
            person = profile.profile_pic
            image_of_person = face_recognition.load_image_file(f'static/{person}')
            
        
            person_face_encoding = face_recognition.face_encodings(image_of_person)[0]
            known_face_encodings.append(person_face_encoding)
            known_face_names.append(f'{person}'[:-10])
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True
        while True:
            (self.grabbed, self.frame) = self.video.read()
            small_frame = cv2.resize(self.frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]
            if process_this_frame:
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(
                    rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"
                        
                        
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    
                    if not matches[best_match_index]:
                        print("not")
                           
                    elif matches[best_match_index]:
                        name = known_face_names[best_match_index]
                        print("yes") 
                       
                            
                            
                    else:
                        print("either") 
                          
                           
                    profile = SModel.Student.objects.get(Q(profile_pic__icontains=name))
                       # return JsonResponse({'not':1},status=200)
                 
                    face_names.append(name)
                    
            process_this_frame = not process_this_frame

            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                cv2.rectangle(self.frame, (left, top), (right, bottom), (0, 0, 255), 2)

                cv2.rectangle(self.frame, (left, bottom - 35),
                            (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(self.frame, name, (left + 6, bottom - 6),
                            font, 0.5, (255, 255, 255), 1)
                #cv2.imshow('Video', self.frame)

                #cv2.waitKey(10)
                  # break


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@gzip.gzip_page
def livefe(request):
    try:
        
      cam = VideoCamera()
      return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except: 
        pass


def studentloginback(request):
     return redirect('student:student-dashboard')
class LiveStraming(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.fram) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()
    def is_ajax(request):
        return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
   
    def get_frame(self):
        image = self.fram
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
    
    def update(self):
        request=self
        known_face_encodings = []
        known_face_names = []
        profiles = SModel.Student.objects.all()
        for profile in profiles:
            person = profile.profile_pic
            image_of_person = face_recognition.load_image_file(f'static/{person}')
            
        
            person_face_encoding = face_recognition.face_encodings(image_of_person)[0]
            known_face_encodings.append(person_face_encoding)
            known_face_names.append(f'{person}'[:-10])
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True
        while True:
            (self.grabbed, self.fram) = self.video.read()
            small_frame = cv2.resize(self.fram, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]
            if process_this_frame:
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(
                    rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"
                        
                        
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    
                    if not matches[best_match_index]:
                        print("not")
                           
                    elif matches[best_match_index]:
                        name = known_face_names[best_match_index]
                        print("yes") 
                        student_marks_view(self)
                        #return redirect('student:')
                            
                            
                    else:
                        print("either") 
                          
                           
                    profile = SModel.Student.objects.get(Q(profile_pic__icontains=name))
                       # return JsonResponse({'not':1},status=200)
                 
                    face_names.append(name)
                    
            process_this_frame = not process_this_frame

            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                cv2.rectangle(self.fram, (left, top), (right, bottom), (0, 0, 255), 2)

                cv2.rectangle(self.fram, (left, bottom - 35),
                            (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(self.fram, name, (left + 6, bottom - 6),
                            font, 0.5, (255, 255, 255), 1)
                #cv2.imshow('Video', self.frame)

                #cv2.waitKey(10)
                  # break


def gena(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
@gzip.gzip_page
def livestram(request,id):
    try:
      cam = LiveStraming()
      return StreamingHttpResponse(gena(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except: 
        pass


   