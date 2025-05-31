from django.contrib import admin
from .models import Contact, CarouselSlider
# Register your models here.
class ContactAdmin(admin.ModelAdmin):
    list_display = ('user','name', 'email', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
admin.site.register(Contact, ContactAdmin)

class CarouselSliderAdmin(admin.ModelAdmin):
    list_display = ('short_title', 'created_at')
    search_fields = ('title',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)
admin.site.register(CarouselSlider, CarouselSliderAdmin)