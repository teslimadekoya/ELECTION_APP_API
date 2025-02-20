from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Election, Candidate
from .serializers import ElectionSerializer, CandidateSerializer
from users.permissions import IsAdmin, IsVoter

# GET /elections/: View a list of all elections
class ElectionListView(APIView):
    permission_classes = [IsAdmin]  # No authentication required for viewing election list

    def get(self, request):
        elections = Election.objects.all().order_by('-start_date')
        serializer = ElectionSerializer(elections, many=True)
        return Response(serializer.data)

# POST /elections/: Create a new election (admin only)
class ElectionCreateView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request):
        # Ensure the user is an admin
        if not request.user.is_staff:
            return Response({"error": "Permission denied. Only admins can create elections."}, status=status.HTTP_403_FORBIDDEN)

        serializer = ElectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# GET /elections/<id>/: View detailed information about a specific election (voter or admin)
class ElectionDetailView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request, election_id):
        election = get_object_or_404(Election, pk=election_id)
        serializer = ElectionSerializer(election)
        return Response(serializer.data)

# PATCH /elections/<id>/: Update election details (admin only)
class ElectionUpdateView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def patch(self, request, election_id):
        # Ensure the user is an admin
        if not request.user.is_staff:
            return Response({"error": "Permission denied. Only admins can update elections."}, status=status.HTTP_403_FORBIDDEN)

        election = get_object_or_404(Election, pk=election_id)
        serializer = ElectionSerializer(election, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# DELETE /elections/<id>/: Delete an election (admin only)
class ElectionDeleteView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def delete(self, request, election_id):
        # Ensure the user is an admin
        if not request.user.is_staff:
            return Response({"error": "Permission denied. Only admins can delete elections."}, status=status.HTTP_403_FORBIDDEN)

        election = get_object_or_404(Election, pk=election_id)
        election.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# POST /elections/<id>/candidates/: Add candidates to an election (admin only)
class CandidateCreateView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request, election_id):
        # Ensure the user is an admin
        if not request.user.is_staff:
            return Response({"error": "Permission denied. Only admins can add candidates."}, status=status.HTTP_403_FORBIDDEN)

        election = get_object_or_404(Election, pk=election_id)
        candidate_data = request.data
        candidate_data['election'] = election.id
        serializer = CandidateSerializer(data=candidate_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# GET /elections/<id>/candidates/: View candidates in an election (open to everyone)
class CandidateListView(APIView):
    permission_classes = []  # No authentication required for viewing candidates

    def get(self, request, pk):
        candidate = Candidate.objects.all()
        serializer = CandidateSerializer(candidate, many= True)
        return Response (serializer.data, status=status.HTTP_200_OK)
