from django.db import models
		
class City(models.Model):
	name = models.CharField(max_length=200)
	country = models.CharField(max_length=50)
	summary = models.TextField()
	pub_date = models.DateTimeField('date published', auto_now_add=True)

	def __str__(self):
		return self.name
		
class User(models.Model):
	username = models.CharField(max_length=50)
	password = models.CharField(max_length=50)
	
	def __str__(self):
		return self.username
		
class Post(models.Model):
	title = models.CharField(max_length=50)
	city = models.ForeignKey(City, null=False)
	user = models.ForeignKey(User, null=False)
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title
	