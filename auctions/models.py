from django.db import models, transaction
from accounts.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Auction(models.Model):

    STATUS_CHOICES = (
        ('PENDING', 'Pending Approval'),
        ('APPROVED', 'Approved'),
        ('ACTIVE', 'Live / Active'),
        ('CLOSED', 'Closed'),
        ('CANCELLED', 'Cancelled'),
        ('REJECTED', 'Rejected'),
    )

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auctions')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='auctions')
    item_name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='auction_images/', blank=True, null=True)
    starting_price = models.DecimalField(max_digits=12,decimal_places=2)
    minimum_bid_increment = models.DecimalField(max_digits=12,decimal_places=2)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    # These fields permanently record the result when the auction closes.
    winner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='won_auctions',
        blank=True,
        null=True)
    winning_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.item_name
    

    def update_status(self):
        now = timezone.now()
        if self.status == 'APPROVED' and now >= self.start_datetime:
            self.status = 'ACTIVE'
            self.save(update_fields=['status', 'updated_at'])

        elif self.status == 'ACTIVE' and now >= self.end_datetime:
            from bids.models import Bid
            
            winning_bid = (
                Bid.objects
                .filter(auction=self)
                .select_related('bidder')
                .order_by('-amount', '-created_at')
                .first())

            with transaction.atomic():
                self.status = 'CLOSED'

                if winning_bid:
                    self.winner = winning_bid.bidder
                    self.winning_amount = winning_bid.amount

                self.save(update_fields=['status', 'winner', 'winning_amount', 'updated_at'])

                if winning_bid:
                    Transaction.objects.update_or_create(
                        auction=self,
                        defaults={
                            'seller': self.seller,
                            'buyer': winning_bid.bidder,
                            'winning_amount': winning_bid.amount,
                            'status': 'COMPLETED',
                            'transaction_date': now,
                        })


class Transaction(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'))

    auction = models.OneToOneField(Auction, on_delete=models.CASCADE, related_name='transaction')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sold_transactions')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchased_transactions')
    winning_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    transaction_date = models.DateTimeField()

    def __str__(self):
        return f'Transaction for {self.auction.item_name} - ₹{self.winning_amount}'