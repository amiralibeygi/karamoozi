from django.contrib.auth.models import AbstractUser,User
from django.db import models
from django.utils import timezone
import os
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Genre(models.Model):
    ename = models.CharField(max_length=50, null=True, blank=True, default="")
    name = models.CharField(max_length=20, null=True, blank=True, default='')

    def __str__(self):
        return self.name

def custom_image_path(instance, filename):
    # Customize the image path and filename based on parameters
    return os.path.join('images', filename)

class Movie(models.Model):
    ename = models.CharField(max_length=100, default="")
    name = models.CharField(max_length=100)
    actors = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    director = models.CharField(max_length=100)
    genre = models.ManyToManyField(Genre)
    path_to_file = models.FileField(upload_to='movies/', null=True, blank=True)
    cover_image = models.ImageField(upload_to=custom_image_path, null=True, blank=True)
    backdrop_image = models.ImageField(upload_to=custom_image_path, null=True, blank=True)
    comment = models.ManyToManyField('Comment', related_name='movie_comments', null=True, blank=True, default="")
    country = models.CharField(max_length=50)
    description = models.TextField()
    year = models.PositiveIntegerField( null=True)
    add_to_website = models.DateField(default=timezone.now)
    duration = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category,  on_delete=models.SET_NULL, null=True, blank=True, default="action")


    def __str__(self):
        return self.name

class Serie(models.Model):
    ename = models.CharField(max_length=100, default="")
    name = models.CharField(max_length=100)
    actors = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    director = models.CharField(max_length=100)
    genre = models.ManyToManyField(Genre)
    path_to_file = models.FileField(upload_to='series/', null=True, blank=True)
    cover_image = models.ImageField(upload_to=custom_image_path, null=True, blank=True)
    backdrop_image = models.ImageField(upload_to=custom_image_path, null=True, blank=True)
    comment = models.ManyToManyField('Comment', related_name='serie_comments', null=True, blank=True, default="")
    country = models.CharField(max_length=50)
    description = models.TextField()
    year = models.PositiveIntegerField( null=True)
    add_to_website = models.DateField(default=timezone.now)
    duration = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name



class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="", null=True, blank=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE,related_name='movie_comments', default="", null=True, blank=True)  # Assuming you have a Movie model
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE,related_name='serie_comments', default="", null=True, blank=True)  # Assuming you have a Movie model
    text = models.TextField(null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Comment by {self.user} on {self.movie or self.serie}'

