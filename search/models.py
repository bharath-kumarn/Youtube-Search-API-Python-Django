
from django.db import models
class Favourites(models.Model):
	title = models.CharField(max_length=255, blank=True, null=True)
	yt_link = models.CharField(max_length=255, blank=True, null=True)

	class Meta:
		managed = True

	def __str__(self):
		return self.title
