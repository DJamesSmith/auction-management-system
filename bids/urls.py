from django.urls import path
from . import views


urlpatterns = [
    path("place/<int:auction_id>/", views.place_bid, name="place_bid"),
    path("history/", views.bid_history, name="bid_history"),
]
