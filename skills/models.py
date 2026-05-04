from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# OOP ideas we used in class: encapsulation (models hide DB details),
# inheritance (Django model base classes), and string representation below.

class Category(models.Model):
    """Groups skills so people can browse by topic (Programming, Cooking, etc.)."""
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class SkillListing(models.Model):
    """One post: what I teach, written by a logged-in user."""
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # reverse() builds the URL for the detail page from the route name
        return reverse('skill-detail', kwargs={'pk': self.pk})
