from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):  # This is A Enumeration class
        """
        We can get human-readable : Post.Status.labels
        and value in database : Post.Status.values
        """

        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="blog_posts",  # user.blog_posts
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(
        auto_now_add=True,
    )  # auto_now_add -> when create object
    updated = models.DateTimeField(auto_now=True)  # auto_now -> when update object
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    objects = models.Manager()
    published = PublishedManager() # our custom manager.

    class Meta:
        ordering = ["-publish"]
        indexes = [models.Index(fields=["-publish"])]  # is not support in MySQL

    def __str__(self):
        return f"{self.title}"
