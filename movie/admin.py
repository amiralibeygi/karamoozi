from django.contrib import admin
from .models import Movie, Comment, Category,Genre, Serie
# Register your models here.


admin.site.register(Movie)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Serie)
