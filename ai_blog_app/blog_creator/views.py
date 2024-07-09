from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import get_object_or_404

import json
import os

from pytube import YouTube, extract
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
import assemblyai as aai

import google.generativeai as genai

from .models import BlogPost

### Helper Functions

GOOGLE_API_KEY = settings.GOOGLE_API_KEY
ASSEMBLY_AI_API_KEY = settings.ASSEMBLY_AI_API_KEY

aai.settings.api_key = ASSEMBLY_AI_API_KEY
genai.configure(api_key=GOOGLE_API_KEY)

# Function to get the youtube title
def youtube_title(video_url):
    try:
        video = YouTube(video_url)
        title = video.title
        return title
    except Exception as e:
        print(f"Error getting video title: {e}")
        return None

def get_video_id(url):
    try:
        video_id = extract.video_id(url)
        return video_id
    except Exception as e:
        print(f"Error extracting video ID: {e}")
        return None

def get_transcript(link):
    try:
        id = get_video_id(link)
        if not id:
            return None
        transcript_json = YouTubeTranscriptApi.get_transcript(id)
        transcript = ""
        for text in transcript_json:
            transcript += text['text']
        return transcript
    except (NoTranscriptFound, TranscriptsDisabled):
        return None

def download_audio(link):
    try:
        yt = YouTube(link)
        audio_file = yt.streams.filter(only_audio=True).first()
        audio_file_output = audio_file.download(output_path=settings.MEDIA_ROOT)
        base, _ = os.path.splitext(audio_file_output)
        
        new_file = base + ".mp3"
        os.rename(audio_file_output, new_file)
        return new_file
    except Exception as e:
        print(f"Error downloading audio: {e}")
        return None

def get_transcript_from_audio(link):
    audio_file = download_audio(link)
    if audio_file:
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_file)
        os.remove(audio_file)  # Delete the audio file after transcription
        return transcript.text
    else:
        return None

def get_youtube_or_audio_transcription(link):
    transcript = get_transcript(link)
    if not transcript:
        transcript = get_transcript_from_audio(link)
    return transcript

def get_blog_content(transcript):
    prompt = f"Generate a blog post for me based on the content of what is discussed in this youtube video's transcript: {transcript}"
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text

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
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({"error": "Invalid data sent"}, status=400)
        
        # Get video title
        title = youtube_title(youtube_link)
        if not title:
            return JsonResponse({"error": "Error getting video title"}, status=500)
        
        # Get the transcript
        transcript = get_youtube_or_audio_transcription(youtube_link)
        if not transcript:
            return JsonResponse({"error": "Error getting transcript"}, status=500)
        
        # Generate the blog content using Gemini
        blog_content = get_blog_content(transcript)
        if not blog_content:
            return JsonResponse({"error": "Error generating blog content"}, status=500)
        
        # Save blog to the database
        new_blog_article = BlogPost.objects.create(
            user=request.user,
            youtube_title=title,
            youtube_url=youtube_link,
            generated_content=transcript
        )
        new_blog_article.save()
        
        # Return the blog article
        return JsonResponse({"content": blog_content}, status=200)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
    

def blog_list(request):
    blog_articles = BlogPost.objects.filter(user=request.user)
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
