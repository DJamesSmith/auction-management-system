from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from django.contrib import messages
from .models import User
from auctions.models import Auction
from bids.models import Bid

@never_cache
@login_required(login_url='login')
def home(request):
    return render(request, "home.html")

def register_view(request):
    if request.method == "POST":
        print(request.POST)
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        role = request.POST.get("role")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Password Validation
        if password != confirm_password:
            messages.error(request,"Password and Confirm Password do not match.")
            return redirect("register")

        # Email Check
        if User.objects.filter(email=email).exists():
            messages.error(request,"Email already exists.")
            return redirect("register")

        # Phone Check
        if User.objects.filter(phone=phone).exists():
            messages.error(request,"Phone number already exists.")
            return redirect("register")

        # create_user method from UserManager
        User.objects.create_user(name=name, email=email, phone=phone, password=password)
        messages.success(request,"Registration Successful. Please Login.")
        return redirect("login")

    return render(request,"accounts/register.html")

def login_view(request):
    context: dict = {
        "error": ""
    }

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)        # "Mark this user as logged in by creating a session."
            return redirect("dashboard")
        else:
            context["error"] = "Invalid Email/Phone or Password"

    return render(request,"accounts/login.html", context)


@never_cache
@login_required(login_url='login')
def dashboard(request):
    user = request.user
    
    own_auctions = Auction.objects.filter(seller=user)

    active_auctions_count = Auction.objects.filter(status='ACTIVE').count()
    own_auctions_count = own_auctions.count()
    bids_placed_count = Bid.objects.filter(bidder=user).count()

    won_auctions = (
        Auction.objects
        .filter(winner=user, status='CLOSED')
        .select_related('seller', 'category')
        .select_related('transaction')
        .order_by('-end_datetime')
    )

    context = {
        'own_auctions_count': own_auctions_count,
        'active_auctions_count': active_auctions_count,
        'bids_placed_count': bids_placed_count,
        'winning_auctions_count': won_auctions.count(),
        'won_auctions': won_auctions,
    }

    response = render(request,"accounts/dashboard.html", context)
    
    response["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"

    return response


def logout_view(request):
    logout(request)
    return redirect("login")