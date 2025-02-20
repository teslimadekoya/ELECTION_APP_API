from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Election(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ]

    election_type = models.CharField(max_length=1000, unique=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    election_status = models.CharField(max_length=9, choices=STATUS_CHOICES, blank=False, null=False, default='upcoming')

    def __str__(self):
        return self.election_type
    
    def is_upcoming(self):
        return self.election_status == 'upcoming'
    
    def is_ongoing(self):
        return self.election_status == 'ongoing'
    
    def is_completed(self):
        return self.election_status == 'completed'
    
    def save(self, *args, **kwargs):
        current_time = timezone.now()

        if self.start_date > current_time:
            self.election_status = 'upcoming'
        elif self.end_date and self.end_date < current_time:
            self.election_status = 'completed'
        elif self.start_date <= current_time <= self.end_date:
            self.election_status = 'ongoing'
        
        super().save(*args, **kwargs)

class Candidate(models.Model):
    candidate_name = models.CharField(max_length=1000)
    candidate_party = models.CharField(max_length=255)
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='candidates', null=True)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.candidate_name

    def update_vote_count(self):
        from voting.models import Vote
        self.votes = Vote.objects.filter(candidate=self).count()
        self.save()

from django.db.models.signals import post_save
from django.dispatch import receiver
from voting.models import Vote

@receiver(post_save, sender=Vote)
def update_candidate_votes(sender, instance, **kwargs):
    instance.candidate.update_vote_count()
