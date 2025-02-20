from rest_framework import serializers
from .models import Vote
from election.models import Candidate, Election


class VoteSerializer(serializers.ModelSerializer):
    voter = serializers.StringRelatedField(read_only=True)  # Always display voter's name
    candidate = serializers.PrimaryKeyRelatedField(queryset=Candidate.objects.all(), write_only=True)
    election = serializers.PrimaryKeyRelatedField(queryset=Election.objects.all(), write_only=True)
    candidate_name = serializers.CharField(source='candidate.candidate_name', read_only=True)  
    election_name = serializers.CharField(source='election.election_type', read_only=True)

    class Meta:
        model = Vote
        fields = ['id', 'voter', 'candidate', 'election', 'candidate_name', 'election_name', 'timestamp']

