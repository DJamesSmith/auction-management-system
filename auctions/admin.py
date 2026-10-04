from django.contrib import admin
from .models import Auction, Category, Transaction


admin.site.register(Category)


@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):

    list_display = (
        'item_name',
        'seller',
        'status',
        'winner',
        'winning_amount',
        'end_datetime',
    )

    list_select_related = ('seller', 'winner')

    actions = [
        'approve_auctions',
        'reject_auctions',
    ]

    @admin.action(description='Approve selected auctions')
    def approve_auctions(self, request, queryset):

        updated = queryset.filter(
            status='PENDING'
        ).update(
            status='APPROVED'
        )

        self.message_user(
            request,
            f'{updated} auction(s) approved successfully.'
        )

    @admin.action(description='Reject selected auctions')
    def reject_auctions(self, request, queryset):

        updated = queryset.filter(
            status='PENDING'
        ).update(
            status='REJECTED'
        )

        self.message_user(
            request,
            f'{updated} auction(s) rejected successfully.'
        )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'auction',
        'seller',
        'buyer',
        'winning_amount',
        'status',
        'transaction_date',
    )

    list_select_related = ('auction', 'seller', 'buyer')