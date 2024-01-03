from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVectorField,SearchVector
# Create your models here.

class Note(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    title = models.CharField(max_length = 200)
    content = models.TextField()
    shared_with = models.ManyToManyField(User,related_name="shared_notes",blank=True,null=True)

    # Added a SearchVectorField for text indexing
    search_vector = SearchVectorField(null=True, blank=True)
    def save(self, *args, **kwargs):
        # Update the SearchVectorField whenever the model is saved
        self.search_vector = SearchVector('content')
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.title}"

    