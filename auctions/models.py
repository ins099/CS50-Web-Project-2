from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
	pass


class Category(models.Model):
	name = models.CharField(max_length=60, blank=False, primary_key=True)

	def __str__(self):
		return self.name


class Listing(models.Model):
	title = models.CharField(max_length=70, blank=False)
	description = models.TextField(blank=True)
	img_url = models.URLField(blank=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listings")
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
	date_created = models.DateField(auto_now_add=True)
	ended = models.BooleanField(default=False)

	def best_bid(self):
		bids = self.bids.all()
		prices = [i.price for i in bids]
		return bids[prices.index(max(prices))]

	def __str__(self):
		return self.title


class Bid(models.Model):
	price = models.FloatField(null=False)
	listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
	time_stamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.price)


class Comment(models.Model):
	comment = models.TextField(null=False)
	listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments", null=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
	time_stamp = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.comment