from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied

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

