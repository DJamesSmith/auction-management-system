from django.contrib import admin
from .models import Bid

admin.site.register(Bid)

# so an administrator can inspect bid records;
# Django Admin having full CRUD access to Bid records