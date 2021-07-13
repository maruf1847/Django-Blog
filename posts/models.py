from tinymce import HTMLField
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User



class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return self.user.username


# from PIL import Image
# for profile picture size
# def save(self, **kwargs):
#     super().save()
#
#     img = Image.open(self.profile_picture.path)
#
#     if img.height > 300 or img.width > 400:
#         output_size = (300, 300)
#         img.thumbnail(output_size)
#         img.save(self.image.path)


class Category(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Post(models.Model):
    objects = None
    title = models.CharField(max_length=100)
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    content = HTMLField()
    comment_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to="thumbnail_pics")
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField()
    previous_post = models.ForeignKey('self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey('self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'id': self.id})
