from django.db import models


class User(models.Model):
    id = models.CharField(max_length=36, primary_key=True, default='')
    email = models.EmailField()
    firstName = models.CharField(max_length=245)
    lastName = models.CharField(max_length=245)


class Course(models.Model):
    id = models.CharField(max_length=36, primary_key=True, default='')
    title = models.TextField()
    description = models.TextField()
    publishedAt = models.DateTimeField()


class Certificate(models.Model):
    course = models.CharField(max_length=36, default='')
    user = models.CharField(max_length=36, default='')
    completedDate = models.DateTimeField()
    startDate = models.DateTimeField()



