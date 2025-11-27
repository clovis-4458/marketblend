from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

# =========================
# LOGIN VIEW
# =========================
def index(request):
    """
    Login view. Handles 'next' parameter to redirect after login.
    """
    next_url = request.GET.get('next') or request.POST.get('next') or '/'

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html", {"next": next_url})


# =========================
# REGISTER VIEW
# =========================
def register_view(request):
    """
    Register view. Handles 'next' parameter to redirect after registration.
    """
    next_url = request.GET.get('next') or request.POST.get('next') or '/'

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            messages.success(request, f"Welcome {username}! Your account has been created.")
            return redirect(next_url)

    return render(request, "register.html", {"next": next_url})


# =========================
# LOGOUT VIEW
# =========================
def logout_view(request):
    """
    Logs out the user and redirects to the homepage or login page.
    """
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('home')  # or 'accounts:index' if you prefer to send them to login page
