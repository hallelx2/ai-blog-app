import os
from pytube import YouTube, extract
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
from django.conf import settings
import assemblyai as aai

GOOGLE_API_KEY = settings.GOOGLE_API_KEY
ASSEMBLY_AI_API_KEY = settings.ASSEMBLY_AI_API_KEY

aai.settings.api_key = ASSEMBLY_AI_API_KEY
genai.configure(api_key=GOOGLE_API_KEY)


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

def get_blog_content(transcript, content_type):
    if content_type == "blog":
        prompt = f"Generate a blog post based on this transcript: {transcript}"
    elif content_type == "linkedin":
        prompt = f"Generate a LinkedIn post based on this transcript: {transcript}"
    elif content_type == "tweet":
        prompt = f"Generate a tweet based on this transcript: {transcript}"
    else:
        return None
    
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text