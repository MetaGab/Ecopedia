from django.db import models

# Create your models here.
class Animal(models.Model):
    name = models.CharField(max_length=256)
    slug = models.CharField(max_length=256)
    description = models.TextField()
    image_link = models.CharField(max_length=1024)
    map_link = models.CharField(max_length=1024)

class Tip(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    description = models.TextField()

class Question(models.Model):
    description = models.TextField()

class Quiz(models.Model):
    quid = models.CharField(max_length=6)
    expires_at = models.DateTimeField()
    questions = models.ManyToManyField(Question)
    active = models.BooleanField(default=True)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    description = models.TextField()
    is_correct = models.BooleanField(default=False)