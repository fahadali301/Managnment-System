from django.contrib.auth.models import AbstractUser, Group
from django.db import models
class Company(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)


class Branch(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)



class Building(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)


class Floor(models.Model):
    Floor_name = models.CharField(max_length=100)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)


class Room(models.Model):
    name = models.CharField(max_length=100)
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)

class Asset(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)


class Permissions(models.Model):
    permission = models.CharField(max_length=100)
    codename = models.CharField(max_length=100,default='')



class Role(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    ]
    role = models.CharField(
        max_length=100,
        choices=ROLE_CHOICES,
        null=False,
        blank=False,
    )
    permissions = models.ManyToManyField(Permissions, related_name='roles')



class User(AbstractUser):

    address = models.CharField(max_length=255, default='Unknown')
    role = models.ForeignKey(Role, on_delete=models.CASCADE,default=1)

