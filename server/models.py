from django.db import models
from django.contrib.auth.models import User

class Thread(models.Model):
	name = models.CharField(max_length=100)
	user = models.ForeignKey(User)
	date = models.DateTimeField()
	type = models.CharField(max_length=50)
	last_post = models.DateTimeField()

class Post(models.Model):
	thread = models.ForeignKey(Thread)
	content = models.TextField(max_length=10000)
	user = models.ForeignKey(User)
	date = models.DateTimeField()

class Thumb(models.Model):
	user = models.ForeignKey(User)
	post = models.ForeignKey(Post)

class PollOption(models.Model):
	thread = models.ForeignKey(Thread)
	name = models.CharField(max_length=100)

class PollVote(models.Model):
	user = models.ForeignKey(User)
	option = models.ForeignKey(PollOption)
	date = models.DateTimeField()

class LastThreadVisit(models.Model):
	user = models.ForeignKey(User)
	thread = models.ForeignKey(Thread)
	date = models.DateTimeField()

class Profile(models.Model):
	user = models.ForeignKey(User)
	last_post = models.DateTimeField()

