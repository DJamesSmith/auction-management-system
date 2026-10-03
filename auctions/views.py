from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

from .forms import AuctionForm
from .models import Auction, Category
from bids.models import Bid
from django.db.models import Prefetch


@login_required
def create_auction(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        form = AuctionForm(request.POST,request.FILES)

        if form.is_valid():
            auction = form.save(commit=False)
            auction.seller = request.user
            auction.status = 'PENDING'
            auction.save()

            messages.success(request,'Auction created successfully and sent for admin approval.')

            return redirect('my_auctions')

        else:
            return render(request, 'auctions/create_auction.html', {
                'categories': categories,
                'form': form,
                'data': request.POST
            })

    return render(request,'auctions/create_auction.html', {
        'categories': categories
    })


@login_required
def my_auctions(request):
    auctions = Auction.objects.filter(
        seller=request.user
    ).order_by('-created_at')

    for auction in auctions:
        auction.update_status()

    return render(request, 'auctions/my_auctions.html', { 'auctions': auctions })


# objective is to move approved auctions into ACTIVE when their scheduled start time has arrived, and close active auctions whose end time has passed.
@login_required
def live_auctions(request: HttpRequest) -> HttpResponse:
    scheduled_auctions = Auction.objects.filter(status__in=['APPROVED', 'ACTIVE'])

    for auction in scheduled_auctions:
        auction.update_status()

    live_auctions_queryset = (
        Auction.objects
        .filter(status='ACTIVE')
        .select_related('category', 'seller')
        .prefetch_related(
            Prefetch(
                'bids',
                queryset=Bid.objects.order_by('-amount', '-created_at'),
                to_attr='ordered_bids',
            ))
        .order_by('end_datetime'))

    for auction in live_auctions_queryset:
        latest_bid = auction.ordered_bids[0] if auction.ordered_bids else None

        auction.current_price =  latest_bid.amount if latest_bid else auction.starting_price
        auction.next_bid_amount = auction.current_price + auction.minimum_bid_increment

    return render(request, 'auctions/live_auctions.html', { 'auctions': live_auctions_queryset })



@login_required
def edit_auction(request, auction_id):

    auction = Auction.objects.get(
        id=auction_id,
        seller=request.user
    )

    categories = Category.objects.all()

    if request.method == 'POST':

        form = AuctionForm(
            request.POST,
            request.FILES,
            instance=auction
        )

        if form.is_valid():

            auction = form.save(commit=False)

            # Keep the same seller
            auction.seller = request.user

            # Keep current status
            auction.status = auction.status

            auction.save()

            messages.success(
                request,
                'Auction updated successfully.'
            )

            return redirect('my_auctions')

        else:

            return render(
                request,
                'auctions/edit_auction.html',
                {
                    'categories': categories,
                    'form': form,
                    'auction': auction
                }
            )

    form = AuctionForm(instance=auction)

    return render(
        request,
        'auctions/edit_auction.html',
        {
            'categories': categories,
            'form': form,
            'auction': auction
        }
    )


@login_required
def cancel_auction(request, auction_id):

    auction = Auction.objects.get(
        id=auction_id,
        seller=request.user
    )

    if auction.status in ['PENDING', 'APPROVED']:

        auction.delete()

        messages.success(
            request,
            'Auction cancelled successfully.'
        )

    else:

        messages.error(
            request,
            'This auction cannot be cancelled.'
        )

    return redirect('my_auctions')

