from django.shortcuts import get_object_or_404, render,redirect

from blog.models import PostBlog, Comment, BlogImage
from django.contrib import messages
from django.contrib.auth.decorators import login_required   
from django.db.models import Q
from django.contrib.auth.models import User


# Create your views here.
@login_required
def post_blog(request):
    current_user = request.user

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        images = request.FILES.getlist("image")

        post = PostBlog.objects.create(
            title=title, content=content, author=current_user
        )

        for img in images:
            BlogImage.objects.create(blog=post, image=img)

        messages.success(request, "Post created successfully.")

    return render(request, "post_blog.html")


@login_required
def blog_details(request, slug):
    post = get_object_or_404(PostBlog, slug=slug)

    session_key = f"viewed_post_{post.id}"
    if not request.session.get(session_key, False):
        post.views += 1
        post.save(update_fields=["views"])
        request.session[session_key] = True

    comments = post.comments.filter(parent__isnull=True).order_by("-created_at")

    if request.method == "POST":
        body = request.POST.get("body")
        parent_id = request.POST.get("parent_id")
        parent_obj = None

        if parent_id:
            parent_obj = Comment.objects.filter(id=parent_id).first()

        if body and request.user.is_authenticated:
            Comment.objects.create(
                blog=post, user=request.user, body=body, parent=parent_obj
            )
            messages.success(request, "Comment posted successfully.")
            return redirect("blog_details", slug=slug)
        
    user = get_object_or_404(User, username=post.author.username)
    # Fetch popular blogs by the same author with at least 20 views
    popular_blogs = PostBlog.objects.filter(views__gte=20, author=user).order_by("-views")

    context = {
        "popular_blogs": popular_blogs,
        "post": post,
        "comments": comments,
        "liked": (
            request.user in post.likes.all() if request.user.is_authenticated else False
        ),
        "total_likes": post.likes.count(),
    }

    return render(request, "blog_details.html", context)


@login_required
def like_post(request, slug):
    post = get_object_or_404(PostBlog, slug=slug)
    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)
    else:
        post.likes.add(user)

    return redirect("blog_details", slug=slug)


@login_required
def reply_comment(request):
    if request.method == "POST":
        parent_id = request.POST.get("parent_id")
        blog_id = request.POST.get("blog_id")
        body = request.POST.get("body")

        blog = get_object_or_404(PostBlog, id=blog_id)
        parent_comment = get_object_or_404(Comment, id=parent_id)

        Comment.objects.create(
            blog=blog, user=request.user, body=body, parent=parent_comment
        )
        messages.success(request, "Your reply has been posted.")

        return redirect("blog_details", slug=blog.slug)


def search_view(request):
    query = request.GET.get("query", "")
    results = PostBlog.objects.none()
    if query:
        results = PostBlog.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    return render(request, "search_results.html", {"query": query, "results": results})
