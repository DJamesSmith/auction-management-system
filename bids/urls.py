from django.urls import path
from . import views


urlpatterns = [
    path("place/<int:auction_id>/", views.place_bid, name="place_bid"),
    path("history/", views.bid_history, name="bid_history"),
    path("history/delete/<int:bid_id>/", views.delete_bid, name="delete_bid"),
    path("history/delete-all/", views.delete_all_bid_history, name="delete_all_bid_history"),
]