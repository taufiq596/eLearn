from django.urls import path 
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path('login/', views.userlogin, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.userlogout, name='logout'),
    path('blog/', views.blog, name='blog'),
    path('blog/<str:slug>/', views.blogpost),
    path('addpost/', views.addpost, name='addpost'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('update/<int:id>/', views.update, name='update'),
    path('comment/', views.comment, name='comment'),
    path('profile/<username>/', views.viewprofile, name='profile'),
    path('editprofile/<int:id>/', views.editProfile, name='editprofile'),
    path('changepassword/<int:id>/', views.changePassword, name='changepassword'),
    path('search/', views.search, name='search'),
    
]
