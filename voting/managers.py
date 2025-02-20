from django.db import models

class VoteManager(models.Manager):
    def get_votes_for_candidate_in_election(self, candidate, election):
        return self.filter(candidate=candidate, election=election).count()

    def get_user_vote_for_election(self, user, election):
        return self.filter(voter=user, election=election).first()  # Returns the vote if exists

# Now you can use this manager in the Vote model
