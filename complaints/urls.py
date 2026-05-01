from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_dashboard, name='student_dashboard'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('submit/', views.submit_complaint, name='submit_complaint'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/update/<int:pk>/', views.update_complaint_status, name='update_status'),
    path('admin-dashboard/delete/<int:pk>/', views.delete_complaint, name='delete_complaint'),
]
