from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
		
class City(models.Model):
	name = models.CharField(max_length=200)
	country = models.CharField(max_length=50)
	summary = models.TextField()
	pub_date = models.DateTimeField('date published', auto_now_add=True)

	def __str__(self):
		return self.name
		
class Post(models.Model):
	title = models.CharField(max_length=50)
	city = models.ForeignKey(City, null=False)
	userid = models.IntegerField(default=0, null=False) #Not a foreign key because user is in seperate DB
	user = models.CharField(max_length=200)
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title

# Model Forms
class MyUserCreationForm(UserCreationForm):
  class Meta(UserCreationForm.Meta):
    help_texts = {
      'username' : '',
    }