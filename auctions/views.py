from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Category, Bid, Comment
from .forms import NewListing


def index(request):
    listings = Listing.objects.all()
    context = {"listings": listings}
    # Get the bids
    context["bids"] = [l.best_bid() for l in listings]
    return render(request, "auctions/index.html", context)


def listing(request, id):
    listing = Listing.objects.get(pk=id)

    # Check if listing is has ended
    if listing.ended:
        context = {"winner_bid": listing.best_bid(), "listing": listing}
        return render(request, "auctions/listing_ended.html", context)
    
    context = {"listing": listing}

    # Get the best bid
    context["current_bid"] = listing.best_bid()

    # Load comments
    context["comments"] = listing.comments.all()

    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        
        # Check if the id is already in the watchlist
        if not listing_id in request.session["watchlist"]:
            request.session["watchlist"].append(listing_id)
        else:
            request.session["watchlist"].remove(listing_id)
        request.session.modified = True

    # Check if watchlist exist in sessions
    if not "watchlist" in request.session:
        request.session["watchlist"] = []
    watchlist = id in request.session["watchlist"]
    context["watchlist"] = watchlist

    return render(request, "auctions/listing.html", context)


def create_listing(request):
    if request.method == "POST":
        form = NewListing(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["price"]
            img = form.cleaned_data["img_url"]
            category_name = dict(form.fields['category'].choices)[int(form.cleaned_data["category"])]
            try:
                # We create the listing
                new_listing = Listing(title=title,
                                        description=description,
                                        img_url=img,                                        
                                        author=request.user,
                                        category=Category.objects.get(pk=category_name))
                new_listing.save()

                # We create the first bid
                new_bid = Bid(price=price, listing=new_listing, author=request.user)
                new_bid.save()

            except IntegrityError:
                context = {"message": "An error ocurred."}
                return render(request, "auctions/create.html", context)

            return HttpResponseRedirect(reverse("listing", args=[new_listing.id]))



    categories = Category.objects.all()
    context = {"listing_form": NewListing()}
    return render(request, "auctions/create.html", context)


def watchlist(request):
    if not "watchlist" in request.session:
        request.session["watchlist"] = []
    listings = []
    for id in request.session["watchlist"]:
        listings.append(Listing.objects.get(pk=int(id)))
    context = {"watchlist": listings}
    # Get the bids
    context["bids"] = [l.best_bid() for l in listings]
    return render(request, "auctions/watchlist.html", context)


def bid_registration(request):
    if request.method == "POST":
        price = request.POST["price"]
        listing = Listing.objects.get(pk=int(request.POST["listing-id"]))
        author = request.user
        new_bid = Bid(price=price , listing=listing , author=author)
        new_bid.save()
        context = {"bid": new_bid}
        return render(request, "auctions/bid.html", context)

    return HttpResponseRedirect(reverse("index"))


def close_bid(request):
    if request.method == "POST":
        listing = Listing.objects.get(pk=request.POST["listing-id"])
        listing.ended = True
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=[listing.id]))


def add_comment(request):
    if request.method == "POST":
        listing = Listing.objects.get(pk=request.POST["listing-id"])
        new_comment = Comment(comment= request.POST["comment"], listing=listing, author=request.user)
        new_comment.save()
        return HttpResponseRedirect(reverse("listing", args=[listing.id]))


def categories(request):
    context = {}
    if request.method == "POST":
        print(request.POST)
        category = Category.objects.get(pk=request.POST["selected"])
        context["listings"] = category.listings.all()
        context["category_selected"] = category
    
    context["categories"] = Category.objects.all()
    return render(request, "auctions/categories.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")