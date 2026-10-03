from django.contrib import admin
from .models import Auction, Category


admin.site.register(Category)


@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):

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