from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

import json

from .models import BlogPost
from .helpers import get_blog_content, youtube_title, get_youtube_or_audio_transcription

@login_required()
def index(request):
    return render(request, "index.html")

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            error_message = "Invalid username or password"
            return render(request, "login.html", {'error_message': error_message})
    return render(request, "login.html")

@csrf_exempt
@login_required
def generate_blog(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            youtube_link = data["link"]
            content_type = data["type"]
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({"error": "Invalid data sent"}, status=400)

        # Get video title
        title = youtube_title(youtube_link)
        if not title:
            return JsonResponse({"error": "Error getting video title"}, status=500)

        # Check if the blog post already exists for the given user and content type
        if BlogPost.objects.filter(user=request.user, youtube_title=title, content_type=content_type).exists():
            return JsonResponse({"error": f"Blog Post for this video already exists for the selected content type."}, status=400)

        # Proceed to generate and save the blog post
        transcript = get_youtube_or_audio_transcription(youtube_link)
        if not transcript:
            return JsonResponse({"error": "Error getting transcript"}, status=500)

        blog_content = get_blog_content(transcript, content_type)
        if not blog_content:
            return JsonResponse({"error": "Error generating blog content"}, status=500)

        new_blog_article = BlogPost.objects.create(
            user=request.user,
            youtube_title=title,
            youtube_url=youtube_link,
            content_type=content_type,
            generated_content=blog_content
        )
        new_blog_article.save()

        return JsonResponse({"content": blog_content}, status=200)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

    

def blog_list(request):
    blog_articles = BlogPost.objects.filter(user=request.user).order_by("content_type", "-created_at")
    return render(request, "blogs.html", {"blog_articles": blog_articles})

def blog_article_by_id(request, pk):
    blog_article = BlogPost.objects.get(id=pk)
    if blog_article and blog_article.user == request.user:
        return render(request, "details.html", {"blog_article": blog_article})
    return redirect("/")

@login_required
def delete_blog(request, pk):
    blog_article = get_object_or_404(BlogPost, id=pk)
    
    if blog_article.user == request.user:
        blog_article.delete()
        return redirect("/blog-list")
    
    return redirect("/")
    
def user_signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        repeatPassword = request.POST["repeatPassword"]
        
        if password == repeatPassword:
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                login(request, user)
                return redirect("/")
            except:
                error_message = "Error creating account"
                return render(request, "signup.html", {"error_message": error_message})
        else:
            error_message = "Password Do not Match"
            return render(request, "signup.html", {"error_message": error_message})
    
    return render(request, "signup.html")

def user_logout(request):
    logout(request)
    return redirect("/")
