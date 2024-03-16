from django.db import models

# Create your models here.
class NewsLinks(models.Model):
    id = models.AutoField(primary_key=True)
    link = models.URLField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Specify the custom table name
        db_table = 'news_data'

    def __str__(self):
        return f"Entry: {self.link}"