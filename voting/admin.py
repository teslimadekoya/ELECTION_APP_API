from django.contrib import admin
from .models import Vote

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['voter', 'candidate', 'election', 'timestamp']
    list_filter = ['election', 'candidate']
    search_fields = ['voter__username', 'candidate__name', 'election__name']
