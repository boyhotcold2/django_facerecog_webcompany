from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [

    path('dashboard/', views.dashboard, name='dashboard'),

    path('nav_calendar/', views.nav_calendar, name='nav_calendar'),


    path('index/', views.index, name='index'),
    path('video_stream/', views.video_stream, name='video_stream'),
    path('add_photos/', views.add_photos, name='add_photos'),
    path('add_photos/<slug:emp_id>/', views.click_photos, name='click_photos'),
    path('train_model/', views.train_model, name='train_model'),
    path('detected/', views.detected, name='detected'),
    path('identify/', views.identify, name='identify'),
    path('add_emp/', views.add_emp, name='add_emp'),

    path('all_students/', views.all_students, name="all_students"),
    path('absent_students/', views.absent_students, name="absent_students"),
    path('report/', views.report, name="report"),
    path('about/', views.about, name="about"),
    path('send_file/', views.send_file, name="send_file"),
    path('send/', views.send, name="send"),


    path('', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),

    path('addPhoto/', views.addPhoto, name="addPhoto"),

    path('all_students/', views.all_students, name="all_students"),
    path('absent_students/', views.absent_students, name="absent_students"),
    path('profile/<str:pk>/', views.profile, name="profile"),
    path('delete/<str:pk>', views.deleteStudent, name='delete'),

    path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),


]
