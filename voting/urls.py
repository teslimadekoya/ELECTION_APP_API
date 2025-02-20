from django.urls import path
from .views import ElectionResultView, CastVoteView, VoteListView,VoteDetailView

urlpatterns = [
    path('elections/votes/', VoteListView.as_view(), name= 'votes'),
    path('elections/votes/<int:id>/', VoteDetailView.as_view(), name='vote-detail'),
    path('elections/voting/', CastVoteView.as_view(), name='voting'),
    path('elections/<int:election_id>/results/', ElectionResultView.as_view(), name='election-results'),  # Added this
]
