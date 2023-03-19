from django.urls import path,include
from django.contrib import admin
from . import views
from django.contrib.auth.views import LogoutView,LoginView
app_name="exam"
urlpatterns = [
    path('',views.home_view,name=''),
    path('logout', LogoutView.as_view(template_name='exam/logout.html'),name='logout'),
    path('contactus', views.contactus_view),
    path('afterlogin', views.afterlogin_view,name='afterlogin'),



    path('adminclick', views.adminclick_view),
    path('adminlogin', LoginView.as_view(template_name='exam/adminlogin.html'),name='adminlogin'),
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),
    path('admin-teacher', views.admin_teacher_view,name='admin-teacher'),
    path('admin-view-teacher', views.admin_view_teacher_view,name='admin-view-teacher'),
    path('update-teacher/<int:pk>', views.update_teacher_view,name='update-teacher'),
    path('delete-teacher/<int:pk>', views.delete_teacher_view,name='delete-teacher'),
    path('admin-view-pending-teacher', views.admin_view_pending_teacher_view,name='admin-view-pending-teacher'),
    path('admin-view-teacher-salary', views.admin_view_teacher_salary_view,name='admin-view-teacher-salary'),
    path('approve-teacher/<int:pk>', views.approve_teacher_view,name='approve-teacher'),
    path('reject-teacher/<int:pk>', views.reject_teacher_view,name='reject-teacher'),

    path('admin-student', views.admin_student_view,name='admin-student'),
    path('admin-view-student', views.admin_view_student_view,name='admin-view-student'),
    path('admin-view-student-marks', views.admin_view_student_marks_view,name='admin-view-student-marks'),
    path('admin-view-marks/<int:pk>', views.admin_view_marks_view,name='admin-view-marks'),
    path('admin-check-marks/<int:pk>', views.admin_check_marks_view,name='admin-check-marks'),
    path('update-student/<int:pk>', views.update_student_view,name='update-student'),
    path('delete_student_view/<int:id>', views.delete_student_view,name='delete_student_view'),

    path('admin-course/<int:id>', views.admin_course_view,name='admin-course'),
    path('admin-add-course', views.admin_add_course_view,name='admin-add-course'),
    path('admin-view-course', views.admin_view_course_view,name='admin-view-course'),
    path('delete-course/<int:pk>', views.delete_course_view,name='delete-course'),

    path('admin-question', views.admin_question_view,name='admin-question'),
    path('admin-add-question/<int:id>', views.admin_add_question_view,name='admin-add-question'),
    path('admin-view-question', views.admin_view_question_view,name='admin-view-question'),
    path('view-question/<int:pk>', views.view_question_view,name='view-question'),
    path('delete-question/<int:pk>', views.delete_question_view,name='delete-question'),
    path('register_depart/<int:id>',views.register_depart,name="register_depart"),
    path('admin_view_departiment/',views.admin_view_departiment,name="admin_view_departiment"),
    path('head/<int:id>/',views.head,name="head"),
    path('assgin_teacher/<int:id>/',views.assgin_teacher,name="assgin_teacher"),
    path('register_collage/',views.register_collage,name="register_collage"),
    path('delete_colage/<int:id>',views.delete_colage,name="delete_colage"),
    path('permistion/',views.permistion,name="permistion"),
    path('first_exam/<int:id>',views.first_exam,name="first_exam"),
    path('add_student/',views.add_student,name="add_student"),
    path('add_student_info/<int:id>',views.add_student_info,name="add_student_info"),
    path('view_student_marks/',views.view_student_marks,name="view_student_marks"),
    path('student_marks/<int:id>',views.student_marks,name="student_marks"),
    path('livestreaming/<int:id>',views.livestreaming,name="livestreaming"),
    path('sendmessage/<int:id>',views.sendmessage,name="sendmessage"),

    


 ]
 
 