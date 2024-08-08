from django.db import models

# Create your models here.


class person(models.Model):
    fname = models.CharField(max_length=51)
    lname = models.CharField(max_length=51)
    ismale = models.BooleanField()
    email = models.CharField( max_length=54)
    phone = models.CharField(max_length=21)
    cin = models.CharField(max_length=21)
    cen = models.CharField(max_length=21)
    info = models.CharField(max_length=4096)
    bday = models.CharField(max_length=21)
    
    def __str__(self) -> str:
        return self.fname + " "+ self.lname
