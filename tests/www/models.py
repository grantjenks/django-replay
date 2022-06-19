from django.db import models


class Essay(models.Model):
    publish_date = models.DateTimeField(blank=True, null=True)
    title = models.CharField(max_length=100)
    text = models.TextField()

    def __str__(self):
        return self.title


class Comment(models.Model):
    essay = models.ForeignKey(Essay)
    name = models.CharField(max_length=100)
    website = models.URLField(blank=True)
    email = models.EmailField()
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
