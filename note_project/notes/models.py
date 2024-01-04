from django.contrib.auth.models import User
from typing import Any
from django.db import models
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
class Note(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    shared_with = models.ManyToManyField(User, related_name='shared_notes', blank=True)

    # # Add a search vector field
    # search_vector = SearchVectorField(null=True, editable=False)

    # def save(self, *args, **kwargs):
    #     # Update search_vector on save
    #     self.search_vector = SearchVector('title', 'content')
    #     super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.owner.username + " " + str(self.owner.id) + " - " + self.title
