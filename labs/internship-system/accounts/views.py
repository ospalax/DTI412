from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group

from .forms import CustomUserCreationForm
from .models import InternshipRequest

from django.shortcuts import get_object_or_404
from .forms import InternshipRequestForm
from .models import InternshipRequest

# Create your views here.

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")

    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html', {'user': request.user})

@login_required
def lecturer_dashboard(request):
    # Check if user belongs to 'Lecturer' group or is superuser
    if not (request.user.groups.filter(name='Lecturer').exists() or request.user.is_superuser):
        raise PermissionDenied # Triggers 403 Forbidden Response
    return render(request, 'accounts/lecturer_dashboard.html')

@login_required
def profile(request):
    # Fetch the user's first assigned group (role) if it exists
    user_group = request.user.groups.first()
    role = user_group.name if user_group else "No Role Assigned"
    return render(request, 'accounts/profile.html', {'role': role})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Fetch the Student group and assign it to the new user
            student_group, created = Group.objects.get_or_create(name='Student')
            user.groups.add(student_group)

            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def dashboard(request):
    # Fetch requests for the logged-in student to pass to the dynamic dashboard
    student_requests = InternshipRequest.objects.filter(student=request.user)
    return render(request, 'accounts/dashboard.html', {'user': request.user, 'requests': student_requests})

@login_required
def lecturer_dashboard(request):
    if not (request.user.groups.filter(name='Lecturer').exists() or request.user.is_superuser):
        raise PermissionDenied
    # Fetch all pending requests for the lecturer to review
    pending_requests = InternshipRequest.objects.filter(status='Pending')
    return render(request, 'accounts/lecturer_dashboard.html', {'requests': pending_requests})

@login_required
def submit_request(request):
    # Only allow students
    if not request.user.groups.filter(name='Student').exists():
        raise PermissionDenied

    if request.method == 'POST':
        form = InternshipRequestForm(request.POST)
        if form.is_valid():
            internship_req = form.save(commit=False)
            internship_req.student = request.user # Tie request to the logged-in student
            internship_req.save()
            messages.success(request, "Internship request submitted successfully.")
            return redirect('dashboard')
    else:
        form = InternshipRequestForm()

    return render(request, 'accounts/submit_request.html', {'form': form})

@login_required
def update_request_status(request, request_id, action):
    # Only allow lecturers or admins
    if not (request.user.groups.filter(name='Lecturer').exists() or request.user.is_superuser):
        raise PermissionDenied

    internship_req = get_object_or_404(InternshipRequest, id=request_id)

    if action == 'approve':
        internship_req.status = 'Approved'
    elif action == 'reject':
        internship_req.status = 'Rejected'

    internship_req.save()
    messages.success(request, f"Request successfully {action}d.")
    return redirect('lecturer_dashboard')
