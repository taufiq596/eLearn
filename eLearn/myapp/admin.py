from django.contrib import admin
from .models import BlogPost, Contact, BlogComment
# Register your models here.

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display=['id', 'title', 'content','author', 'view', 'slug', 'image', 'date']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'phone', 'description']

@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display=['id','comment', 'user', 'post', 'parent', 'timestamp']