from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from social.models import Profile, Post, Comment, Like, Follow
from django.core.files.uploadedfile import SimpleUploadedFile
import urllib.request
import random
import time

class Command(BaseCommand):
    help = 'Seeds the database with dynamic demo users, varied posts, and organic interactions for NOIR.'

    def get_real_image(self, filename, width=800, height=1000, category=""):
        url = f"https://picsum.photos/{width}/{height}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req)
        content = response.read()
        return SimpleUploadedFile(filename, content, content_type="image/jpeg")

    def handle(self, *args, **kwargs):
        self.stdout.write("Clearing existing data...")
        User.objects.filter(is_superuser=False).delete()
        Post.objects.all().delete()
        
        users_data = [
            {'username': 'alexmorrow', 'display_name': 'Alex Morrow', 'bio': 'Visual Designer', 'email': 'alex@noir.com'},
            {'username': 'mayachen', 'display_name': 'Maya Chen', 'bio': 'Photographer', 'email': 'maya@noir.com'},
            {'username': 'leohart', 'display_name': 'Leo Hart', 'bio': 'Architect', 'email': 'leo@noir.com'},
            {'username': 'noahvale', 'display_name': 'Noah Vale', 'bio': 'Filmmaker', 'email': 'noah@noir.com'},
            {'username': 'irisstone', 'display_name': 'Iris Stone', 'bio': 'Art Director', 'email': 'iris@noir.com'},
        ]
        
        users = []
        for data in users_data:
            user = User.objects.create_user(username=data['username'], email=data['email'], password='password123')
            user.profile.display_name = data['display_name']
            user.profile.bio = data['bio']
            try:
                user.profile.avatar = self.get_real_image(f"avatar_{user.username}.jpg", 400, 400)
                user.profile.save()
            except Exception as e:
                self.stdout.write(f"Could not fetch avatar for {user.username}: {e}")
                user.profile.save()
            users.append(user)
            self.stdout.write(f"Created user: {user.username}")

        # Follow logic
        for user in users:
            for other_user in users:
                if user != other_user and random.choice([True, False]):
                    Follow.objects.create(follower=user, following=other_user)

        captions = [
            "Morning light across the studio.",
            "Concrete, glass, and a little silence.",
            "Shot on a rainy Tuesday.",
            "An experiment in negative space.",
            "Visual exploration.",
            "Distant horizons.",
            "Geometric harmony in architecture.",
            "The spaces in between.",
            "Finding balance.",
            "A study of contrast and form.",
            "Monochrome daydreams.",
            "Structural integrity.",
            "Chasing shadows.",
            "Minimalist tendencies.",
            "The art of simplicity."
        ]
        
        comments_pool = [
            "Incredible work.", "Love the lighting here.", "Stunning.", 
            "The composition is perfect.", "Beautiful tones.", "Masterpiece.", 
            "Inspiring as always.", "Can't stop looking at this.", 
            "Where was this taken?", "Absolutely flawless."
        ]
        
        # Generate 20 posts
        for i in range(20):
            author = random.choice(users)
            try:
                width = random.choice([800, 1000, 1200])
                height = random.choice([800, 1000, 1200])
                image_file = self.get_real_image(f"post_{i}.jpg", width, height)
            except Exception as e:
                self.stdout.write(f"Could not fetch post image {i}: {e}")
                continue
                
            post = Post.objects.create(
                author=author,
                caption=random.choice(captions),
                location=random.choice(["Studio", "Tokyo", "London", "New York", "Paris", "Berlin", ""]),
                image=image_file
            )
            self.stdout.write(f"Created post {i+1} for {author.username}")
            
            # Add random likes (0 to 4)
            likers = random.sample(users, random.randint(0, 4))
            for liker in likers:
                Like.objects.create(user=liker, post=post)
                
            # Add random comments (0 to 5)
            for _ in range(random.randint(0, 5)):
                commenter = random.choice(users)
                Comment.objects.create(author=commenter, post=post, content=random.choice(comments_pool))

        self.stdout.write(self.style.SUCCESS("Database seeded dynamically with 20+ posts!"))
