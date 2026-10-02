from django.urls import path
from . import views


urlpatterns = [
    path("place/<int:auction_id>/", views.place_bid, name="place_bid"),
]
