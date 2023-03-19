from django.urls import path
from teacher import views
from django.contrib.auth.views import LoginView
app_name="teacher"
urlpatterns = [
path('teacherclick', views.teacherclick_view),
path('teacherlogin', LoginView.as_view(template_name='teacher/teacherlogin.html'),name='teacherlogin'),
path('teachersignup', views.teacher_signup_view,name='teachersignup'),
path('teacher-dashboard', views.teacher_dashboard_view,name='teacher-dashboard'),
path('teacher-exam', views.teacher_exam_view,name='teacher-exam'),
path('teacher-add-exam', views.teacher_add_exam_view,name='teacher-add-exam'),
path('teacher-view-exam', views.teacher_view_exam_view,name='teacher-view-exam'),
path('delete-exam/<int:pk>', views.delete_exam_view,name='delete-exam'),


path('teacher-question', views.teacher_question_view,name='teacher-question'),
path('teacher-add-question', views.teacher_add_question_view,name='teacher-add-question'),
path('teacher-view-question', views.teacher_view_question_view,name='teacher-view-question'),
path('see-question/<int:pk>', views.see_question_view,name='see-question'),
path('remove-question/<int:pk>', views.remove_question_view,name='remove-question'),

path('teacher_manage_course/',views.teacher_manage_course,name="teacher_manage_course"),
path('qtdelete/<int:id>/',views.qtdelete,name="qtdelete"),
path(' teacher_wiew_course/',views.teacher_wiew_course,name="teacher_wiew_course"),
path('register_student_view/',views.register_student_view,name="register_student_view"),
path('teacher_add_student/',views.teacher_add_student,name="teacher_add_student"),
path('delete_student/<int:id>',views.delete_student,name="delete_student"),
path('student_marks/',views.student_marks,name="student_marks"),
path('exam_schedule/<int:id>',views.exam_schedule,name="exam_schedule"),
path('update-student/<int:pk>', views.update_student_view,name='update-student'),
path('livestreaming/',views.livestreaming,name="livestreaming"),
path('assgine_lecturer/<int:id>',views.assgine_lecturer,name="assgine_lecturer"),

]