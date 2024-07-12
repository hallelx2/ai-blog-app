# myapp/management/commands/populate_uuid.py

from django.core.management.base import BaseCommand
from blog_creator.models import BlogPost
import uuid

class Command(BaseCommand):
    help = 'Populate UUID field for existing BlogPost records'

    def handle(self, *args, **kwargs):
        posts_without_uuid = BlogPost.objects.filter(uuid__isnull=True)
        for post in posts_without_uuid:
            post.uuid = uuid.uuid4()
            post.save()
        self.stdout.write(self.style.SUCCESS('Successfully populated UUID field for existing BlogPost records'))
