from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<str:id>", views.listing, name="listing"),
    path("createlisting", views.create_listing, name="newlisting"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("bid", views.bid_registration, name="bid"),
    path("categories", views.categories, name="categories"),
    path("closebid", views.close_bid, name="closebid"),
    path("comment", views.add_comment, name="addcomment")
]
