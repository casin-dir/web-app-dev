from django.contrib.auth.models import User
from django.db import models



# Create your models here.
class Team(models.Model):
    name = models.CharField( max_length=50 )
    country = models.CharField( max_length = 30 )
    sportType = models.CharField( max_length = 30 )
    prizeCount = models.IntegerField()
    desc = models.CharField( max_length=2000, null=True  )
    imageUrl = models.CharField( max_length=100, null=True )
    betUsers = models.ManyToManyField( User )
    
    def __str__(self):
        return "Name = %s, Country = %s, sportType = %s" % (self.name, self.country, self.sportType) 


