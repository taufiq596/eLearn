from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class BlogPost(models.Model):
    # class Meta:
    #     ordering=("-date",)
    title = models.CharField(max_length=150)
    content = models.TextField()
    author = models.CharField(max_length=100, default="")
    view = models.IntegerField(default=0)
    slug = models.CharField(max_length=150)
    image = models.ImageField()
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.title

class Contact(models.Model):
    name = models.CharField(max_length = 100)
    email = models.EmailField(max_length = 100)
    phone = models.BigIntegerField()
    description = models.TextField()

    def __str__(self):
        return self.name

class BlogComment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment
            