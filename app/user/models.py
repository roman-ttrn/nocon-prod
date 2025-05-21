from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    contributor_points = models.PositiveIntegerField(default=0)

    @property
    def status(self):
        if self.contributor_points >= 120:
            return "Надежда (андреевна)"
        elif self.contributor_points >= 80:
            return "Мактрахер"
        elif self.contributor_points >= 50:
            return "Мазафакер"
        elif self.contributor_points >= 20:
            return "Свой"
        elif self.contributor_points >= 10:
            return "Осваивается"
        else:
            return "Недавно прибыл"
        
    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return static('user/images/default.jpg')  # static путь
    
    def __str__(self):
        return self.user.username
    
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='posts/', blank=True)  # <-- ВАЖНО
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    class Meta:
        ordering = ['-created_at']

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"Post by {self.author.username} at {self.created_at}"
