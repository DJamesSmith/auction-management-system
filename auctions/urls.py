from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_auction, name='create_auction'),
    path('my-auctions/', views.my_auctions, name='my_auctions'),
    path('edit-auction/<int:auction_id>/',views.edit_auction,name='edit_auction'),
    path(
        'cancel-auction/<int:auction_id>/',
        views.cancel_auction,
        name='cancel_auction'
    ),
]