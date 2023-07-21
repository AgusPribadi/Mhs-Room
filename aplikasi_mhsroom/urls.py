from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('create_post/', views.create_post, name='create_post'),
    path('post/<int:post_id>/', views.detail_post, name='detail_post'),
    path('create_comment/<int:post_id>/', views.create_comment, name='create_comment'),
    path('add_friend/<int:friend_id>/', views.add_friend, name='add_friend'),
]
