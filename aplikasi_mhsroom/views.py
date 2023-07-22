from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Post, Comment, Profile
from django.contrib.auth.models import User
from .forms import ProfileForm, PostForm, CommentForm
from datetime import datetime, timezone, timedelta
import locale
import re

def index(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    return render(request, 'profile.html', {'user': user, 'profile': profile})

@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')  # Redirect ke halaman login setelah logout

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the User object

            # Create a new Profile object and associate it with the user
            profile = Profile.objects.create(user=user)

            # You can add additional fields to the Profile model and set them here

            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def home(request):
    # Mengambil semua postingan dari seluruh pengguna dan mengurutkannya berdasarkan tanggal pembuatan
    all_posts = Post.objects.all().order_by('-created_at')

    # Mengambil semua komentar dari postingan pengguna dan teman-temannya
    comments = Comment.objects.filter(post__in=all_posts)

    # Ubah format waktu untuk setiap postingan
    for post in all_posts:
        post.created_at = convert_to_indonesian_time(post.created_at)

    return render(request, 'home.html', {'user': request.user, 'all_posts': all_posts, 'comments': comments})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

def detail_post(request, post_id):
    # Mengambil postingan berdasarkan ID
    post = get_object_or_404(Post, id=post_id)

    # Mengambil semua komentar untuk postingan ini
    comments = Comment.objects.filter(post=post)

    return render(request, 'detail_post.html', {'post': post, 'comments': comments})

@login_required
def create_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()

            return redirect("home")

    else:
        form = CommentForm()

    return render(request, "home.html", {"form": form})

@login_required
def add_friend(request, friend_id):
    friend = User.objects.get(id=friend_id)
    if friend != request.user:
        profile = Profile.objects.get(user=request.user)
        profile.friends.add(friend)
    return redirect('home')

def convert_to_indonesian_time(utc_time):
    # Buat selisih waktu dengan Waktu Indonesia (UTC+7)
    from_zone = timezone.utc
    to_zone = timezone(timedelta(hours=7))

    # Konversi waktu ke Waktu Indonesia
    indonesian_time = utc_time.replace(tzinfo=from_zone).astimezone(to_zone)

    # Set locale ke bahasa Indonesia
    locale.setlocale(locale.LC_TIME, 'id_ID')

    # Format waktu dalam format yang diinginkan (21 Juli 2023, 23:49 WIB)
    return indonesian_time.strftime('%d %B %Y, %H:%M WIB')