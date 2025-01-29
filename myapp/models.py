from django.db import models

# Create your models here.

class person(models.Model):
    fname = models.CharField(max_length=51, null=True, blank=True)
    lname = models.CharField(max_length=51, null=True, blank=True)
    ismale = models.BooleanField(null=True, blank=True)
    email = models.CharField(max_length=54, null=True, blank=True)
    phone = models.CharField(max_length=21, null=True, blank=True)
    cin = models.CharField(max_length=21, null=True, blank=True)
    cen = models.CharField(max_length=21, null=True, blank=True)
    info = models.CharField(max_length=4096, null=True, blank=True)
    bday = models.CharField(max_length=21, null=True, blank=True)
    
    def __str__(self) -> str:
        if self.lname and self.fname: 
            return self.fname + " " + self.lname
        elif self.lname:
            return  self.lname
        elif self.fname:
            return self.fname
        else:
            return ""
            
