from django.urls import path
from . import views

urlpatterns = [
    # Core Lab Routes
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('lecturer/', views.lecturer_dashboard, name='lecturer_dashboard'),

    # Challenge Routes
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('submit-request/', views.submit_request, name='submit_request'),
    path('update-request/<int:request_id>/<str:action>/', views.update_request_status, name='update_request_status'),
]
