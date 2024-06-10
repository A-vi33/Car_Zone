from django.contrib import admin
from .models import Car, Comment

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'color', 'quantity','price')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name','created_at')