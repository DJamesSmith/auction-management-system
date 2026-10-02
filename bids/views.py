from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import render

from auctions.models import Auction
from .models import Bid


@login_required(login_url="login")
def place_bid(request, auction_id):
    if request.method != "POST":
        return JsonResponse({
            "status": "error",
            "message": "Only POST requests are allowed."
        }, status=405)

    if request.user.role != "GENERAL_USER":
        return JsonResponse({
                "status": "error",
                "message": "Administrators are not allowed to place bids.",
            }, status=403)

    with transaction.atomic():
        try:
            auction = (
                Auction.objects
                .select_for_update()
                .get(pk=auction_id))
        except Auction.DoesNotExist:
            return JsonResponse({
                "status": "error",
                "message": "Auction not found."
                }, status=404)

        # Re-evaluate the auction status while holding the row lock.
        auction.update_status()

        if auction.status != "ACTIVE":
            return JsonResponse({
                "status": "error",
                "message": "This auction is no longer live.",
            }, status=400)

        if timezone.now() >= auction.end_datetime:
            auction.status = "CLOSED"
            auction.save(update_fields=["status", "updated_at"])
            return JsonResponse({
                "status": "error",
                "message": "This auction has ended."
            }, status=400)

        latest_bid = (Bid.objects
                    .filter(auction=auction)
                    .order_by("-amount", "-created_at")
                    .first())

        current_price =  latest_bid.amount if latest_bid else auction.starting_price
        next_bid_amount = current_price + auction.minimum_bid_increment

        Bid.objects.create(auction=auction, bidder=request.user, amount=next_bid_amount)

    return JsonResponse({
        "status": "success",
        "message": "Bid placed successfully.",
        "auction_id": auction.id,
        "current_price": str(next_bid_amount),
        "next_bid_amount": str(next_bid_amount + auction.minimum_bid_increment),
    })


@login_required(login_url="login")
def bid_history(request):
    bids = (
        Bid.objects
        .select_related("auction", "auction__category", "bidder")
        .order_by("-created_at"))

    return render(request, "bids/bid_history.html", { "bids": bids })