from django.shortcuts import render, HttpResponse, redirect
from .models import *
from .forms import *
import face_recognition
import cv2
import numpy as np
import winsound
from django.db.models import Q
from playsound import playsound
import os
from .models import  Profile
from student.models import Student




last_face = 'no_face'
current_path = os.path.dirname(__file__)
sound_folder = os.path.join(current_path, 'sound/')
face_list_file = os.path.join(current_path, 'face_list.txt')
sound = os.path.join(sound_folder, 'beep.wav')


def index(request):
    scanned = LastFace.objects.all().order_by('date').reverse()
    present = Profile.objects.filter(present=True).order_by('updated').reverse()
    absent = Profile.objects.filter(present=False).order_by('shift')
    nm=request.session['username']
    un=User.objects.get(username=nm)
    type=un.type 
    sup=un.is_superuser
    context = {
        'scanned': scanned,
        'present': present,
        'absent': absent,
        'type':type,'nm':nm,'sup':sup
    }
    return render(request, 'core/index.html', context)


def ajax(request):
    last_face = LastFace.objects.last()
    context = {
        'last_face': last_face
    }
    return render(request, 'core/ajax.html', context)


def scan(request):

    global last_face

    known_face_encodings = []
    known_face_names = []

    profiles = Student.objects.all()
    for profile in profiles:
        person = profile.profile_pic
        image_of_person = face_recognition.load_image_file(f'static/{person}')
        
    
        person_face_encoding = face_recognition.face_encodings(image_of_person)[0]
        known_face_encodings.append(person_face_encoding)
        known_face_names.append(f'{person}'[:-10])


    video_capture = cv2.VideoCapture(0)

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:

        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(
                rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(
                    known_face_encodings, face_encoding)
                name = "you are Unknown person"

                face_distances = face_recognition.face_distance(
                    known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                    profile = Profile.objects.get(Q(image__icontains=name))
                    
                    if profile.present == True:
                        pass
                    else:
                        profile.present = True
                        profile.save()

                    if last_face != name:
                        last_face = LastFace(last_face=name,user=profile)
                        last_face.save()
                        last_face = name
                        winsound.PlaySound(sound, winsound.SND_ASYNC)
                    else:
                        pass

                face_names.append(name)

        process_this_frame = not process_this_frame

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            cv2.rectangle(frame, (left, bottom - 35),
                          (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6),
                        font, 0.5, (255, 255, 255), 1)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == 13:
            break

    video_capture.release()
    cv2.destroyAllWindows()
    return HttpResponse('scaner closed', last_face)


def profiles(request):
    profiles = Profile.objects.all()
    nm=request.session['username']
    un=User.objects.get(username=nm)
    type=un.type 
    sup=un.is_superuser
    context = {
        'profiles': profiles,
        'type':type,'nm':nm,'sup':sup
    }
    return render(request, 'core/profiles.html', context)


def details(request):
    try:
       
        last_face = LastFace.objects.last()
        profile = Profile.objects.get(Q(image__icontains=last_face))
    except:
        last_face = None
        profile = None

    context = {
        'profile': profile,
        'last_face': last_face
    }
    return render(request, 'core/details.html', context)


def add_profile(request):
    #form = ProfileForm()
    if request.method == 'POST' :
        fn=request.POST.get('fname',False)
        ln=request.POST.get('lname',False)
        un=request.POST.get('unsername',False)
        #unl=request.session['usrn']
        adby=request.session['username']
      
        us=User.objects.get(username=un)
        nn=us.type
        gen=request.POST.get('gender',False)
        phon=request.POST.get('phone',False)
        em=request.POST.get('email',False)
        sal=request.POST.get('salary',False)
        ex=request.POST.get('exp',False)
        gfrom=request.POST.get('gfrom',False)
        gyea=request.POST.get('gyear',False)
        imag=request.FILES['image'] 
        age=request.POST.get('age',False)
        pro=request.POST.get('pro',False)
        status=request.POST.get('status',False)
        shift=request.POST.get('shift',False)
        rank=request.POST.get('rank',False)
         
        en=Profile.objects.create(adby=adby,type=nn,first_name=fn,last_name=ln,username=us,gender=gen,phone=phon,email=em,salary=sal,exp=ex,gfrom=gfrom,gyear=gyea,image=imag,age=age,profession=pro,status=status,ranking=rank,shift=shift)  
        en.save()
        return redirect('core:profiles')
        
        
        #form = ProfileForm(request.POST,request.FILES)
        #if form.is_valid():
            #form.save()
            #return redirect('core:profiles')
    #context={'form':form}
    un=request.session['usrn']
    nm=request.session['username']
    un=User.objects.get(username=nm)
    type=un.type 
    sup=un.is_superuser
    return render(request,'core/add_profile.html',{'un':un, 'type':type,'nm':nm,'sup':sup})


def edit_profile(request,id):
    profile = Profile.objects.get(id=id)
    
    if request.method == 'POST':
        fn=request.POST.get('fname',False)
        ln=request.POST.get('lname',False)
        #us=request.POST.get('username',False)
        gen=request.POST.get('gender',False)
        phon=request.POST.get('phone',False)
        em=request.POST.get('email',False)
        sal=request.POST.get('salary',False)
        ex=request.POST.get('exp',False)
        gfrom=request.POST.get('gfrom',False)
        gyea=request.POST.get('gyear',False)
        imag=request.FILES['image'] 
        age=request.POST.get('age',False)
        pro=request.POST.get('pro',False)
        status=request.POST.get('status',False)
        shift=request.POST.get('shift',False)
        rank=request.POST.get('rank',False)
        p = Profile.objects.get(id=id)
        p.first_name=fn
        p.last_name=ln
        #p.username=us
        p.gender=gen
        p.phone=phon
        p.email=em
        p.salary=sal
        p.exp=ex
        p.gfrom=gfrom
        p.gyear=gyea
        p.image=imag
        p.age=age
        p.profession=pro
        p.status=status
        p.shift=shift
        p.ranking=rank
        p.save()
        return redirect('core:profiles')
    nm=request.session['username']
    un=User.objects.get(username=nm)
    type=un.type 
    sup=un.is_superuser
        
    return render(request,'core/edit_profile.html',{'pro':profile, 'type':type,'nm':nm,'sup':sup})


def delete_profile(request,id):
    profile = Profile.objects.get(id=id)
    profile.delete()
    return redirect('core:profiles')


def clear_history(request):
    history = LastFace.objects.all()
    history.delete()
    return redirect('core:index')


def reset(request):
    profiles = Profile.objects.all()
    for profile in profiles:
        if profile.present == True:
            profile.present = False
            profile.save()
        else:
            pass
    return redirect('core:index')

