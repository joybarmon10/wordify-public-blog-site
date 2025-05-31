from django.shortcuts import render, redirect
from blog.models import PostBlog
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Contact
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def home(request):
    blog = PostBlog.objects.all()
    paginator = Paginator(blog, 9)
    page = request.GET.get("page")
    try:
        blog = paginator.page(page)
    except PageNotAnInteger:
        blog = paginator.page(1)
    except EmptyPage:
        blog = paginator.page(paginator.num_pages)

    popular_blogs = PostBlog.objects.filter(views__gte=20).order_by("-views")

    context = {
        "blog": blog,
        "paginator": paginator,
        "popular_blogs": popular_blogs,
    }

    return render(request, "home.html", context)


@login_required
def contact(request):
    current_user = request.user
    if request.method == 'POST':
        user = current_user
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        contact = Contact(
            user=user,
            name=name,
            email=email,
            message=message
        )
        contact.save()
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('home')
    return render(request, "contact.html")

def about(request):
    return render(request, "about.html")
