from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),

    # Custom Admin URLs
    path('admin-panel/', views.admin_login, name='admin_login'),
    path('admin-panel/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/delete/<int:student_id>/', views.admin_delete_student, name='admin_delete_student'),
    path('admin-panel/logout/', views.admin_logout, name='admin_logout'),
]
