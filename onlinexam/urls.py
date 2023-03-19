from django.urls import path,include
from django.contrib import admin
from exam import views
from django.contrib.auth.views import LogoutView,LoginView
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static,serve
urlpatterns = [
   
    path('admin/',admin.site.urls),
    path('teacher/',include('teacher.urls',namespace="teacher")),
    path('student/',include('student.urls',namespace="student")),
    path('',include('exam.urls',namespace="exam")),
    path('core/',include('core.urls',namespace="core")),
    url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
