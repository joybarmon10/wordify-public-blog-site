from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.

class PostBlog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def short_title(self):
        return self.title[:27]

    def short_description(self):
        return self.content[:112]

    def total_likes(self):
        return self.likes.count()

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            num = 1
            while PostBlog.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)


class BlogImage(models.Model):
    blog = models.ForeignKey(PostBlog, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="blog_images/")
    
    def __str__(self):
        return f"Image for {self.blog.title}"


class Comment(models.Model):
    blog = models.ForeignKey(
        PostBlog, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username}"
