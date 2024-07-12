import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BlogPost(models.Model):
    CONTENT_TYPE_CHOICES = [
        ("blog", "Blog Content"),
        ("linkedin", "LinkedIn Content"),
        ("tweet", "Tweet Content"),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    youtube_title = models.CharField(max_length=300)
    youtube_url = models.URLField()
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES, default="blog")
    generated_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'youtube_title', 'content_type'], name='unique_user_youtube_content')
        ]
    
    def __str__(self):
        return self.youtube_title
