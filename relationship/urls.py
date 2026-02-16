from django.urls import path
from relationship.views import IncomingLikesView, OutgoingLikesView, MatchesView, LikeView, CommentLikeView

urlpatterns = [
    path("incoming/", IncomingLikesView.as_view(), name="relationship-incoming"),
    path("outgoing/", OutgoingLikesView.as_view(), name="relationship-outgoing"),
    path("matches/", MatchesView.as_view(), name="relationship-matches"),
    path("like/", LikeView.as_view(), name="relationship-like"),
    path("comment-like/", CommentLikeView.as_view(), name="relationship-comment-like"),
]
