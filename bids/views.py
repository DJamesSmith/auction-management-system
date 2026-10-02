from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect
from django.utils import timezone

from auctions.models import Auction
from .models import Bid


@login_required(login_url="login")
def place_bid(request, auction_id):
    if request.method != "POST":
        messages.error(request, "Only POST requests are allowed.")
        return redirect("live_auctions")

    if request.user.role != "GENERAL_USER":
        messages.error(request, "Administrators are not allowed to place bids.")
        return redirect("live_auctions")

    with transaction.atomic():
        try:
            auction = (
                Auction.objects
                .select_for_update()
                .get(pk=auction_id)
            )
        except Auction.DoesNotExist:
            messages.error(request, "Auction not found.")
            return redirect("live_auctions")

        # Re-evaluate the auction status while holding the row lock.
        auction.update_status()

        if auction.status != "ACTIVE":
            messages.error(request, "This auction is no longer live.")
            return redirect("live_auctions")

        if timezone.now() >= auction.end_datetime:
            auction.status = "CLOSED"
            auction.save(update_fields=["status", "updated_at"])
            messages.error(request, "This auction has ended.")
            return redirect("live_auctions")

        latest_bid = (
            Bid.objects
            .filter(auction=auction)
            .order_by("-amount", "-created_at")
            .first()
        )

        current_price = (
            latest_bid.amount
            if latest_bid
            else auction.starting_price
        )

        next_bid_amount = current_price + auction.minimum_bid_increment
        Bid.objects.create(auction=auction, bidder=request.user, amount=next_bid_amount)

    messages.success(request, f"Bid of ₹{next_bid_amount:.2f} placed successfully for {auction.item_name}.")

    return redirect("live_auctions")


@login_required(login_url="login")
def bid_history(request):
    bids = (
        Bid.objects
        .select_related("auction", "auction__category", "bidder")
        .order_by("-created_at"))
    return render(request, "bids/bid_history.html", {"bids": bids})