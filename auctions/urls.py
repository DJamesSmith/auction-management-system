<<<<<<< HEAD
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_auction, name='create_auction'),
    path('my-auctions/', views.my_auctions, name='my_auctions'),
    path('live-auctions/', views.live_auctions, name='live_auctions'),
    path('edit-auction/<int:auction_id>/', views.edit_auction, name='edit_auction'),
    path('cancel-auction/<int:auction_id>/', views.cancel_auction, name='cancel_auction'),
=======
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_auction, name='create_auction'),
    path('my-auctions/', views.my_auctions, name='my_auctions'),
    path('live-auctions/', views.live_auctions, name='live_auctions'),
    path('edit-auction/<int:auction_id>/', views.edit_auction, name='edit_auction'),
    path('cancel-auction/<int:auction_id>/', views.cancel_auction, name='cancel_auction'),
>>>>>>> 7159795b6044deffa8701f4b9b7a29f57ca8987b
]