from django.db import models

# Create your models here.
# {
#       "url": "https://example.com/article123",
#       "title": "Breaking News: Global Economy Update",
#       "snippet": "The global economy is facing new challenges...",
#       "domain": "bbc.com",
#       "socialimage": "https://example.com/news-image.jpg",
#       "language": "English",
#       "seendate": "20250323T120000Z"
#     },

class GDLETNewsModel(models.Model):
    url = models.CharField(max_length=400, blank=True)
    title=models.CharField(max_length=400, blank=True)
    summary=models.TextField(null=True, blank=True)
    domain=models.URLField(blank=True)
    socialimage=models.URLField(blank=True)
    language=models.CharField(max_length=250)
    sourcecountry=models.CharField(max_length=250, blank=True)
    #sentiment_analysis = models.CharField(max_length=200, blank=True)
    seendate=models.DateTimeField()

    class Meta:
        ordering = ('-seendate',)

    def __str__(self):
        return f"{self.title}, {self.url}"



