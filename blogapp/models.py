from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now=True)
    content = RichTextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='post_likes')
    read_status = models.ManyToManyField(User, related_name='post_read_status')
    subscriptions = models.ManyToManyField(User, related_name='post_subscriptions')

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title + ' by ' + str(self.author)

    def save(self,  *args, **kwargs):
        self.slug = slugify(self.title)
        return super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.id])


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    following = models.ManyToManyField(User, related_name='following')
    followers = models.ManyToManyField(User, related_name='followers')
