from django.db import models
from django.conf import settings
from election.models import Election, Candidate

class VoteManager(models.Manager):
    def get_user_vote_for_election(self, user, election_id):
        """Check if a user has already voted in the specified election."""
        return self.filter(voter=user, election_id=election_id).first()

    def get_votes_for_candidate_in_election(self, candidate, election):
        """Count the votes for a specific candidate in a specific election."""
        return self.filter(candidate=candidate, election=election).count()

class Vote(models.Model):
    voter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Linking to the custom user model
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = VoteManager()

    def __str__(self):
        return f"{self.voter} voted for {self.candidate} in {self.election}"

    class Meta:
        unique_together = ('voter', 'election')  # Ensures a user can only vote once per election
