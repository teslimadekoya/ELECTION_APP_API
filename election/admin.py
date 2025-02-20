from django.contrib import admin
from .models import Election, Candidate

admin.site.site_header = "Election App"

class CandidateInline(admin.TabularInline):
    model = Candidate
    extra = 3

    def get_readonly_fields(self, request, obj=None):
        return ['votes']

class ElectionAdmin(admin.ModelAdmin):
    list_display = ('id','election_type', 'election_status', 'start_date', 'end_date')

    fieldsets = [
        (None, {'fields': ['election_type']}),
        ('Date Information', {'fields': ['start_date', 'end_date'], 'classes': ['collapse']}),
    ]
    inlines = [CandidateInline]

class CandidateAdmin(admin.ModelAdmin):
    list_display = ('candidate_name', 'candidate_party', 'votes')

    def get_readonly_fields(self, request, obj=None):
        return ['votes']

    exclude = ['votes']

admin.site.register(Election, ElectionAdmin)
admin.site.register(Candidate, CandidateAdmin)
