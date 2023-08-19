from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Movie, Comment, User, Serie, Genre
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.urls import reverse
from django.http import HttpResponse
import httpagentparser
import json
import re
def Home(request):
    all_shows = list(Movie.objects.all()) + list(Serie.objects.all())
    genres = Genre.objects.all()

    return render(request, 'home.html', {'shows': all_shows, 'genres': genres})

## use for live search result 
def search_movies(request):
    query = request.GET.get('q', '')
    serialized_results = ''
    pattern = r'\b[a-zA-Z]+|[0-9]+\b'
    matched = re.search(pattern, query)
    print(matched)
    if matched:
        print(query)
        
        results = Movie.objects.filter(ename__icontains=query).values('id', 'name','cover_image', 'country', 'genre', 'category', 'ename', 'year')
        results_list = list(results)

        results1 = Serie.objects.filter(ename__icontains=query).values('id', 'name','cover_image', 'country', 'genre', 'category', 'ename', 'year')
        results_list.append(list(results1))
        print(results_list[0])
        serialized_results = json.dumps(results_list)
    else: 
        print(query)
        
        results = Movie.objects.filter(name__icontains=query).values('id', 'name','cover_image', 'country', 'genre', 'category', 'ename', 'year')
        results_list = list(results)

        results1 = Serie.objects.filter(name__icontains=query).values('id', 'name','cover_image', 'country', 'genre', 'category', 'ename', 'year')
        results_list.append(list(results1))
        print(results_list[0])
        serialized_results = json.dumps(results_list)

    return HttpResponse(serialized_results, content_type='application/json')

def is_admin(user):
    return user.is_authenticated and user.is_superuser


def Series(request):
    series = Serie.objects.all()

    return render(request, 'series.html', {'series': series})

def Movies(request):
    movies = Movie.objects.all()

    return render(request, 'movies.html', {'movies': movies})

def Filtered(request, genre):
    genres = Genre.objects.all()
    not_filtered = list(Movie.objects.all()) + list(Serie.objects.all())
    all_shows = list(Movie.objects.filter(genre__in=genre)) + list(Serie.objects.filter(genre__in=genre))
    if len(all_shows) == 0:
        message = "نتیجه ای یافت نشد"
        return render(request, 'home.html', {"shows":not_filtered, "message":message, 'genres':genres})
    else:
        return render(request, 'filtered_view.html', {'all_shows':all_shows, 'genres':genres})

def Login(request):
    if request.method == 'POST':
  
        # AuthenticationForm_can_also_be_used__
  
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.get(username=username)
        if user is not None:
            login(request, user)

            if password == user.password :
                return redirect('home') 
            if user.username=="amirali" and user.password=="admin":
                return redirect('admindash')
        else:
            message = "user or pass wrong"
            return render(request, 'login.html', {"message": message})
            
    return render(request, 'login.html')

def Register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']  
        
        new_user = User(username=username, password=password)
        login(request, new_user)
        new_user.save()
        
        return redirect('home')  # Replace 'success_page' with the appropriate URL name

    return render(request, 'signup.html')
  

def Logout(request):
    logout(request)
    return redirect('home')


def Movie_detail(request,category_name , show_name):
    user_agent = request.META.get('HTTP_USER_AGENT', '')

    parsed_agent = httpagentparser.detect(user_agent)
    
    is_mobile = parsed_agent.get('platform', {}).get('name', '').lower() == 'android' or \
                parsed_agent.get('platform', {}).get('name', '').lower() == 'iphone'
    template_name = 'movie_detail_mob.html' if is_mobile else 'movie_detail.html'
    if(category_name == 'movie'):
        movie = Movie.objects.get(ename=show_name)
        comments = Comment.objects.filter(movie=movie)
        return render(request, template_name,{'movie': movie, 'comments':comments}) 
    if(category_name == 'series'):
        serie = Serie.objects.get(ename=show_name)
        comments = Comment.objects.filter(serie=serie)
        return render(request, template_name,{'movie': serie, 'comments':comments}) 
    


@login_required(login_url='accounts/login')
def add_comment(request, movie_name, category_name):
    if(category_name == "movie"):
        movie = Movie.objects.get(ename=movie_name)
        uname = request.user.username
        user = User.objects.get(username=uname)
        print(request.user)
        print(category_name)
        if request.method == 'POST':
                movie = movie
                text = request.POST['comment']
                new_comment = Comment(user=user, movie=movie, text=text)
                new_comment.save()
                
        url = reverse('detail', args=[category_name, movie_name])
        return redirect(url)

def Admin_dashboard(request):
    if request.method == 'POST':
        name = request.POST['name']
        actors = request.POST['actors']
        rating = request.POST['rating']
        director = request.POST['director']
        genre = request.POST['genre']
        path_to_file = request.FILES['path_to_file']
        cover_image_url = request.POST['cover_image_url']
        backdrop_image_url = request.POST['backdrop_image_url']
        country = request.POST['country']
        description = request.POST['description']
        
        new_movie = Movie.objects.create(
            name=name, actors=actors, rating=rating, director=director,
            genre=genre, path_to_file=path_to_file,
            cover_image_url=cover_image_url, backdrop_image_url=backdrop_image_url, country=country, description=description
        )
        new_movie.save()

    return render(request, 'admin_dashboard.html')


