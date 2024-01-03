from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVectorField,SearchVector
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    shared_with = models.ManyToManyField(User, related_name="shared_notes", blank=True)
    
    # Add a SearchVectorField for text indexing
    search_vector = SearchVectorField(null=True, blank=True)

    def __str__(self):
        return f"{self.title}"

@receiver(post_save, sender=Note)
def update_search_vector(sender, instance, **kwargs):
    # Update the SearchVectorField after the instance has been saved
    Note.objects.filter(pk=instance.pk).update(search_vector=SearchVector('title', 'content'))



    