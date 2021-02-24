from django.db import models

# Create your models here.


# Accessing the POSTGRES database with a class:
class Teacher(models.Model):
    name = models.CharField(max_length=80)
    age = models.IntegerField()


class TestModel(models.Model):
    field1 = models.CharField(max_length=80)
    field2 = models.IntegerField()


