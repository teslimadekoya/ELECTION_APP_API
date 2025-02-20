from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Vote
from election.models import Candidate, Election
from .serializers import VoteSerializer
from users.permissions import IsAdmin,IsVoter, IsBoth
# Existing Vote views...


class CastVoteView(APIView):
    permission_classes = [IsAuthenticated]


    def post(self, request):
        serializer = VoteSerializer(data=request.data)
        
        if serializer.is_valid():
            election_id = serializer.validated_data['election']
            candidate_id = serializer.validated_data['candidate']

            if election_id == candidate_id:
                return Response({'error': 'You cannot vote for yourself'}, status=status.HTTP_400_BAD_REQUEST)

            if Vote.objects.filter(voter=request.user, election_id=election_id).exists():
                return Response({'error': 'You have already voted'}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save(voter=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VoteListView(APIView):
    # permission_classes = [IsAdmin]  # No authentication required for viewing election list

    def get(self, request):
        vote = Vote.objects.all()
        serializer = VoteSerializer(vote, many=True)
        return Response(serializer.data)
    
class VoteDetailView(APIView):
    def get(self, request, id):
        vote = get_object_or_404(Vote, id=id)
        serializer = VoteSerializer(vote)
        return Response(serializer.data)

    def delete(self, request, id):
        vote = get_object_or_404(Vote, id=id)
        vote.delete()
        return Response({'message': 'Vote has been deleted'}, status=status.HTTP_204_NO_CONTENT)


# POST /elections/<id>/results/: Publish results of an election (Admin only)
# GET /elections/<id>/results/: View results of an election (Open to voters and admin)
class ElectionResultView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdmin()]
        return [IsBoth()]

    def post(self, request, election_id):
        # Only admins can publish results
        if not request.user.is_staff:
            return Response({"error": "Permission denied. Only admins can publish results."}, status=status.HTTP_403_FORBIDDEN)

        election = get_object_or_404(Election, id=election_id)

        # Calculate results
        candidates = election.candidates.all()
        results = {candidate.candidate_name: Vote.objects.get_votes_for_candidate_in_election(candidate, election) for candidate in candidates}

        return Response({"election": election.election_type, "results": results, "status": "Published"}, status=status.HTTP_201_CREATED)

    def get(self, request, election_id):
        election = get_object_or_404(Election, id=election_id)

        # Fetch vote counts
        candidates = election.candidates.all()
        results = {candidate.candidate_name: Vote.objects.get_votes_for_candidate_in_election(candidate, election) for candidate in candidates}

        return Response({"election": election.election_type, "results": results}, status=status.HTTP_200_OK)
