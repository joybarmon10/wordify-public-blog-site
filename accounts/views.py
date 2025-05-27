from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from blog.models import PostBlog
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

# Create your views here.


def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("register")

        user = User.objects.create_user(
            first_name=first_name, last_name=last_name, email=email, username=username, password=password
        )
        user.save()
        messages.success(request, "User created successfully.")
        return redirect("login")
    return render(request, "register.html")

def user_login(request):
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, "Login successful.")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("login")
    return render(request, "login.html")


# user logout
def user_logout(request):
    logout(request)
    messages.success(request, "Logout successful.")
    return redirect("login")


@login_required
def profile(request):
    current_user = request.user
    try:
        profile = Profile.objects.get(user=current_user)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=current_user)

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        image = request.FILES.get("user-profile")
        bio = request.POST.get("bio")

        if first_name:
            current_user.first_name = first_name
        if last_name:
            current_user.last_name = last_name

        current_user.save()
        messages.success(request, "Profile Updated successfully.")

        if bio is not None: 
            profile.bio = bio
            profile.save()
            messages.success(request, "Bio updated successfully.")

        if image:
            profile.image = image
            profile.save()
            messages.success(request, "Profile Updated successfully.")

        return redirect("profile")

    blog = PostBlog.objects.filter(author=current_user)
    popular_blogs = PostBlog.objects.filter(views__gte=20, author=current_user).order_by("-views")
    return render(request, "profile.html", {"blog": blog, "popular_blogs": popular_blogs, "profile": profile})


def view_user_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = getattr(user, "profile", None)
    blog = PostBlog.objects.filter(author=user)

    popular_blogs = PostBlog.objects.filter(views__gte=20, author=user).order_by("-views")

    return render(
        request,
        "view_profile.html",
        {"user_profile": user, "profile": profile, "blog": blog, "popular_blogs": popular_blogs},
    )
