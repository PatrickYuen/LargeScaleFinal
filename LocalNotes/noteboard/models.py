from django.db import models

class Post(models.Model):
	title = models.CharField(max_length=70)
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title