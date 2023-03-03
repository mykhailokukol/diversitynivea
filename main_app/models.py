from django.db import models


class DataModel(models.Model):
    """  """
    
    title = models.CharField(max_length=512, null=True, blank=True)
    streamer = models.CharField(max_length=512, null=True, blank=True)
    createdAt = models.CharField(max_length=512, null=True, blank=True, unique=True)
    logUrl = models.CharField(max_length=512, null=True, blank=True)
    websiteUrl = models.CharField(max_length=512, null=True, blank=True)
    rating = models.CharField(max_length=512, null=True, blank=True)
    streamsNumber = models.CharField(max_length=512, null=True, blank=True)
    isStreamMade = models.CharField(max_length=512, null=True, blank=True)
    duration = models.CharField(max_length=512, null=True, blank=True)
    
    date_uploaded = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return str(self.date_uploaded)
