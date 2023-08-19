from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.Home, name='home'),
    path('/series', views.Series, name="series"),
    path('/movies', views.Movies, name="movies"),
    path('filtered/<str:genre>', views.Filtered, name="genre"),
    path('accounts/login/', views.Login, name='login'),
    path('accounts/signup/', views.Register, name='signup'),
    path('accounts/logout/', views.Logout, name='logout'),
    path('detail/<str:category_name>/<str:show_name>/', views.Movie_detail, name='detail'),
    path('<str:category_name>/<str:movie_name>/add_comment/', views.add_comment, name='add_comment'),
    path('admindash/', views.Admin_dashboard, name='admin-dashboard'),
    path('search/', views.search_movies, name='search_movies'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)