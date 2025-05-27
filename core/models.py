from django.db import models

# Create your models here.

class CarouselSlider(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='carousel/')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def short_title(self):
        return self.title[:500]
    
    def short_description(self):
        return self.description[:112]


class Contact(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

