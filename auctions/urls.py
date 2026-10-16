from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_auction, name='create_auction'),
    path('my-auctions/', views.my_auctions, name='my_auctions'),
    path('live-auctions/', views.live_auctions, name='live_auctions'),
    path('edit-auction/<int:auction_id>/', views.edit_auction, name='edit_auction'),
    path('cancel-auction/<int:auction_id>/', views.cancel_auction, name='cancel_auction'),
    path('timer/<int:auction_id>/', views.auction_timer, name='auction_timer'),
    path('predict-category/',views.auction_image_prediction,name='auction_image_prediction'),
    path('prediction-status/<int:prediction_id>/', views.auction_image_prediction_status, name='auction_image_prediction_status'),
]