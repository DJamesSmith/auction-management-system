from django.db import models
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.item_name
    

    def update_status(self):
        now = timezone.now()
        if self.status == 'APPROVED' and now >= self.start_datetime:
            self.status = 'ACTIVE'
            self.save(update_fields=['status'])

        elif self.status == 'ACTIVE' and now >= self.end_datetime:
            self.status = 'CLOSED'
            self.save(update_fields=['status'])