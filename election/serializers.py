from rest_framework import serializers
from .models import Election, Candidate

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['id', 'candidate_name', 'candidate_party', 'votes']

class ElectionSerializer(serializers.ModelSerializer):
    candidates = CandidateSerializer(many=True, read_only=True)

    class Meta:
        model = Election
        fields = ['id', 'election_type', 'start_date', 'end_date', 'election_status', 'candidates']
