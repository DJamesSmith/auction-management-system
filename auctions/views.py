from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import AuctionForm
from .models import Auction, Category


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
            return render(request,'auctions/create_auction.html',
                {
                    'categories': categories,
                    'form': form,
                    'data': request.POST
                }
            )

    return render(request,'auctions/create_auction.html',
        {
            'categories': categories
        }
    )


@login_required
def my_auctions(request):
    auctions = Auction.objects.filter(
        seller=request.user
    ).order_by('-created_at')

    for auction in auctions:
        auction.update_status()

    return render(
        request,
        'auctions/my_auctions.html',
        {
            'auctions': auctions
        }
    )


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














