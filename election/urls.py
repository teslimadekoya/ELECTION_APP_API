from django.urls import path
from .views import (
    ElectionCreateView,
    ElectionListView,
    ElectionDetailView,
    ElectionUpdateView,
    ElectionDeleteView,
    CandidateCreateView,
    CandidateListView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Token authentication routes
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Election related URLs
    path('elections/', ElectionListView.as_view(), name='election-list'),
    path('elections/create/', ElectionCreateView.as_view(), name='election-create'),
    path('elections/<int:election_id>/', ElectionDetailView.as_view(), name='election-detail'),
    path('elections/<int:election_id>/update/', ElectionUpdateView.as_view(), name='election-update'),
    path('elections/<int:election_id>/delete/', ElectionDeleteView.as_view(), name='election-delete'),

    # Candidate related URLs
    path('elections/<int:pk>/candidates/list/', CandidateListView.as_view(), name='candidate-list'),
    path('elections/<int:election_id>/candidates/create/', CandidateCreateView.as_view(), name='candidate-create'),
]
