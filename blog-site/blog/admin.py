from django.contrib import admin
from .models import PostBlog, Comment, BlogImage


# Inline model for BlogImage
class BlogImageInline(admin.TabularInline):
    model = BlogImage
    extra = 1  # Number of empty forms to display by default


# Admin class for PostBlog
class PostBlogAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "created_at",
        "updated_at",
    )  
    search_fields = (
        "title",
        "content",
        "author__username",
    )  
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("created_at", "author") 
    inlines = [BlogImageInline] 



admin.site.register(PostBlog, PostBlogAdmin)



class CommentAdmin(admin.ModelAdmin):
    list_display = ("blog", "user", "created_at")
    search_fields = ("body",) 
    list_filter = ("created_at",)



admin.site.register(Comment, CommentAdmin)

admin.site.register(BlogImage)
