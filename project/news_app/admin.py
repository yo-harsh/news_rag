from django.contrib import admin
from .models import NewsLinks

# Register your models here.
class NewsLinksAdmin(admin.ModelAdmin):
    # Define the list of fields to display in the admin list view
    list_display = ('id', 'link', 'text', 'created_at')

    # Make the 'created_at' field clickable for sorting
    list_display_links = ('created_at',)

# Register the NewsLinks model with its corresponding admin class
admin.site.register(NewsLinks, NewsLinksAdmin)